from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter

CONTEXT = 128
LOOKBACK = 20
HORIZON = 10
REBALANCE_STEP = 10
TOP_K = 6
INITIAL_CAPITAL = 1_000_000.0
BROKERAGE_INR = 20.0
DP_SELL_INR = 13.5
GST = 0.18
EXCHANGE_RATE = 307.0 / 10_000_000.0
SEBI_RATE = 10.0 / 10_000_000.0
STT_DELIVERY_RATE = 0.001
STAMP_BUY_RATE = 0.00015
SLIPPAGE_STRESSES = (0.0, 0.00125, 0.0025, 0.00375, 0.0050)
START_DATE = date(2023, 1, 1)
BLOCK_SIZE = 5
BOOTSTRAP_REPS = 10000

SYMBOLS = (
    "RELIANCE", "TCS", "HDFCBANK", "INFY", "ICICIBANK", "SBIN", "ITC",
    "BHARTIARTL", "LT", "AXISBANK", "KOTAKBANK", "HINDUNILVR", "MARUTI",
    "SUNPHARMA", "BAJFINANCE", "ASIANPAINT", "TITAN", "HCLTECH", "WIPRO",
    "ULTRACEMCO", "NESTLEIND", "M&M", "NTPC", "ONGC", "POWERGRID",
    "TATAMOTORS", "TATASTEEL", "ADANIENT", "CIPLA", "DRREDDY",
)


@dataclass
class Series:
    dates: list[str]
    log_close: np.ndarray
    turnover: np.ndarray


def load_series(adjusted_path: Path, raw_path: Path) -> Series:
    adj_dates, values = [], []
    with adjusted_path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            adj_dates.append(row["date"][:10])
            values.append(float(row["adj_close"]))
    raw = {}
    with raw_path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            raw[row["date"][:10]] = float(row["turnover"])
    if adj_dates != sorted(adj_dates) or len(adj_dates) != len(set(adj_dates)):
        raise RuntimeError(f"{adjusted_path}: dates are not sorted/unique")
    turnovers = [raw.get(d, float("nan")) for d in adj_dates]
    return Series(adj_dates, np.log(np.asarray(values, dtype=np.float32)),
                  np.asarray(turnovers, dtype=float))


def load_pit(path: Path) -> dict[str, list[tuple[date, date]]]:
    spans: dict[str, list[tuple[date, date]]] = {}
    with path.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            if row.get("exchange") != "NSE":
                continue
            symbol = row["symbol"].upper()
            if symbol not in SYMBOLS:
                continue
            spans.setdefault(symbol, []).append((
                date.fromisoformat(row["rebalance_date"][:10]),
                date.fromisoformat(row["valid_to"][:10]),
            ))
    for symbol in spans:
        spans[symbol].sort()
    return spans


def pit_eligible(spans: dict[str, list[tuple[date, date]]], day: str) -> set[str]:
    d = date.fromisoformat(day[:10])
    out = set()
    for symbol, intervals in spans.items():
        if any(a <= d <= b for a, b in intervals):
            out.add(symbol)
    return out


def top_k(scores: dict[str, float], k: int = TOP_K) -> dict[str, float]:
    ranked = sorted(scores.items(), key=lambda x: (x[1], x[0]), reverse=True)
    chosen = ranked[: min(k, len(ranked))]
    if not chosen:
        return {}
    w = 1.0 / len(chosen)
    return {symbol: w for symbol, _ in chosen}


def mean_return(signal_rows: list[dict]) -> dict:
    arr = np.asarray([r["future_log_return"] for r in signal_rows], dtype=float)
    tf = np.asarray([r["timesfm_forecast_return"] for r in signal_rows], dtype=float)
    return {
        "n_stock_observations": int(arr.size),
        "timesfm_return_mae": float(np.mean(np.abs(arr - tf))),
        "persistence_return_mae": float(np.mean(np.abs(arr))),
        "timesfm_directional_excess_pp": float(
            100.0 * (np.mean((tf > 0) == (arr > 0)) - np.mean(arr > 0))
        ),
    }


def execution_cost(trades: list[tuple[str, str, float]], slippage_rate: float) -> dict:
    totals = defaultdict(float)
    for side, symbol, notional in trades:
        exchange = notional * EXCHANGE_RATE
        sebi = notional * SEBI_RATE
        brokerage = BROKERAGE_INR
        stt = notional * STT_DELIVERY_RATE
        stamp = notional * STAMP_BUY_RATE if side == "buy" else 0.0
        dp = DP_SELL_INR if side == "sell" else 0.0
        gst = GST * (brokerage + exchange + sebi)
        slip = notional * slippage_rate
        totals["brokerage_inr"] += brokerage
        totals["exchange_inr"] += exchange
        totals["sebi_inr"] += sebi
        totals["stt_inr"] += stt
        totals["stamp_inr"] += stamp
        totals["dp_inr"] += dp
        totals["gst_inr"] += gst
        totals["slippage_inr"] += slip
    totals["total_inr"] = sum(totals.values())
    return dict(totals)


def simulate(signal_rows: list[dict], strategy_key: str, slippage_rate: float) -> tuple[dict, list[dict], list[dict]]:
    by_date: dict[str, list[dict]] = defaultdict(list)
    for row in signal_rows:
        by_date[row["date"]].append(row)

    equity = INITIAL_CAPITAL
    positions: dict[str, float] = {}
    period_records = []
    cost_records = []
    for day in sorted(by_date):
        rows = by_date[day]
        target_scores = {r["symbol"]: float(r[strategy_key]) for r in rows}
        target_weights = top_k(target_scores)

        eligible = {r["symbol"]: r for r in rows}
        target_values = {s: equity * w for s, w in target_weights.items()}
        all_symbols = set(positions) | set(target_values)
        trades = []
        max_participation = 0.0
        for symbol in sorted(all_symbols):
            current = float(positions.get(symbol, 0.0))
            target = float(target_values.get(symbol, 0.0))
            delta = target - current
            if abs(delta) < 1e-8:
                continue
            side = "buy" if delta > 0 else "sell"
            notional = abs(delta)
            turnover_row = eligible.get(symbol)
            if turnover_row is not None:
                avg_turnover = float(turnover_row["avg_turnover_63d"])
                if np.isfinite(avg_turnover) and avg_turnover > 0:
                    max_participation = max(max_participation, notional / avg_turnover)
            trades.append((side, symbol, notional))

        costs = execution_cost(trades, slippage_rate)
        cost_total = float(costs["total_inr"])
        post_cost_equity = max(0.0, equity - cost_total)
        positions = {s: post_cost_equity * w for s, w in target_weights.items()}

        gross_positions = {}
        for symbol, value in positions.items():
            row = eligible[symbol]
            gross_positions[symbol] = value * float(np.exp(row["future_log_return"]))
        gross_equity = float(sum(gross_positions.values()))
        net_period_return = gross_equity / equity - 1.0 if equity > 0 else -1.0
        gross_period_return = (sum(
            target_values[s] * float(np.exp(eligible[s]["future_log_return"]))
            for s in target_weights
        ) / equity - 1.0) if equity > 0 else -1.0
        period_records.append({
            "date": day,
            "year": int(day[:4]),
            "strategy": strategy_key,
            "gross_period_return": gross_period_return,
            "net_period_return": net_period_return,
            "cost_inr": cost_total,
            "turnover_inr": float(sum(t[2] for t in trades)),
            "max_participation": max_participation,
            "n_selected": len(target_weights),
            "regime": rows[0]["regime"],
        })
        cost_records.append(costs)
        positions = gross_positions
        equity = gross_equity

    # Explicit end-of-holdout liquidation.
    liq_trades = [("sell", s, v) for s, v in positions.items() if v > 1e-8]
    liq_costs = execution_cost(liq_trades, slippage_rate)
    final_equity = max(0.0, equity - liq_costs["total_inr"])

    eq_curve = [INITIAL_CAPITAL]
    running = INITIAL_CAPITAL
    for rec in period_records:
        running *= 1.0 + rec["net_period_return"]
        eq_curve.append(running)
    eq_curve.append(final_equity)
    curve = np.asarray(eq_curve)
    drawdown = curve / np.maximum.accumulate(curve) - 1.0
    periods_per_year = 252.0 / HORIZON
    period_returns = np.asarray([r["net_period_return"] for r in period_records], dtype=float)
    sharpe = float(
        np.mean(period_returns) / np.std(period_returns, ddof=1) * np.sqrt(periods_per_year)
    ) if len(period_returns) > 1 and np.std(period_returns, ddof=1) > 0 else float("nan")
    total_costs = defaultdict(float)
    for rec in cost_records:
        for k, v in rec.items():
            total_costs[k] += float(v)
    for k, v in liq_costs.items():
        total_costs[k] += float(v)

    return {
        "strategy": strategy_key,
        "slippage_rate": slippage_rate,
        "initial_capital": INITIAL_CAPITAL,
        "final_equity": final_equity,
        "net_total_return": final_equity / INITIAL_CAPITAL - 1.0,
        "net_mean_period_return": float(np.mean(period_returns)),
        "net_sharpe_periodized": sharpe,
        "max_drawdown": float(np.min(drawdown)),
        "periods": len(period_records),
        "mean_turnover_fraction": float(np.mean([r["turnover_inr"] / max(INITIAL_CAPITAL, 1.0) for r in period_records])),
        "max_participation": float(max(r["max_participation"] for r in period_records) if period_records else 0.0),
        "total_costs": dict(total_costs),
    }, period_records, cost_records


def block_signflip_pvalue(diffs: np.ndarray, block_size: int = BLOCK_SIZE, reps: int = BOOTSTRAP_REPS) -> float:
    diffs = np.asarray(diffs, dtype=float)
    if len(diffs) < block_size:
        return float("nan")
    blocks = [diffs[i:i+block_size] for i in range(0, len(diffs), block_size)]
    block_means = np.asarray([np.mean(x) for x in blocks if len(x) == block_size], dtype=float)
    if len(block_means) == 0:
        return float("nan")
    observed = float(np.mean(block_means))
    rng = np.random.default_rng(20260920)
    signs = rng.choice(np.array([-1.0, 1.0]), size=(reps, len(block_means)))
    null_means = (signs * block_means[None, :]).mean(axis=1)
    return float(np.mean(null_means >= observed - 1e-15))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--adjusted-dir", default="data/cache/equities/tejhq_nse_adjusted")
    ap.add_argument("--raw-dir", default="data/cache/equities/tejhq_nse")
    ap.add_argument("--pit-universe", default="data/cache/equities/tejhq_nse_pit_universe.csv")
    ap.add_argument("--output", default="p7_timesfm10_holdout_results")
    args = ap.parse_args()

    adjusted = {s: load_series(
        Path(args.adjusted_dir) / f"{s}.csv",
        Path(args.raw_dir) / f"{s}.csv",
    ) for s in SYMBOLS}
    spans = load_pit(Path(args.pit_universe))
    ref_dates = adjusted["RELIANCE"].dates
    ref_index = {d: i for i, d in enumerate(ref_dates)}

    origin_indices = []
    for i, d in enumerate(ref_dates):
        if d < START_DATE.isoformat() or i < CONTEXT + LOOKBACK:
            continue
        future_idx = i + HORIZON
        if future_idx >= len(ref_dates):
            continue
        if not origin_indices or i - origin_indices[-1] >= REBALANCE_STEP:
            origin_indices.append(i)
    # Keep the final origin only when all strategy legs have a full 10-session endpoint.
    origin_indices = [i for i in origin_indices if i + HORIZON < len(ref_dates)]

    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    signal_rows = []
    stock_observations = []
    eligible_counts = []
    dispersion_history = []

    for i in origin_indices:
        day = ref_dates[i]
        future_day = ref_dates[i + HORIZON]
        pit = pit_eligible(spans, day)
        elig = []
        contexts = []
        future_map = {}
        momentum_map = {}
        turnover_map = {}

        for symbol in SYMBOLS:
            s = adjusted[symbol]
            idx_map = {d: j for j, d in enumerate(s.dates)}
            if symbol not in pit or day not in idx_map or future_day not in idx_map:
                continue
            j = idx_map[day]
            jf = idx_map[future_day]
            if j < CONTEXT + LOOKBACK:
                continue
            contexts.append(s.log_close[j-CONTEXT:j].copy())
            future_map[symbol] = float(s.log_close[jf] - s.log_close[j])
            momentum_map[symbol] = float(s.log_close[j] - s.log_close[j-LOOKBACK])
            turnover_slice = s.turnover[max(0, j-63):j]
            turnover_map[symbol] = float(np.nanmean(turnover_slice)) if np.isfinite(turnover_slice).any() else float("nan")
            elig.append(symbol)

        if len(elig) < TOP_K:
            continue

        forecasts = model.predict_batch(contexts, horizon=HORIZON, return_quantiles=False, univariate=True)
        tf_map = {
            symbol: float(np.asarray(out.forecast).reshape(-1)[-1] - contexts[k][-1])
            for k, (symbol, out) in enumerate(zip(elig, forecasts))
        }

        ret20 = np.asarray(list(momentum_map.values()), dtype=float)
        breadth = float(np.mean(ret20 > 0))
        equal_return = float(np.mean(ret20))
        dispersion = float(np.std(ret20))
        dispersion_history.append(dispersion)
        past_disp = dispersion_history[:-1]
        vol_regime = "high_vol" if past_disp and dispersion > float(np.median(past_disp[-60:])) else "low_vol"
        if breadth >= 0.5 and equal_return >= 0:
            regime = "risk_on"
        elif breadth < 0.5 and equal_return < 0:
            regime = "stress"
        else:
            regime = "mixed"
        regime = f"{regime}_{vol_regime}"

        eligible_counts.append(len(elig))
        for symbol in elig:
            signal_rows.append({
                "date": day,
                "symbol": symbol,
                "timesfm_forecast_return": tf_map[symbol],
                "momentum": momentum_map[symbol],
                "future_log_return": future_map[symbol],
                "avg_turnover_63d": turnover_map[symbol],
                "regime": regime,
            })
            stock_observations.append({
                "date": day,
                "symbol": symbol,
                "future_log_return": future_map[symbol],
                "timesfm_forecast_return": tf_map[symbol],
            })

    summaries = []
    period_outputs = {}
    for slippage_rate in SLIPPAGE_STRESSES:
        for strategy_key in ("timesfm_forecast_return", "momentum"):
            s, periods, costs = simulate(signal_rows, strategy_key, slippage_rate)
            summaries.append(s)
            period_outputs[(slippage_rate, strategy_key)] = periods

    # Paired block inference: TimesFM net period return minus momentum net period return at each stress.
    inference = []
    for slippage_rate in SLIPPAGE_STRESSES:
        a = {r["date"]: r["net_period_return"] for r in period_outputs[(slippage_rate, "timesfm_forecast_return")]}
        b = {r["date"]: r["net_period_return"] for r in period_outputs[(slippage_rate, "momentum")]}
        common = sorted(set(a) & set(b))
        diffs = np.asarray([a[d] - b[d] for d in common], dtype=float)
        inference.append({
            "slippage_rate": slippage_rate,
            "periods": len(diffs),
            "mean_paired_difference": float(np.mean(diffs)),
            "median_paired_difference": float(np.median(diffs)),
            "positive_period_fraction": float(np.mean(diffs > 0)),
            "block_signflip_p_one_sided": block_signflip_pvalue(diffs),
        })

    # Annual/regime diagnostics use the maximum-stress candidate and control period series.
    diagnostic_slippage = SLIPPAGE_STRESSES[-1]
    diag = []
    for strategy_key in ("timesfm_forecast_return", "momentum"):
        for r in period_outputs[(diagnostic_slippage, strategy_key)]:
            diag.append({
                "strategy": strategy_key,
                "date": r["date"],
                "year": r["year"],
                "regime": r["regime"],
                "net_period_return": r["net_period_return"],
                "cost_inr": r["cost_inr"],
                "turnover_inr": r["turnover_inr"],
                "max_participation": r["max_participation"],
            })

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "signal_rows.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=signal_rows[0].keys())
        writer.writeheader()
        writer.writerows(signal_rows)
    with (out / "diagnostic_periods.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=diag[0].keys())
        writer.writeheader()
        writer.writerows(diag)

    result = {
        "lane": "phase7_post_selection_timesfm10_holdout",
        "holdout_start": START_DATE.isoformat(),
        "horizon_sessions": HORIZON,
        "rebalance_step_sessions": REBALANCE_STEP,
        "context": CONTEXT,
        "lookback": LOOKBACK,
        "top_k": TOP_K,
        "symbols_requested": list(SYMBOLS),
        "mean_eligible_stocks_per_origin": float(np.mean(eligible_counts)),
        "min_eligible_stocks_per_origin": int(np.min(eligible_counts)),
        "max_eligible_stocks_per_origin": int(np.max(eligible_counts)),
        "origin_count": len(origin_indices),
        "origin_date_first": origin_indices and ref_dates[origin_indices[0]] or None,
        "origin_date_last": origin_indices and ref_dates[origin_indices[-1]] or None,
        "slippage_stresses": list(SLIPPAGE_STRESSES),
        "fee_model": {
            "cash_delivery_stt_buy_rate": STT_DELIVERY_RATE,
            "cash_delivery_stt_sell_rate": STT_DELIVERY_RATE,
            "stamp_buy_rate": STAMP_BUY_RATE,
            "sebi_turnover_rate": SEBI_RATE,
            "exchange_plus_ipft_rate": EXCHANGE_RATE,
            "brokerage_per_order_inr": BROKERAGE_INR,
            "dp_sell_inr": DP_SELL_INR,
            "gst_rate": GST,
        },
        "strategy_summaries": summaries,
        "paired_block_inference": inference,
        "gate": {
            "candidate_is_single_frozen_post_selection_cell": True,
            "multiple_testing_search_on_holdout": False,
            "phase7_final_promotion_requires_all_stresses_net_positive": True,
            "phase7_final_promotion_requires_candidate_ahead_of_momentum_at_max_stress": True,
            "phase7_final_promotion_requires_block_inference_and_capacity_review": True,
        },
        "note": "Post-selection holdout; candidate parameters were frozen before holdout execution. Bootstrap universe remains limited to the repository's 30-name stock panel.",
    }
    (out / "summary.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
