from __future__ import annotations

import argparse
import csv
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from src.model.timesfm3_adapter import TimesFM3Adapter

CONTEXT = 128
HORIZON = 5
LOOKBACK = 20
FOLDS = 4
ORIGINS_PER_FOLD = 8
TOP_K = 6
CAPITAL = 1_000_000.0
BROKERAGE_PER_ORDER = 20.0
DP_SELL = 13.5
STRATEGIES = ("equal_weight", "momentum", "timesfm", "hybrid", "momentum_gate")
ONE_WAY_COST_SCENARIOS = (0.00125, 0.0025, 0.00375, 0.0050)


@dataclass(frozen=True)
class Series:
    dates: list[str]
    log_close: np.ndarray


def load_series(path: Path) -> Series:
    dates: list[str] = []
    values: list[float] = []
    with path.open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if not {"date", "adj_close"}.issubset(reader.fieldnames or []):
            raise RuntimeError(f"{path}: expected date and adj_close")
        for row in reader:
            dates.append(row["date"][:10])
            values.append(float(row["adj_close"]))
    if dates != sorted(dates) or len(dates) != len(set(dates)):
        raise RuntimeError(f"{path}: dates are not sorted/unique")
    return Series(dates=dates, log_close=np.log(np.asarray(values, dtype=np.float32)))


def zscore(x: np.ndarray) -> np.ndarray:
    mean = float(np.mean(x))
    std = float(np.std(x))
    if std <= 1e-12:
        return np.zeros_like(x)
    return (x - mean) / std


def choose_top(scores: np.ndarray, k: int, eligible: np.ndarray | None = None) -> np.ndarray:
    mask = np.ones(len(scores), dtype=bool) if eligible is None else eligible.copy()
    idx = np.flatnonzero(mask)
    if len(idx) == 0:
        return np.zeros(len(scores), dtype=float)
    order = idx[np.argsort(scores[idx])[::-1]]
    picks = order[: min(k, len(order))]
    w = np.zeros(len(scores), dtype=float)
    w[picks] = 1.0 / len(picks)
    return w


def fixed_cost(notional_orders: int) -> float:
    return float(notional_orders) * (BROKERAGE_PER_ORDER + DP_SELL)


def portfolio_trade_cost(old_w: np.ndarray, new_w: np.ndarray, capital: float, one_way_rate: float) -> tuple[float, float]:
    delta = np.abs(new_w - old_w)
    traded_notional = float(delta.sum() * capital)
    orders = int(np.sum((old_w > 1e-12) & (new_w < 1e-12)) + np.sum((new_w > 1e-12) & (old_w < 1e-12)))
    fixed = fixed_cost(orders)
    proportional = traded_notional * one_way_rate
    return proportional + fixed, traded_notional


def fold_origins(common_dates: list[str]) -> list[np.ndarray]:
    start = LOOKBACK + CONTEXT
    end = len(common_dates) - HORIZON - 1
    if end <= start:
        raise RuntimeError("insufficient common history for strategy folds")
    edges = np.linspace(start, end + 1, FOLDS + 1, dtype=int)
    folds: list[np.ndarray] = []
    for i in range(FOLDS):
        a, b = int(edges[i]), int(edges[i + 1] - 1)
        if b < a:
            raise RuntimeError("empty strategy fold")
        candidates = np.arange(a, b + 1, 5, dtype=int)
        if len(candidates) < ORIGINS_PER_FOLD:
            candidates = np.linspace(a, b, ORIGINS_PER_FOLD, dtype=int)
        folds.append(np.unique(candidates[:ORIGINS_PER_FOLD]))
    return folds


def run_backtest(
    returns: list[dict[str, np.ndarray | str]],
    one_way_rate: float,
) -> list[dict]:
    results = []
    for strategy in STRATEGIES:
        capital = CAPITAL
        old_w = np.zeros(TOP_K)
        equity_curve = [capital]
        gross_period_returns: list[float] = []
        net_period_returns: list[float] = []
        turnover: list[float] = []

        for row in returns:
            scores = np.asarray(row[strategy + "_score"], dtype=float)
            future = np.asarray(row["future_return"], dtype=float)

            if strategy == "equal_weight":
                new_w = np.ones(TOP_K) / TOP_K
            elif strategy == "momentum_gate":
                eligible = np.asarray(row["timesfm_positive"], dtype=bool)
                new_w = choose_top(scores, TOP_K, eligible)
            else:
                new_w = choose_top(scores, TOP_K)

            # Equal-weight portfolio is represented over TOP_K slots; cost is based on weight turnover.
            # The signal is long-only and uninvested slots remain cash.
            period_return = float(np.dot(new_w, future[np.argsort(scores)[-TOP_K:][::-1]]) if strategy != "equal_weight" else np.mean(future))
            # For scored strategies, selected returns must correspond to selected names, not score order.
            if strategy != "equal_weight":
                selected = np.flatnonzero(new_w > 0)
                period_return = float(np.dot(new_w[selected], future[selected]))

            fee, traded_notional = portfolio_trade_cost(old_w, new_w, capital, one_way_rate)
            net_return = (period_return * capital - fee) / capital
            capital *= max(0.0, 1.0 + net_return)

            gross_period_returns.append(period_return)
            net_period_returns.append(net_return)
            turnover.append(traded_notional / CAPITAL)
            equity_curve.append(capital)
            old_w = new_w

        arr = np.asarray(net_period_returns)
        eq = np.asarray(equity_curve)
        drawdowns = eq / np.maximum.accumulate(eq) - 1.0
        results.append({
            "strategy": strategy,
            "one_way_cost_rate": one_way_rate,
            "net_total_return": float(eq[-1] / CAPITAL - 1.0),
            "gross_mean_5d_return": float(np.mean(gross_period_returns)),
            "net_mean_5d_return": float(np.mean(net_period_returns)),
            "net_median_5d_return": float(np.median(net_period_returns)),
            "net_hit_rate": float(np.mean(arr > 0)),
            "net_max_drawdown": float(np.min(drawdowns)),
            "mean_turnover_fraction_per_rebalance": float(np.mean(turnover)),
            "rebalance_count": int(len(arr)),
            "final_capital": float(eq[-1]),
        })
    return results


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data/cache/equities/tejhq_nse_adjusted")
    ap.add_argument("--symbols", default="RELIANCE,TCS,HDFCBANK,INFY,ICICIBANK,SBIN,ITC,BHARTIARTL,LT,AXISBANK,KOTAKBANK,HINDUNILVR,MARUTI,SUNPHARMA,BAJFINANCE,ASIANPAINT,TITAN,HCLTECH,WIPRO,ULTRACEMCO,NESTLEIND,M&M,NTPC,ONGC,POWERGRID,TATAMOTORS,TATASTEEL,ADANIENT,CIPLA,DRREDDY")
    ap.add_argument("--output", default="p4_stock_overlay_results")
    args = ap.parse_args()

    symbols = [s.strip().upper() for s in args.symbols.split(",") if s.strip()]
    series = {s: load_series(Path(args.data_dir) / f"{s}.csv") for s in symbols}

    common = set(series[symbols[0]].dates)
    for s in symbols[1:]:
        common &= set(series[s].dates)
    common_dates = sorted(common)
    if len(common_dates) < CONTEXT + LOOKBACK + HORIZON + FOLDS * ORIGINS_PER_FOLD:
        raise RuntimeError("common stock history is too short for the declared strategy experiment")

    index = {s: {d: i for i, d in enumerate(series[s].dates)} for s in symbols}
    folds = fold_origins(common_dates)
    all_rows = []
    model = TimesFM3Adapter(
        checkpoint="google/timesfm-3.0-pytorch",
        device="cpu",
        per_core_batch_size=8,
        purpose="research_only",
    )

    for fold_no, origins in enumerate(folds, start=1):
        for origin_pos in origins:
            date = common_dates[int(origin_pos)]
            contexts = []
            momentum = []
            future = []
            for s in symbols:
                i = index[s][date]
                contexts.append(series[s].log_close[i - CONTEXT:i].copy())
                momentum.append(float(series[s].log_close[i] - series[s].log_close[i - LOOKBACK]))
                future.append(float(np.exp(series[s].log_close[i + HORIZON] - series[s].log_close[i]) - 1.0))

            forecasts = model.predict_batch(contexts, horizon=HORIZON, return_quantiles=True, univariate=True)
            tfm_return = np.array([
                float(np.asarray(out.forecast).reshape(-1)[-1] - contexts[j][-1])
                for j, out in enumerate(forecasts)
            ], dtype=float)
            mom = np.asarray(momentum, dtype=float)
            fut = np.asarray(future, dtype=float)

            hybrid = 0.5 * zscore(mom) + 0.5 * zscore(tfm_return)
            gate = tfm_return > 0

            all_rows.append({
                "fold": fold_no,
                "date": date,
                "future_return": fut,
                "equal_weight_score": np.zeros(len(symbols)),
                "momentum_score": mom,
                "timesfm_score": tfm_return,
                "hybrid_score": hybrid,
                "momentum_gate_score": mom,
                "timesfm_positive": gate,
            })

    # Backtest equal-weight universe separately from top-k selections; scored strategies use their own selected names.
    scenario_results = []
    for rate in ONE_WAY_COST_SCENARIOS:
        scenario_results.extend(run_backtest(all_rows, rate))

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)

    # Persist compact per-origin signal/return table for reproducibility.
    rows_out = []
    for row in all_rows:
        for s, m, t, h, g, fr in zip(
            symbols,
            row["momentum_score"],
            row["timesfm_score"],
            row["hybrid_score"],
            row["timesfm_positive"],
            row["future_return"],
        ):
            rows_out.append({
                "fold": row["fold"],
                "date": row["date"],
                "symbol": s,
                "momentum_20d": float(m),
                "timesfm_5d_forecast": float(t),
                "hybrid_score": float(h),
                "timesfm_positive": bool(g),
                "future_5d_return": float(fr),
            })

    with (out / "per_origin_signals.csv").open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=rows_out[0].keys())
        writer.writeheader()
        writer.writerows(rows_out)

    summary = {
        "lane": "P4.1_exploratory_stock_selection_timesfm_overlay",
        "model": "timesfm-3.0-pytorch",
        "stocks": len(symbols),
        "common_dates": len(common_dates),
        "folds": FOLDS,
        "origins_per_fold": ORIGINS_PER_FOLD,
        "total_rebalances": len(all_rows),
        "lookback_sessions": LOOKBACK,
        "forecast_horizon": HORIZON,
        "top_k": TOP_K,
        "capital": CAPITAL,
        "brokerage_reference_per_order": BROKERAGE_PER_ORDER,
        "dp_sell_reference": DP_SELL,
        "one_way_cost_scenarios": list(ONE_WAY_COST_SCENARIOS),
        "note": "Research-only, long-only cash-equity overlay test. No production use. Current statutory/broker references are stress inputs; final Phase 7 uses effective-date charges.",
    }
    (out / "summary.json").write_text(json.dumps(summary, indent=2) + "\\n", encoding="utf-8")
    (out / "strategy_results.json").write_text(json.dumps(scenario_results, indent=2) + "\\n", encoding="utf-8")
    print(json.dumps({"summary": summary, "strategy_results": scenario_results}, indent=2))


if __name__ == "__main__":
    main()
