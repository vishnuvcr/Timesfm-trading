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
ORIGINS_PER_MODEL_BATCH = 8

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
            o = float(row["open"]); h = float(row["high"]); l = float(row["low"]); c = float(row["close"])
            rows.append({
                "time": int(row["time"]),
                "day": t.date().isoformat(),
                "minute": minutes - (9 * 60 + 15),
                "open": o, "close": c,
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
    return np.divide(
        np.cumsum(close * vol),
        np.cumsum(vol),
        out=close.copy(),
        where=np.cumsum(vol) > 0,
    ).astype(np.float32)

def build_common_data(all_sessions):
    common = None
    for symbol in SYMBOLS:
        days = set(all_sessions[symbol])
        common = days if common is None else common & days
    common_days = sorted(common)
    data = {}
    for symbol in SYMBOLS:
        log_close=[]; opens=[]; vwap=[]; valid=[]; volume=[]
        for day in common_days:
            vals = all_sessions[symbol][day]
            log_close.extend(math.log(r["close"]) for r in vals)
            opens.extend(r["open"] for r in vals)
            vwap.extend(session_vwap(vals))
            valid.extend(r["valid"] for r in vals)
            volume.extend(r["volume"] for r in vals)
        data[symbol] = {
            "log_close": np.asarray(log_close, dtype=np.float32),
            "open": np.asarray(opens, dtype=np.float32),
            "vwap": np.asarray(vwap, dtype=np.float32),
            "valid": np.asarray(valid, dtype=bool),
            "volume": np.asarray(volume, dtype=np.float32),
        }
    return common_days, data

def select_origins(common_days, horizon):
    edges = np.linspace(0, len(common_days), FOLDS+1, dtype=int)
    selected={}
    for fold in range(1, FOLDS+1):
        days=common_days[edges[fold-1]:edges[fold]]
        candidates=[]
        for di in range(edges[fold-1], edges[fold]):
            for minute in range(MIN_ORIGIN_MINUTE, LAST_EXIT_MINUTE-horizon+1, horizon):
                candidates.append((di, minute))
        if len(candidates)<ORIGINS_PER_FOLD:
            raise RuntimeError(f"horizon={horizon}, fold={fold}: only {len(candidates)} origins")
        picks=np.linspace(0,len(candidates)-1,ORIGINS_PER_FOLD,dtype=int)
        selected[fold]=[candidates[i] for i in np.unique(picks)]
    return selected

def rank_ic(a,b):
    if len(a)<2 or np.std(a)==0 or np.std(b)==0:
        return math.nan
    return float(np.corrcoef(np.argsort(np.argsort(a)), np.argsort(np.argsort(b)))[0,1])

def cost_components(buy_notional,sell_notional,n_buy,n_sell,slippage):
    turnover=buy_notional+sell_notional
    brokerage=(n_buy+n_sell)*BROKERAGE_PER_EXECUTION
    exchange=turnover*NSE_CASH_PER_SIDE
    sebi=turnover*SEBI_PER_SIDE
    stt=sell_notional*STT_INTRADAY_SELL
    stamp=buy_notional*STAMP_BUY
    gst=GST*(brokerage+exchange+sebi)
    slip=turnover*slippage
    total=brokerage+exchange+sebi+stt+stamp+gst+slip
    return {"brokerage":brokerage,"exchange":exchange,"sebi":sebi,"stt":stt,"stamp":stamp,"gst":gst,"slippage":slip,"total":total}

def simulate(periods, score_key, slippage):
    capital=CAPITAL; out=[]
    for row in periods:
        chosen=[s for s,_ in sorted(row[score_key].items(),key=lambda x:(x[1],x[0]),reverse=True)[:TOP_K]]
        gross=float(np.mean([row["realized_return"][s] for s in chosen]))
        costs=cost_components(capital,capital,TOP_K,TOP_K,slippage)
        net=(gross*capital-costs["total"])/capital
        participation=max(row["participation_60m"].get(s,0.0) for s in chosen)
        capital*=max(0.0,1.0+net)
        out.append({"day":row["day"],"fold":row["fold"],"horizon":row["horizon"],"gross_return":gross,"net_return":net,"cost_total":costs["total"],"participation":participation})
    arr=np.asarray([x["net_return"] for x in out],dtype=float)
    curve=CAPITAL*np.cumprod(np.r_[1.0,1.0+arr])
    dd=curve/np.maximum.accumulate(curve)-1.0
    return {"net_total_return":float(capital/CAPITAL-1.0),"mean_period_return":float(arr.mean()) if len(arr) else math.nan,"max_drawdown":float(dd.min()) if len(dd) else math.nan,"period_count":len(out),"mean_turnover_fraction":2.0,"max_participation":float(max((x["participation"] for x in out),default=0.0)),"periods":out}

def block_signflip(diffs, block_size=5, reps=10000, seed=20260920):
    diffs=np.asarray(diffs,dtype=float)
    blocks=[diffs[i:i+block_size] for i in range(0,len(diffs),block_size) if len(diffs[i:i+block_size])==block_size]
    if not blocks: return math.nan
    b=np.asarray([x.mean() for x in blocks])
    obs=float(b.mean())
    rng=np.random.default_rng(seed)
    signs=rng.choice(np.array([-1.0,1.0]),size=(reps,len(b)))
    return float(np.mean((signs*b).mean(axis=1)>=obs-1e-15))

def bh(pvals):
    ordered=sorted(pvals.items(),key=lambda x:x[1]); m=len(ordered); out={}; running=1.0
    for rank,(name,p) in reversed(list(enumerate(ordered,1))):
        running=min(running,p*m/rank); out[name]=running
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--zip",required=True)
    ap.add_argument("--output",default="p4_intraday_strategy_batched_results")
    args=ap.parse_args()
    digest=sha256_file(Path(args.zip))
    if digest!=SOURCE_SHA256: raise SystemExit("release SHA-256 mismatch")

    with zipfile.ZipFile(args.zip) as zf:
        sessions={s:build_complete_sessions(read_symbol(zf,s)) for s in SYMBOLS}
    common_days,data=build_common_data(sessions)
    model=TimesFM3Adapter(checkpoint="google/timesfm-3.0-pytorch",device="cpu",per_core_batch_size=8,purpose="research_only")

    forecast_rows=[]; periods_by_horizon={h:[] for h in HORIZONS}
    for horizon in HORIZONS:
        tasks=[]
        for fold,origins in select_origins(common_days,horizon).items():
            for day_idx,minute in origins:
                base=day_idx*375+minute
                ctxs=[]; usable=[]
                for s in SYMBOLS:
                    start=base-CONTEXT
                    if start<0 or not data[s]["valid"][start:base].all(): continue
                    ctxs.append(data[s]["log_close"][start:base]); usable.append(s)
                if len(usable)>=TOP_K:
                    tasks.append((fold,day_idx,minute,usable,ctxs))
        for start_idx in range(0,len(tasks),ORIGINS_PER_MODEL_BATCH):
            chunk=tasks[start_idx:start_idx+ORIGINS_PER_MODEL_BATCH]
            all_ctx=[]; spans=[]
            for fold,day_idx,minute,usable,ctxs in chunk:
                off=len(all_ctx)
                all_ctx.extend(ctxs)
                spans.append((fold,day_idx,minute,usable,off))
            outputs=model.predict_batch(all_ctx,horizon=max(HORIZONS),return_quantiles=False,univariate=True)
            for fold,day_idx,minute,usable,off in spans:
                base=day_idx*375+minute
                tf={}; vw={}; flog={}; real={}; part={}
                for j,s in enumerate(usable):
                    ctx=all_ctx[off+j]
                    pred=float(np.asarray(outputs[off+j].forecast).reshape(-1)[horizon-1]-ctx[-1])
                    exit_idx=base+horizon; entry_idx=base+1
                    future=float(data[s]["log_close"][exit_idx]-data[s]["log_close"][base])
                    entry=float(data[s]["open"][entry_idx]); exitp=float(np.exp(data[s]["log_close"][exit_idx]))
                    price=float(np.exp(data[s]["log_close"][base])); v=float(data[s]["vwap"][base])
                    realized=exitp/entry-1.0
                    trailing=float(np.mean(np.exp(data[s]["log_close"][max(0,base-60):base])*data[s]["volume"][max(0,base-60):base]))
                    tf[s]=pred; vw[s]=price/v-1.0 if v>0 else 0.0; flog[s]=future; real[s]=realized; part[s]=(CAPITAL/TOP_K)/max(trailing,1.0)
                    forecast_rows.append({"fold":fold,"day":common_days[day_idx],"minute":minute,"horizon":horizon,"symbol":s,"timesfm_forecast_return":pred,"future_log_return":future,"realized_execution_return":realized,"vwap_score":vw[s]})
                periods_by_horizon[horizon].append({"fold":fold,"day":common_days[day_idx],"horizon":horizon,"timesfm":tf,"vwap":vw,"future_log_return":flog,"realized_return":real,"participation_60m":part})

    forecast_summary=[]
    for h in HORIZONS:
        rows=[r for r in forecast_rows if r["horizon"]==h]; y=np.asarray([r["future_log_return"] for r in rows]); p=np.asarray([r["timesfm_forecast_return"] for r in rows])
        by=defaultdict(list)
        for r in rows: by[(r["fold"],r["day"],r["minute"])].append(r)
        ics=[rank_ic(np.asarray([x["timesfm_forecast_return"] for x in v]),np.asarray([x["future_log_return"] for x in v])) for v in by.values()]
        acc=float(np.mean((p>0)==(y>0))); base=float(np.mean(y>0))
        forecast_summary.append({"horizon":h,"stock_observations":len(rows),"origin_count":len(by),"timesfm_mae":float(np.mean(np.abs(y-p))),"persistence_mae":float(np.mean(np.abs(y))),"directional_accuracy":acc,"positive_return_base_rate":base,"directional_excess_pp":100*(acc-base),"mean_cross_sectional_rank_ic":float(np.nanmean(ics)) if ics else math.nan})

    strategy_results=[]
    for h in HORIZONS:
        periods=periods_by_horizon[h]
        for strat in ("timesfm","vwap"):
            for slip in EXTRA_SLIPPAGE:
                sim=simulate(periods,strat,slip)
                fold=[simulate([p for p in periods if p["fold"]==f],strat,slip)["net_total_return"] for f in range(1,FOLDS+1)]
                strategy_results.append({"horizon":h,"strategy":strat,"slippage_rate":slip,"net_total_return":sim["net_total_return"],"max_drawdown":sim["max_drawdown"],"mean_period_return":sim["mean_period_return"],"period_count":sim["period_count"],"mean_turnover_fraction":sim["mean_turnover_fraction"],"max_participation":sim["max_participation"],"fold_returns":fold})

    dev_p={}
    for h in HORIZONS:
        tp=simulate([p for p in periods_by_horizon[h] if p["fold"] in (1,2,3)],"timesfm",PRIMARY_DEV_SLIPPAGE)["periods"]
        vp=simulate([p for p in periods_by_horizon[h] if p["fold"] in (1,2,3)],"vwap",PRIMARY_DEV_SLIPPAGE)["periods"]
        dev_p[str(h)]=block_signflip(np.asarray([a["net_return"]-b["net_return"] for a,b in zip(tp,vp)]))
    dev_q=bh(dev_p)
    candidates=[]
    for h in HORIZONS:
        t=next(x for x in strategy_results if x["horizon"]==h and x["strategy"]=="timesfm" and abs(x["slippage_rate"]-PRIMARY_DEV_SLIPPAGE)<1e-12)
        v=next(x for x in strategy_results if x["horizon"]==h and x["strategy"]=="vwap" and abs(x["slippage_rate"]-PRIMARY_DEV_SLIPPAGE)<1e-12)
        if all(t["fold_returns"][i]>v["fold_returns"][i] and t["fold_returns"][i]>0 for i in range(3)) and dev_q[str(h)]<0.10:
            candidates.append(h)

    holdout=[]
    for h in candidates:
        for slip in EXTRA_SLIPPAGE:
            t=next(x for x in strategy_results if x["horizon"]==h and x["strategy"]=="timesfm" and abs(x["slippage_rate"]-slip)<1e-12)
            v=next(x for x in strategy_results if x["horizon"]==h and x["strategy"]=="vwap" and abs(x["slippage_rate"]-slip)<1e-12)
            holdout.append({"horizon":h,"slippage_rate":slip,"timesfm_holdout_return":t["fold_returns"][3],"vwap_holdout_return":v["fold_returns"][3],"timesfm_ahead_of_vwap":t["fold_returns"][3]>v["fold_returns"][3]})

    out={"lane":"phase4_intraday_timesfm_vwap","model":"timesfm-3.0-pytorch","source_release_sha256":digest,"symbols":list(SYMBOLS),"horizons":list(HORIZONS),"context":CONTEXT,"top_k":TOP_K,"folds":FOLDS,"origins_per_fold":ORIGINS_PER_FOLD,"model_origins_per_batch":ORIGINS_PER_MODEL_BATCH,"extra_slippage":list(EXTRA_SLIPPAGE),"primary_development_slippage":PRIMARY_DEV_SLIPPAGE,"development_block_p":dev_p,"development_bh_q":dev_q,"development_candidates":candidates,"forecast_summary":forecast_summary,"strategy_results":strategy_results,"holdout_results":holdout,"status":"candidate_holdout_required" if candidates else "no_intraday_cell_passed_development","note":"Same frozen data/horizon/fold/cost/promotion protocol as the first intraday matrix; only the TimesFM inference batching was optimized."}
    output=Path(args.output); output.mkdir(parents=True,exist_ok=True)
    with (output/"forecast_rows.csv").open("w",newline="",encoding="utf-8") as fh:
        w=csv.DictWriter(fh,fieldnames=forecast_rows[0].keys()); w.writeheader(); w.writerows(forecast_rows)
    (output/"summary.json").write_text(json.dumps(out,indent=2)+"\n")
    print(json.dumps(out,indent=2))
    if not periods_by_horizon[HORIZONS[0]]: raise SystemExit(1)

if __name__=="__main__":
    main()
