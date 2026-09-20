from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
import re
import zipfile
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter

SYMBOLS = (
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK",
    "SBIN", "ITC", "BHARTIARTL", "LT", "AXISBANK",
)

CONTEXT = 128
TOP_K = 3
FOLDS = 4
DEV_FOLDS = (1, 2, 3)
HOLDOUT_FOLD = 4
MODEL_ORIGINS_PER_BATCH = 16
PRIMARY_SLIPPAGE = 0.0005
SLIPPAGE_STRESSES = (0.0, 0.00025, 0.00050, 0.0010, 0.0020)
CAPITAL = 1_000_000.0
MAX_PARTICIPATION = 0.01
EWMA_SPAN = 20
EWMA_ALPHA = 2.0 / (EWMA_SPAN + 1.0)

# Effective-date cash-delivery research inputs from the project fee manifest.
BROKERAGE = 20.0
DP_SELL = 13.5
STT_BUY = 0.001
STT_SELL = 0.001
EXCHANGE_IPFT = 0.0000307
SEBI_FEE = 0.000001
STAMP_BUY = 0.00015
GST = 0.18

SOURCE_SHA256 = "20024713c455cc16b5daae91e06991d57a1acfa6a30c77bb7d5a742ee1789ab2"
EXTERNAL_COMMIT = "aa60b746f089c3f54df6760bf021708c2d3ce1e8"
END_DATE = "2026-03-31"
IST = timezone(timedelta(hours=5, minutes=30))


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_ts(v: str) -> datetime:
    return datetime.fromtimestamp(int(v), tz=timezone.utc).astimezone(IST)


def read_stock_sessions(zf: zipfile.ZipFile, symbol: str):
    target = f"{symbol}_1m.csv.gz"
    names = [n for n in zf.namelist() if n == target or n.endswith("/" + target) or n.endswith(target)]
    if not names:
        raise RuntimeError(f"{symbol}: minute file not found in release")
    import io

    by_day = defaultdict(list)
    with zf.open(names[0], "r") as raw:
        with gzip.GzipFile(fileobj=raw) as gz:
            text = gz.read().decode("utf-8")

    for row in csv.DictReader(io.StringIO(text)):
        t = parse_ts(row["time"])
        minute = t.hour * 60 + t.minute
        if not (9 * 60 + 15 <= minute <= 15 * 60 + 29):
            continue
        o = float(row["open"])
        h = float(row["high"])
        l = float(row["low"])
        c = float(row["close"])
        valid = (
            o > 0 and h > 0 and l > 0 and c > 0
            and l <= min(o, c) <= max(o, c) <= h
        )
        by_day[t.date().isoformat()].append({
            "ts": int(row["time"]),
            "minute": minute - (9 * 60 + 15),
            "open": o,
            "close": c,
            "volume": float(row.get("Volume", 0) or 0),
            "valid": valid,
        })

    sessions = {}
    for day, vals in by_day.items():
        vals.sort(key=lambda x: x["ts"])
        if (
            len(vals) == 375
            and vals[0]["minute"] == 0
            and vals[-1]["minute"] == 374
            and all(v["valid"] for v in vals)
        ):
            daily_value = sum(v["close"] * max(v["volume"], 0.0) for v in vals)
            sessions[day] = {
                "close": vals[-1]["close"],
                "open": vals[0]["open"],
                "value": daily_value,
            }
    return sessions


def parse_date(raw: str):
    value = raw.strip().strip('"').replace("\ufeff", "")
    formats = (
        "%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y",
        "%d-%b-%Y", "%d-%B-%Y", "%Y-%m-%d",
    )
    for fmt in formats:
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return None


def read_price_csv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as fh:
        rows = list(csv.DictReader(fh))
    out = {}
    for row in rows:
        d = parse_date(row.get("Date", ""))
        if not d:
            continue
        close_raw = row.get("Close") or row.get("Price") or row.get("Close ")
        if close_raw is None:
            continue
        close = float(str(close_raw).replace(",", "").strip())
        if close > 0:
            out[d] = close
    return dict(sorted(out.items()))


def daily_returns(price_map):
    out = {}
    dates = list(price_map)
    for prev, cur in zip(dates, dates[1:]):
        if price_map[prev] > 0 and price_map[cur] > 0:
            out[cur] = math.log(price_map[cur] / price_map[prev])
    return out


def previous_available(ret_map, signal_day):
    candidates = [d for d in ret_map if d < signal_day]
    return ret_map[max(candidates)] if candidates else math.nan


def same_or_previous_available(ret_map, signal_day):
    candidates = [d for d in ret_map if d <= signal_day]
    return ret_map[max(candidates)] if candidates else math.nan


def load_corporate_actions(actions_dir: Path, symbol: str):
    path = actions_dir / f"{symbol}_actions.csv"
    dates = set()
    if not path.exists():
        return dates
    with path.open("r", encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("exchange") == "NSE" and row.get("ex_date"):
                dates.add(row["ex_date"][:10])
    return dates


def find_header_and_parse_flow(path: Path):
    status = {"path": str(path), "parsed": False, "sheet": None, "reason": None, "rows": 0}
    try:
        from openpyxl import load_workbook
    except ImportError as exc:
        status["reason"] = f"openpyxl unavailable: {exc}"
        return {}, status

    if not path.exists():
        status["reason"] = "FII/DII workbook not present"
        return {}, status

    try:
        wb = load_workbook(path, read_only=True, data_only=True)
        for ws in wb.worksheets:
            rows = list(ws.iter_rows(values_only=True))
            for header_idx, row in enumerate(rows[:30]):
                labels = [str(x).strip().lower() if x is not None else "" for x in row]
                if not any("date" in x for x in labels):
                    continue
                date_col = next((i for i, x in enumerate(labels) if "date" in x), None)
                fii_cols = [i for i, x in enumerate(labels) if "fii" in x or "fpi" in x]
                dii_cols = [i for i, x in enumerate(labels) if "dii" in x]
                if date_col is None or not fii_cols or not dii_cols:
                    continue

                def pick_net(cols):
                    for i in cols:
                        if "net" in labels[i]:
                            return [i]
                    return cols

                fii_use = pick_net(fii_cols)
                dii_use = pick_net(dii_cols)
                out = {}
                for data_row in rows[header_idx + 1:]:
                    if date_col >= len(data_row):
                        continue
                    value = data_row[date_col]
                    if hasattr(value, "strftime"):
                        day = value.strftime("%Y-%m-%d")
                    else:
                        day = parse_date(str(value))
                    if not day:
                        continue
                    try:
                        fii = sum(float(data_row[i]) for i in fii_use if i < len(data_row) and data_row[i] not in (None, ""))
                        dii = sum(float(data_row[i]) for i in dii_use if i < len(data_row) and data_row[i] not in (None, ""))
                    except (ValueError, TypeError):
                        continue
                    out[day] = (fii, dii)
                if len(out) >= 50:
                    status.update({"parsed": True, "sheet": ws.title, "rows": len(out)})
                    return dict(sorted(out.items())), status
        status["reason"] = "No robust Date/FII/DII header detected"
        return {}, status
    except Exception as exc:
        status["reason"] = repr(exc)
        return {}, status


def load_global_feature_maps(global_dir: Path):
    names = {
        "nifty": "Nifty 50 Historical Data.csv",
        "nikkei": "Nikkei 225 Historical Data.csv",
        "hang": "Hang Seng Historical Data.csv",
        "sp500": "S&P 500 Historical Data.csv",
        "dax": "DAX Historical Data.csv",
        "brent": "Brent Oil Futures Historical Data.csv",
        "gold": "Gold Futures Historical Data.csv",
        "dxy": "US Dollar Index Historical Data.csv",
    }
    return {
        key: daily_returns(read_price_csv(global_dir / filename))
        for key, filename in names.items()
    }


def feature_row(feature_maps, signal_day):
    return {
        "nifty_same_day": same_or_previous_available(feature_maps["nifty"], signal_day),
        "nikkei_same_day": same_or_previous_available(feature_maps["nikkei"], signal_day),
        "hang_same_day": same_or_previous_available(feature_maps["hang"], signal_day),
        "sp500_prev_day": previous_available(feature_maps["sp500"], signal_day),
        "dax_prev_day": previous_available(feature_maps["dax"], signal_day),
        "brent_prev_day": previous_available(feature_maps["brent"], signal_day),
        "gold_prev_day": previous_available(feature_maps["gold"], signal_day),
        "dxy_prev_day": previous_available(feature_maps["dxy"], signal_day),
    }


def make_covariate_matrix(days, data_by_symbol, feature_maps, flow_map, use_flows, signal_idx, symbol):
    rows = []
    for idx in range(max(0, signal_idx - CONTEXT + 1), signal_idx + 1):
        day = days[idx]
        close_return = data_by_symbol[symbol]["close_return"][idx]
        breadth = float(data_by_symbol[symbol]["breadth"][idx])
        rv20 = float(data_by_symbol[symbol]["rv20"][idx])
        features = feature_row(feature_maps, day)
        row = [
            features["nifty_same_day"],
            features["nikkei_same_day"],
            features["hang_same_day"],
            features["sp500_prev_day"],
            features["dax_prev_day"],
            features["brent_prev_day"],
            features["gold_prev_day"],
            features["dxy_prev_day"],
            breadth,
            rv20,
            close_return,
        ]
        if use_flows:
            prior_dates = [d for d in flow_map if d < day]
            if prior_dates:
                fii, dii = flow_map[max(prior_dates)]
            else:
                fii, dii = (math.nan, math.nan)
            row.extend([fii, dii])
        rows.append(row)

    arr = np.asarray(rows, dtype=np.float32)
    # Causal row-wise fill: each column uses its last observed value.
    for col in range(arr.shape[1]):
        last = 0.0
        for r in range(arr.shape[0]):
            if not np.isfinite(arr[r, col]):
                arr[r, col] = last
            else:
                last = float(arr[r, col])
    return arr.T


def build_stock_daily(sessions_by_symbol, common_days, actions):
    out = {}
    for symbol in SYMBOLS:
        s = sessions_by_symbol[symbol]
        close = np.asarray([s[d]["close"] for d in common_days], dtype=np.float64)
        op = np.asarray([s[d]["open"] for d in common_days], dtype=np.float64)
        value = np.asarray([s[d]["value"] for d in common_days], dtype=np.float64)
        close_ret = np.full(len(common_days), np.nan)
        overnight = np.full(len(common_days), np.nan)
        for i in range(1, len(common_days)):
            close_ret[i] = math.log(close[i] / close[i-1])
            overnight[i] = math.log(op[i] / close[i-1])
        rv20 = np.full(len(common_days), np.nan)
        for i in range(20, len(common_days)):
            rv20[i] = float(np.std(close_ret[i-20:i]))
        out[symbol] = {
            "close": close,
            "open": op,
            "value": value,
            "close_return": close_ret,
            "overnight": overnight,
            "actions": actions[symbol],
            "rv20": rv20,
        }

    breadth = np.full(len(common_days), np.nan)
    for i in range(len(common_days)):
        vals = [out[s]["close_return"][i] for s in SYMBOLS if np.isfinite(out[s]["close_return"][i])]
        breadth[i] = float(np.mean(np.asarray(vals) > 0)) if vals else math.nan
    for symbol in SYMBOLS:
        out[symbol]["breadth"] = breadth
    return out


def eligible_origin(days, stock, idx):
    if idx < CONTEXT or idx + 1 >= len(days):
        return False
    signal_day = days[idx]
    target_day = days[idx + 1]
    if signal_day > END_DATE or target_day > END_DATE:
        return False
    if signal_day in stock["actions"] or target_day in stock["actions"]:
        return False
    return (
        np.isfinite(stock["overnight"][idx])
        and np.isfinite(stock["rv20"][idx])
        and np.all(np.isfinite(stock["overnight"][idx - CONTEXT + 1:idx + 1]))
    )


def fold_indices(days):
    eligible_days = list(range(CONTEXT, len(days) - 1))
    eligible_days = [i for i in eligible_days if days[i] <= END_DATE and days[i + 1] <= END_DATE]
    edges = np.linspace(0, len(eligible_days), FOLDS + 1, dtype=int)
    return {
        fold: eligible_days[edges[fold-1]:edges[fold]]
        for fold in range(1, FOLDS + 1)
    }


def cost_trade(capital, buy_price, sell_price, slippage):
    buy_px = buy_price * (1.0 + slippage)
    sell_px = sell_price * (1.0 - slippage)
    qty = (capital / TOP_K) / buy_px
    buy_notional = qty * buy_px
    sell_notional = qty * sell_px

    brokerage = 2.0 * BROKERAGE
    turnover = buy_notional + sell_notional
    exchange = turnover * EXCHANGE_IPFT
    sebi = turnover * SEBI_FEE
    stt = buy_notional * STT_BUY + sell_notional * STT_SELL
    stamp = buy_notional * STAMP_BUY
    gst = GST * (brokerage + exchange + sebi)
    dp = DP_SELL
    gross = sell_px / buy_px - 1.0
    fixed = brokerage + exchange + sebi + stt + stamp + gst + dp
    pnl = qty * (sell_px - buy_px) - fixed
    return {
        "gross_return": gross,
        "pnl": pnl,
        "brokerage": brokerage,
        "exchange": exchange,
        "sebi": sebi,
        "stt": stt,
        "stamp": stamp,
        "gst": gst,
        "dp": dp,
    }


def simulate(periods, strategy, slippage):
    capital = CAPITAL
    path = []
    cost_total = defaultdict(float)
    participation = []
    for row in periods:
        chosen = sorted(row[strategy].items(), key=lambda x: (x[1], x[0]), reverse=True)[:TOP_K]
        if len(chosen) < TOP_K:
            continue
        per_stock_capital = capital / TOP_K
        pnl = 0.0
        for symbol, _ in chosen:
            if row["participation"][symbol] > MAX_PARTICIPATION:
                continue
            t = cost_trade(per_stock_capital, row["close"][symbol], row["next_open"][symbol], slippage)
            pnl += t["pnl"]
            for k in ("brokerage", "exchange", "sebi", "stt", "stamp", "gst", "dp"):
                cost_total[k] += t[k]
            participation.append(row["participation"][symbol])
        net = pnl / capital if capital > 0 else -1.0
        capital = max(0.0, capital + pnl)
        path.append({"day": row["day"], "fold": row["fold"], "net_return": net})

    arr = np.asarray([x["net_return"] for x in path], dtype=float)
    curve = CAPITAL * np.cumprod(np.r_[1.0, 1.0 + arr])
    dd = curve / np.maximum.accumulate(curve) - 1.0
    return {
        "net_total_return": float(capital / CAPITAL - 1.0),
        "mean_daily_return": float(arr.mean()) if len(arr) else math.nan,
        "max_drawdown": float(dd.min()) if len(dd) else math.nan,
        "period_count": len(path),
        "mean_participation": float(np.mean(participation)) if participation else math.nan,
        "max_participation": float(np.max(participation)) if participation else math.nan,
        "costs": dict(cost_total),
        "path": path,
    }


def block_signflip(diffs, block_size=5, reps=10000, seed=20260921):
    diffs = np.asarray(diffs, dtype=float)
    blocks = [diffs[i:i+block_size] for i in range(0, len(diffs), block_size) if len(diffs[i:i+block_size]) == block_size]
    if not blocks:
        return math.nan
    b = np.asarray([x.mean() for x in blocks])
    observed = float(b.mean())
    rng = np.random.default_rng(seed)
    signs = rng.choice(np.array([-1.0, 1.0]), size=(reps, len(b)))
    return float(np.mean((signs * b).mean(axis=1) >= observed - 1e-15))


def bh(pvals):
    ordered = sorted(pvals.items(), key=lambda x: x[1])
    m = len(ordered)
    out = {}
    running = 1.0
    for rank, (name, p) in reversed(list(enumerate(ordered, 1))):
        running = min(running, p * m / rank)
        out[name] = running
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--zip", required=True)
    ap.add_argument("--global-dir", required=True)
    ap.add_argument("--actions-dir", required=True)
    ap.add_argument("--fii-dii", default="")
    ap.add_argument("--output", default="p4b_btst_results")
    args = ap.parse_args()

    digest = sha256_file(Path(args.zip))
    if digest != SOURCE_SHA256:
        raise SystemExit(f"minute-release SHA-256 mismatch: {digest}")

    global_dir = Path(args.global_dir)
    actions_dir = Path(args.actions_dir)
    feature_maps = load_global_feature_maps(global_dir)
    flow_map, flow_status = find_header_and_parse_flow(Path(args.fii_dii)) if args.fii_dii else ({}, {"parsed": False, "reason": "not supplied"})

    with zipfile.ZipFile(args.zip) as zf:
        sessions = {s: read_stock_sessions(zf, s) for s in SYMBOLS}

    common = set.intersection(*(set(sessions[s]) for s in SYMBOLS))
    common_days = sorted(d for d in common if d <= END_DATE)
    if len(common_days) < 300:
        raise SystemExit(f"too few common sessions: {len(common_days)}")

    actions = {s: load_corporate_actions(actions_dir, s) for s in SYMBOLS}
    stock = build_stock_daily(sessions, common_days, actions)
    folds = fold_indices(common_days)

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    rows = []
    for variant in ("univariate", "global"):
        tasks = []
        for fold, idxs in folds.items():
            for idx in idxs:
                usable = []
                contexts = []
                covars = []
                for s in SYMBOLS:
                    if not eligible_origin(common_days, stock[s], idx):
                        continue
                    trailing = stock[s]["value"][max(0, idx-20):idx]
                    trailing = trailing[np.isfinite(trailing)]
                    median_value = float(np.median(trailing)) if len(trailing) else 0.0
                    participation = (CAPITAL / TOP_K) / max(median_value, 1.0)
                    if participation > MAX_PARTICIPATION:
                        continue
                    target_slice = stock[s]["overnight"][idx-CONTEXT+1:idx+1]
                    level = np.cumsum(target_slice)
                    level = level - level[0]
                    contexts.append(level.astype(np.float32))
                    if variant == "global":
                        covars.append(
                            make_covariate_matrix(
                                common_days,
                                stock,
                                feature_maps,
                                flow_map,
                                False,
                                idx,
                                s,
                            )
                        )
                    usable.append((s, participation))
                if len(usable) >= TOP_K:
                    tasks.append((fold, idx, usable, contexts, covars))

        for offset in range(0, len(tasks), MODEL_ORIGINS_PER_BATCH):
            chunk = tasks[offset:offset + MODEL_ORIGINS_PER_BATCH]
            all_contexts = []
            all_covars = []
            spans = []
            for fold, idx, usable, contexts, covars in chunk:
                start = len(all_contexts)
                all_contexts.extend(contexts)
                all_covars.extend(covars)
                spans.append((fold, idx, usable, start))
            if variant == "global":
                outputs = model.predict_batch(
                    all_contexts,
                    horizon=1,
                    past_only_covariates=all_covars,
                    return_quantiles=False,
                    univariate=True,
                )
            else:
                outputs = model.predict_batch(
                    all_contexts,
                    horizon=1,
                    return_quantiles=False,
                    univariate=True,
                )

            for fold, idx, usable, start in spans:
                signal_day = common_days[idx]
                next_day = common_days[idx + 1]
                tf_scores = {}
                ewma_scores = {}
                future = {}
                next_open = {}
                close = {}
                participation = {}
                for j, (s, part) in enumerate(usable):
                    y_hist = stock[s]["overnight"][idx-EWMA_SPAN+1:idx+1]
                    ewma = 0.0
                    weight_sum = 0.0
                    weight = 1.0
                    for y in y_hist[::-1]:
                        ewma = ewma + weight * float(y)
                        weight_sum += weight
                        weight *= (1.0 - EWMA_ALPHA)
                    ewma /= max(weight_sum, 1e-12)

                    pred_level = float(np.asarray(outputs[start+j].forecast).reshape(-1)[0])
                    context_last = float(all_contexts[start+j][-1])
                    pred = pred_level - context_last
                    tf_scores[s] = pred
                    ewma_scores[s] = ewma
                    close[s] = stock[s]["close"][idx]
                    next_open[s] = stock[s]["open"][idx + 1]
                    future[s] = float(stock[s]["overnight"][idx + 1])
                    participation[s] = part

                rows.append({
                    "fold": fold,
                    "day": signal_day,
                    "next_day": next_day,
                    "variant": variant,
                    "timesfm": tf_scores,
                    "control": ewma_scores,
                    "future": future,
                    "close": close,
                    "next_open": next_open,
                    "participation": participation,
                })

    forecast_summary = []
    for variant in ("univariate", "global"):
        for h in (variant,):
            vals = [r for r in rows if r["variant"] == variant]
            y = []
            p = []
            ics = []
            for r in vals:
                for s in r["future"]:
                    y.append(r["future"][s])
                    p.append(r["timesfm"][s])
                syms = list(r["future"])
                if len(syms) >= 2:
                    a = np.asarray([r["timesfm"][s] for s in syms])
                    b = np.asarray([r["future"][s] for s in syms])
                    ics.append(float(np.corrcoef(np.argsort(np.argsort(a)), np.argsort(np.argsort(b)))[0,1]))
            y = np.asarray(y)
            p = np.asarray(p)
            acc = float(np.mean((p > 0) == (y > 0)))
            base = float(np.mean(y > 0))
            forecast_summary.append({
                "variant": variant,
                "observations": int(len(y)),
                "mae": float(np.mean(np.abs(y - p))),
                "persistence_mae": float(np.mean(np.abs(y))),
                "directional_accuracy": acc,
                "positive_return_base_rate": base,
                "directional_excess_pp": 100.0 * (acc - base),
                "mean_cross_sectional_rank_ic": float(np.nanmean(ics)) if ics else math.nan,
            })

    strategy_results = []
    for variant in ("univariate", "global"):
        variant_rows = [r for r in rows if r["variant"] == variant]
        for strategy in ("timesfm", "control"):
            for slip in SLIPPAGE_STRESSES:
                sim = simulate(variant_rows, strategy, slip)
                fold_returns = []
                for fold in range(1, FOLDS + 1):
                    fp = [r for r in variant_rows if r["fold"] == fold]
                    fold_returns.append(simulate(fp, strategy, slip)["net_total_return"])
                strategy_results.append({
                    "variant": variant,
                    "strategy": strategy,
                    "slippage_rate": slip,
                    "net_total_return": sim["net_total_return"],
                    "max_drawdown": sim["max_drawdown"],
                    "period_count": sim["period_count"],
                    "mean_participation": sim["mean_participation"],
                    "max_participation": sim["max_participation"],
                    "costs": sim["costs"],
                    "fold_returns": fold_returns,
                })

    primary_p = {}
    for variant in ("univariate", "global"):
        vp = [r for r in rows if r["variant"] == variant and r["fold"] in DEV_FOLDS]
        t_periods = simulate(vp, "timesfm", PRIMARY_SLIPPAGE)["path"]
        c_periods = simulate(vp, "control", PRIMARY_SLIPPAGE)["path"]
        diffs = np.asarray([a["net_return"] - b["net_return"] for a, b in zip(t_periods, c_periods)], dtype=float)
        primary_p[variant] = block_signflip(diffs, block_size=5)

    qvals = bh(primary_p)
    candidates = []
    for variant in ("univariate", "global"):
        t = next(x for x in strategy_results if x["variant"] == variant and x["strategy"] == "timesfm" and abs(x["slippage_rate"] - PRIMARY_SLIPPAGE) < 1e-12)
        c = next(x for x in strategy_results if x["variant"] == variant and x["strategy"] == "control" and abs(x["slippage_rate"] - PRIMARY_SLIPPAGE) < 1e-12)
        fold_ok = all(t["fold_returns"][f-1] > c["fold_returns"][f-1] and t["fold_returns"][f-1] > 0 for f in DEV_FOLDS)
        q_ok = qvals[variant] < 0.10
        capacity_ok = t["max_participation"] <= MAX_PARTICIPATION
        if fold_ok and q_ok and capacity_ok:
            candidates.append(variant)

    holdout = []
    for variant in candidates:
        for slip in SLIPPAGE_STRESSES:
            t = next(x for x in strategy_results if x["variant"] == variant and x["strategy"] == "timesfm" and abs(x["slippage_rate"] - slip) < 1e-12)
            c = next(x for x in strategy_results if x["variant"] == variant and x["strategy"] == "control" and abs(x["slippage_rate"] - slip) < 1e-12)
            holdout.append({
                "variant": variant,
                "slippage_rate": slip,
                "timesfm_holdout_return": t["fold_returns"][HOLDOUT_FOLD-1],
                "control_holdout_return": c["fold_returns"][HOLDOUT_FOLD-1],
                "timesfm_ahead": t["fold_returns"][HOLDOUT_FOLD-1] > c["fold_returns"][HOLDOUT_FOLD-1],
            })

    output = {
        "lane": "phase4b_btst_overnight",
        "model": "timesfm-3.0-pytorch",
        "source_release_sha256": digest,
        "external_global_commit": EXTERNAL_COMMIT,
        "common_end_date": END_DATE,
        "symbols": list(SYMBOLS),
        "context_days": CONTEXT,
        "top_k": TOP_K,
        "folds": FOLDS,
        "development_slippage": PRIMARY_SLIPPAGE,
        "slippage_stresses": list(SLIPPAGE_STRESSES),
        "corporate_action_exclusions": {s: len(actions[s]) for s in SYMBOLS},
        "fii_dii_status": flow_status,
        "forecast_summary": forecast_summary,
        "strategy_results": strategy_results,
        "development_block_p": primary_p,
        "development_bh_q": qvals,
        "development_candidates": candidates,
        "holdout_results": holdout,
        "status": "candidate_holdout_required" if candidates else "no_btst_cell_passed_development",
        "note": "BTST target is close-to-next-open. Global covariates are timestamp-safe at the 15:30 IST signal cutoff. FII/DII parsing is a secondary sensitivity only and does not enter the promotion family.",
    }

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "origin_rows.jsonl").open("w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    (out / "summary.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))

    if not rows:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
