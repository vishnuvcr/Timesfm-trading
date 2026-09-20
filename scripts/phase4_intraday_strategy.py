from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import math
import zipfile
from collections import defaultdict
from datetime import datetime, timezone, timedelta
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter

SYMBOLS = ("RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","SBIN","ITC","BHARTIARTL","LT","AXISBANK")
HORIZONS = (15, 30, 60)
CONTEXT = 128
TOP_K = 3
FOLDS = 4
ORIGINS_PER_FOLD = 40
MIN_ORIGIN_MINUTE = 30
LAST_EXIT_MINUTE = 359
CAPITAL = 1_000_000.0
EXTRA_SLIPPAGE = (0.0, 0.00025, 0.00050, 0.0010, 0.0020)
PRIMARY_DEV_SLIPPAGE = 0.0010
BROKERAGE_PER_EXECUTION = 20.0
NSE_CASH_PER_SIDE = 307.0 / 1e7
SEBI_PER_SIDE = 10.0 / 1e7
STT_INTRADAY_SELL = 0.00025
STAMP_BUY = 0.00003
GST = 0.18
IST = timezone(timedelta(hours=5, minutes=30))
SOURCE_SHA256 = "20024713c455cc16b5daae91e06991d57a1acfa6a30c77bb7d5a742ee1789ab2"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

def parse_time(v: str) -> datetime:
    return datetime.fromtimestamp(int(v), tz=timezone.utc).astimezone(IST)

def read_symbol(zf: zipfile.ZipFile, symbol: str):
    target = f"{symbol}_1m.csv.gz"
    names = [n for n in zf.namelist() if n == target or n.endswith("/" + target) or n.endswith(target)]
    if not names:
        raise RuntimeError(f"{symbol}: release file missing")
    import io
    rows = []
    with zf.open(names[0], "r") as raw:
        with gzip.GzipFile(fileobj=raw) as gz:
            text = gz.read().decode("utf-8")
    for row in csv.DictReader(io.StringIO(text)):
        t = parse_time(row["time"])
        minutes = t.hour * 60 + t.minute
        if 9 * 60 + 15 <= minutes <= 15 * 60 + 29:
            o = float(row["open"])
            h = float(row["high"])
            l = float(row["low"])
            c = float(row["close"])
            rows.append({
                "time": int(row["time"]),
                "day": t.date().isoformat(),
                "minute": minutes - (9 * 60 + 15),
                "open": o,
                "close": c,
                "volume": float(row.get("Volume", 0) or 0),
                "valid": bool(o > 0 and h > 0 and l > 0 and c > 0 and l <= min(o, c) <= max(o, c) <= h),
            })
    return rows

def build_complete_sessions(rows):
    by_day = defaultdict(list)
    for r in rows:
        by_day[r["day"]].append(r)
    sessions = {}
    for day, vals in sorted(by_day.items()):
        vals.sort(key=lambda x: x["time"])
        if len(vals) != 375 or vals[0]["minute"] != 0 or vals[-1]["minute"] != 374:
            continue
        sessions[day] = vals
    return sessions

def session_vwap(vals):
    close = np.asarray([r["close"] for r in vals], dtype=np.float64)
    vol = np.asarray([max(0.0, r["volume"]) for r in vals], dtype=np.float64)
    pv = np.cumsum(close * vol)
    vv = np.cumsum(vol)
    return np.divide(pv, vv, out=close.copy(), where=vv > 0).astype(np.float32)

def build_common_data(all_sessions):
    common = None
    for symbol in SYMBOLS:
        days = set(all_sessions[symbol].keys())
        common = days if common is None else common & days
    common_days = sorted(common)
    data = {}
    for symbol in SYMBOLS:
        log_close = []
        opens = []
        vwap = []
        valid = []
        volume = []
        day_start = {}
        offset = 0
        for day in common_days:
            vals = all_sessions[symbol][day]
            day_start[day] = offset
            log_close.extend(math.log(r["close"]) for r in vals)
            opens.extend(r["open"] for r in vals)
            vwap.extend(session_vwap(vals))
            valid.extend(r["valid"] for r in vals)
            volume.extend(r["volume"] for r in vals)
            offset += 375
        data[symbol] = {
            "log_close": np.asarray(log_close, dtype=np.float32),
            "open": np.asarray(opens, dtype=np.float32),
            "vwap": np.asarray(vwap, dtype=np.float32),
            "valid": np.asarray(valid, dtype=bool),
            "volume": np.asarray(volume, dtype=np.float32),
        }
    return common_days, data

def select_origins(common_days, horizon):
    fold_edges = np.linspace(0, len(common_days), FOLDS + 1, dtype=int)
    selected = {}
    day_pos = {d: i for i, d in enumerate(common_days)}
    for fold in range(1, FOLDS + 1):
        days = common_days[fold_edges[fold-1]:fold_edges[fold]]
        candidates = []
        for day in days:
            di = day_pos[day]
            for minute in range(MIN_ORIGIN_MINUTE, LAST_EXIT_MINUTE - horizon + 1, horizon):
                candidates.append((di, minute))
        if len(candidates) < ORIGINS_PER_FOLD:
            raise RuntimeError(f"horizon={horizon} fold={fold} has only {len(candidates)} eligible origins")
        picks = np.linspace(0, len(candidates) - 1, ORIGINS_PER_FOLD, dtype=int)
        selected[fold] = [candidates[i] for i in np.unique(picks)]
    return selected

def rank_ic(a, b):
    if len(a) < 2 or np.std(a) == 0 or np.std(b) == 0:
        return float("nan")
    ra = np.argsort(np.argsort(a))
    rb = np.argsort(np.argsort(b))
    return float(np.corrcoef(ra, rb)[0, 1])

def cost_components(buy_notional, sell_notional, n_buy, n_sell, slippage):
    turnover = buy_notional + sell_notional
    brokerage = (n_buy + n_sell) * BROKERAGE_PER_EXECUTION
    exchange = turnover * NSE_CASH_PER_SIDE
    sebi = turnover * SEBI_PER_SIDE
    stt = sell_notional * STT_INTRADAY_SELL
    stamp = buy_notional * STAMP_BUY
    gst = GST * (brokerage + exchange + sebi)
    slip = turnover * slippage
    total = brokerage + exchange + sebi + stt + stamp + gst + slip
    return {
        "brokerage": brokerage,
        "exchange": exchange,
        "sebi": sebi,
        "stt": stt,
        "stamp": stamp,
        "gst": gst,
        "slippage": slip,
        "total": total,
    }

def simulate(periods, score_key, slippage):
    capital = CAPITAL
    out = []
    for row in periods:
        scores = row[score_key]
        ranked = sorted(scores.items(), key=lambda x: (x[1], x[0]), reverse=True)
        chosen = [s for s, _ in ranked[:TOP_K]]
        gross = float(np.mean([row["realized_return"][s] for s in chosen]))
        buy = capital
        sell = capital
        costs = cost_components(buy, sell, TOP_K, TOP_K, slippage)
        net = (gross * capital - costs["total"]) / capital
        participation = max(row["participation_60m"].get(s, 0.0) for s in chosen)
        capital *= max(0.0, 1.0 + net)
        out.append({
            "day": row["day"],
            "fold": row["fold"],
            "horizon": row["horizon"],
            "gross_return": gross,
            "net_return": net,
            "cost_total": costs["total"],
            "costs": costs,
            "participation": participation,
        })
    total = capital / CAPITAL - 1.0
    arr = np.asarray([x["net_return"] for x in out], dtype=float)
    curve = CAPITAL * np.cumprod(np.r_[1.0, 1.0 + arr])
    dd = curve / np.maximum.accumulate(curve) - 1.0
    return {
        "net_total_return": float(total),
        "mean_period_return": float(np.mean(arr)) if len(arr) else math.nan,
        "max_drawdown": float(np.min(dd)) if len(dd) else math.nan,
        "period_count": len(out),
        "mean_turnover_fraction": 2.0,
        "max_participation": float(max((x["participation"] for x in out), default=0.0)),
        "periods": out,
    }

def block_signflip(diffs, block_size=5, reps=10000, seed=20260920):
    diffs = np.asarray(diffs, dtype=float)
    blocks = [diffs[i:i+block_size] for i in range(0, len(diffs), block_size) if len(diffs[i:i+block_size]) == block_size]
    if not blocks:
        return math.nan
    b = np.asarray([x.mean() for x in blocks])
    obs = float(b.mean())
    rng = np.random.default_rng(seed)
    signs = rng.choice(np.array([-1.0, 1.0]), size=(reps, len(b)))
    return float(np.mean((signs * b).mean(axis=1) >= obs - 1e-15))

def benjamini_hochberg(pvals):
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
    ap.add_argument("--output", default="p4_intraday_strategy_results")
    args = ap.parse_args()

    digest = sha256_file(Path(args.zip))
    if digest != SOURCE_SHA256:
        raise SystemExit(f"release SHA-256 mismatch: {digest}")

    with zipfile.ZipFile(args.zip) as zf:
        sessions = {s: build_complete_sessions(read_symbol(zf, s)) for s in SYMBOLS}
    common_days, data = build_common_data(sessions)

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    forecast_rows = []
    periods_by_horizon = {h: [] for h in HORIZONS}
    for horizon in HORIZONS:
        origins_by_fold = select_origins(common_days, horizon)
        for fold, origins in origins_by_fold.items():
            for day_idx, minute in origins:
                base = day_idx * 375 + minute
                contexts = []
                usable = []
                for symbol in SYMBOLS:
                    start = base - CONTEXT
                    if start < 0 or base + horizon >= (day_idx + 1) * 375:
                        continue
                    if not data[symbol]["valid"][start:base].all():
                        continue
                    contexts.append(data[symbol]["log_close"][start:base])
                    usable.append(symbol)
                if len(usable) < TOP_K:
                    continue

                outputs = model.predict_batch(
                    contexts,
                    horizon=max(HORIZONS),
                    return_quantiles=False,
                    univariate=True,
                )
                tf_score = {}
                vwap_score = {}
                future_log = {}
                realized = {}
                participation = {}

                for j, symbol in enumerate(usable):
                    pred = float(np.asarray(outputs[j].forecast).reshape(-1)[horizon-1] - contexts[j][-1])
                    idx_entry = base + 1
                    idx_exit = base + horizon
                    future = float(data[symbol]["log_close"][idx_exit] - data[symbol]["log_close"][base])
                    entry = float(data[symbol]["open"][idx_entry])
                    exit_price = float(np.exp(data[symbol]["log_close"][idx_exit]))
                    realized_return = exit_price / entry - 1.0
                    vwap = float(data[symbol]["vwap"][base])
                    price = float(np.exp(data[symbol]["log_close"][base]))
                    trailing_value = float(np.mean(
                        np.exp(data[symbol]["log_close"][max(0, base-60):base])
                        * data[symbol]["volume"][max(0, base-60):base]
                    ))
                    trade_value = CAPITAL / TOP_K
                    participation_ratio = trade_value / max(trailing_value, 1.0)
                    tf_score[symbol] = pred
                    vwap_score[symbol] = price / vwap - 1.0 if vwap > 0 else 0.0
                    future_log[symbol] = future
                    realized[symbol] = realized_return
                    participation[symbol] = participation_ratio
                    forecast_rows.append({
                        "fold": fold,
                        "day": common_days[day_idx],
                        "minute": minute,
                        "horizon": horizon,
                        "symbol": symbol,
                        "timesfm_forecast_return": pred,
                        "future_log_return": future,
                        "realized_execution_return": realized_return,
                        "vwap_score": vwap_score[symbol],
                    })

                periods_by_horizon[horizon].append({
                    "fold": fold,
                    "day": common_days[day_idx],
                    "horizon": horizon,
                    "timesfm": tf_score,
                    "vwap": vwap_score,
                    "future_log_return": future_log,
                    "realized_return": realized,
                    "participation_60m": participation,
                })

    forecast_summary = []
    for horizon in HORIZONS:
        rows = [r for r in forecast_rows if r["horizon"] == horizon]
        y = np.asarray([r["future_log_return"] for r in rows], dtype=float)
        p = np.asarray([r["timesfm_forecast_return"] for r in rows], dtype=float)
        ics = []
        by_origin = defaultdict(list)
        for r in rows:
            by_origin[(r["fold"], r["day"], r["minute"])].append(r)
        for obs in by_origin.values():
            ics.append(rank_ic(
                np.asarray([x["timesfm_forecast_return"] for x in obs]),
                np.asarray([x["future_log_return"] for x in obs]),
            ))
        acc = float(np.mean((p > 0) == (y > 0))) if len(y) else math.nan
        base = float(np.mean(y > 0)) if len(y) else math.nan
        forecast_summary.append({
            "horizon": horizon,
            "stock_observations": len(rows),
            "origin_count": len(by_origin),
            "timesfm_mae": float(np.mean(np.abs(y-p))) if len(y) else math.nan,
            "persistence_mae": float(np.mean(np.abs(y))) if len(y) else math.nan,
            "directional_accuracy": acc,
            "positive_return_base_rate": base,
            "directional_excess_pp": 100.0 * (acc-base) if len(y) else math.nan,
            "mean_cross_sectional_rank_ic": float(np.nanmean(ics)) if ics else math.nan,
        })

    strategy_results = []
    for horizon in HORIZONS:
        periods = periods_by_horizon[horizon]
        for strategy in ("timesfm", "vwap"):
            for slippage in EXTRA_SLIPPAGE:
                sim = simulate(periods, strategy, slippage)
                fold_returns = []
                for fold in range(1, FOLDS+1):
                    fold_periods = [p for p in periods if p["fold"] == fold]
                    fold_returns.append(simulate(fold_periods, strategy, slippage)["net_total_return"])
                strategy_results.append({
                    "horizon": horizon,
                    "strategy": strategy,
                    "slippage_rate": slippage,
                    "net_total_return": sim["net_total_return"],
                    "max_drawdown": sim["max_drawdown"],
                    "mean_period_return": sim["mean_period_return"],
                    "period_count": sim["period_count"],
                    "mean_turnover_fraction": sim["mean_turnover_fraction"],
                    "max_participation": sim["max_participation"],
                    "fold_returns": fold_returns,
                })

    dev_p = {}
    for horizon in HORIZONS:
        t_periods = [p for p in periods_by_horizon[horizon] if p["fold"] in (1,2,3)]
        t10 = simulate(t_periods, "timesfm", PRIMARY_DEV_SLIPPAGE)["periods"]
        v10 = simulate(t_periods, "vwap", PRIMARY_DEV_SLIPPAGE)["periods"]
        diffs = np.asarray([a["net_return"] - b["net_return"] for a,b in zip(t10,v10)], dtype=float)
        dev_p[str(horizon)] = block_signflip(diffs)

    dev_q = benjamini_hochberg(dev_p)
    candidates = []
    for horizon in HORIZONS:
        t = next(x for x in strategy_results if x["horizon"] == horizon and x["strategy"] == "timesfm" and abs(x["slippage_rate"]-PRIMARY_DEV_SLIPPAGE)<1e-12)
        v = next(x for x in strategy_results if x["horizon"] == horizon and x["strategy"] == "vwap" and abs(x["slippage_rate"]-PRIMARY_DEV_SLIPPAGE)<1e-12)
        fold_ok = all(t["fold_returns"][i] > v["fold_returns"][i] and t["fold_returns"][i] > 0 for i in range(3))
        if fold_ok and dev_q[str(horizon)] < 0.10:
            candidates.append(horizon)

    holdout = []
    for horizon in candidates:
        for slippage in EXTRA_SLIPPAGE:
            t = next(x for x in strategy_results if x["horizon"] == horizon and x["strategy"] == "timesfm" and abs(x["slippage_rate"]-slippage)<1e-12)
            v = next(x for x in strategy_results if x["horizon"] == horizon and x["strategy"] == "vwap" and abs(x["slippage_rate"]-slippage)<1e-12)
            holdout.append({
                "horizon": horizon,
                "slippage_rate": slippage,
                "timesfm_holdout_return": t["fold_returns"][3],
                "vwap_holdout_return": v["fold_returns"][3],
                "timesfm_ahead_of_vwap": t["fold_returns"][3] > v["fold_returns"][3],
            })

    output = {
        "lane": "phase4_intraday_timesfm_vwap",
        "model": "timesfm-3.0-pytorch",
        "source_release_sha256": digest,
        "symbols": list(SYMBOLS),
        "horizons": list(HORIZONS),
        "context": CONTEXT,
        "top_k": TOP_K,
        "folds": FOLDS,
        "origins_per_fold": ORIGINS_PER_FOLD,
        "extra_slippage": list(EXTRA_SLIPPAGE),
        "primary_development_slippage": PRIMARY_DEV_SLIPPAGE,
        "development_block_p": dev_p,
        "development_bh_q": dev_q,
        "development_candidates": candidates,
        "forecast_summary": forecast_summary,
        "strategy_results": strategy_results,
        "holdout_results": holdout,
        "status": "candidate_holdout_required" if candidates else "no_intraday_cell_passed_development",
        "note": "Exploratory non-executing research. Development folds 1-3 determine holdout eligibility; fold 4 is not used in candidate selection.",
    }

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "forecast_rows.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=forecast_rows[0].keys())
        w.writeheader()
        w.writerows(forecast_rows)
    (out / "summary.json").write_text(json.dumps(output, indent=2) + "\n")
    print(json.dumps(output, indent=2))

    if not periods_by_horizon[HORIZONS[0]]:
        raise SystemExit(1)

if __name__ == "__main__":
    main()
