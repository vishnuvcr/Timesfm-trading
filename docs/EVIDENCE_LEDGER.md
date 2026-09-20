# Evidence ledger — TimesFM / finance / NSE

## E1 — Google TimesFM 3.0 capability

Finding: TimesFM 3.0 adds native multivariate forecasting and flexible past-only and past-and-future covariates; the official PyTorch model card lists a 20-layer transformer, 1280-dimensional model states, 16 heads, 32-point input patch, 64-point forecast patch and nine quantiles.

Source: official Google TimesFM repository and Google Hugging Face model card. citeturn285712search1turn670140view1

Relevance: directly supports the multivariate/covariate Phase 3 design.

Limitation: general forecasting benchmarks are not evidence of trading alpha.

## E2 — TimesFM 3.0 license

Finding: pretrained TimesFM 3.0 weights are under TimesFM Non-Commercial License v1.0. Non-Commercial Purpose excludes commercial gain, production deployment, revenue generation and commercial decision-making; the restriction extends to model outputs.

Source: official model license. citeturn670140view0

Relevance: 3.0 is a scientific/evaluation model in this repository until commercial rights are obtained.

## E3 — US equity directional gate, TimesFM 3.0

Finding: An independent frozen walk-forward repository reports 93,703 US forecasts for TimesFM 3.0 with excess directional accuracy of -5.4% (95% CI -7.3% to -3.7%), median skill -3.4%, 75.1% q10-q90 coverage and 0/112 symbols beating persistence after FDR.

Source: TimesFM Alpha Gate README. citeturn259680search0

Relevance: strong prior against assuming zero-shot 3.0 direction is alpha.

Limitations: Yahoo-based dataset; US market, not NSE; one-month horizon; repository-specific design.

## E4 — Indian equity directional gate, TimesFM 2.5

Finding: The same repository reports 40,992 Indian forecasts for TimesFM 2.5 on NIFTY 50 + NIFTYBEES with excess directional accuracy -5.8% (95% CI -8.4% to -3.2%), median skill -2.7%, 78.0% coverage and 0/51 symbols beating persistence after FDR.

Source: TimesFM Alpha Gate README. citeturn259680search0

Relevance: important NSE-specific prior.

Limitations: not 3.0; Yahoo-based data; survivorship issues are acknowledged by the repository.

## E5 — Important attribution correction

The external README's prose says both generations lacked directional skill on US and Indian equities, but the displayed quantitative table reports a 3.0 result for US and a 2.5 result for India. We therefore do not use an Indian 3.0 numerical result from that repository.

Relevance: prevents overstatement of evidence.

## E6 — TimesFM 3.0 options / IV surface

Finding: A pre-registered September 2026 study evaluated TimesFM-3 on the SPY implied-volatility surface against random walk, AR(1), log-HAR, PCA-VAR and a market forward-variance-implied forecast. TimesFM was competitive in forecast-loss terms; recalibration reduced much of the short-horizon advantage; the market's forward-variance forecast beat the models at ATM nodes; a residual wing signal survived statistical controls. The study explicitly did not run a fill/P&L test.

Source: SSRN study and reproducibility package. citeturn259680search2turn259680search5

Relevance: Phase 5 must benchmark against market-implied movement, not just statistical baselines.

Limitation: SPY, not NSE; no economic execution test.

## E7 — Community NSE options data

Finding: Hugging Face dataset rissin/nse-options-intraday reports about 259M rows and 2.5 GB across NIFTY/BANKNIFTY/SENSEX, with daily history derived from NSE F&O bhavcopy and 1-minute intraday data sourced from Upstox; the dataset card says the intraday history is 2024 to present and the historical daily track spans much earlier.

Source: dataset card. citeturn910524search0turn910524search1

Relevance: useful as a secondary options cross-check / bootstrap dataset.

Limitation: license is listed as other; provenance is mixed; not the primary exchange source.

## E8 — Community 1-minute index/options data

Finding: Hugging Face thetrademarkk/india-index-options-1m reports about 377M rows of 1-minute index/option bars with partial option coverage and a CC BY-NC-4.0 license.

Source: dataset card. citeturn910524search6

Relevance: useful for parser/infrastructure tests if license-compatible.

Limitation: non-commercial license, partial liquidity coverage, and not a substitute for licensed primary exchange history.

## E9 — NSE F&O format transition

Finding: NSE's current all-reports page says the old F&O bhavcopy/common bhavcopy was discontinued from July 8, 2024 and replaced by the F&O-UDiFF Common Bhavcopy Final.

Source: official NSE. citeturn910524search4

Relevance: ingestion must branch on the July 8, 2024 format transition.

## E10 — NSE historical data availability

Finding: NSE provides paid EOD/historical CM and F&O data containing bhavcopy/security/trade details, with technical specifications and tariff for subscribers.

Source: official NSE historical data page. citeturn910524search5

Relevance: authoritative source for the data quality needed for scalping/execution research.

Limitation: restricted products require subscription/licensing; the public repo will not redistribute them.

## E11 — Evidence grade

A = official exchange/model/license source.
B = reproducible independent research with precise methodology/results.
C = community datasets/tools useful for cross-checks.
D = anecdotal/practitioner content.

No trading strategy is promoted solely on C or D evidence.

## E12 — TimesFM 3.0 P1 NIFTY 50 exploratory forecast

Finding: On a fixed secondary NIFTY 50 OHLC snapshot (5,058 rows, 2000-01-03 to 2021-01-25), TimesFM 3.0 was evaluated at 80 forecast origins with context 128 and a 5-session horizon. Log-level MAE was 0.01310 versus persistence 0.01517 (13.63% lower); RMSE was 0.01649 versus 0.01955 (15.66% lower); five-day return MAE was 0.01849 versus 0.02129 (13.18% lower). Directional accuracy was 70.0% versus a 75.0% positive-return base rate, giving -5.0 percentage points excess direction. q10-q90 coverage was 78.75%. An exploratory lag-4 Newey-West paired-loss test on origin-level MAE gave t=-2.10 and one-sided p≈0.018; moving-block bootstrap (block 5) 95% CI was approximately [-0.00416, -0.00029].

Source: repository Phase 3 P1 workflow run 56 and its uploaded artifact; secondary Google Finance-derived GitHub snapshot, upstream commit c73de0e6c9acca1330a19cd41ee3d7dbd5100260 / blob fc51a9331ee2b72c430724d5e0bdd0237f91103a.

Evidence grade: C — exploratory secondary-data result.

Relevance: validates the end-to-end TimesFM 3.0 forecast, quantile and statistical pipeline and suggests level-error improvement can coexist with weak directional excess.

Limitations: secondary dataset with no explicit upstream license file; historical window ends 2021-01-25; only one target/horizon/input family; post-hoc inference; no transaction-cost strategy test; not primary NSE P0 evidence; no promotion value.

## E13 — TimesFM 3.0 secondary-data multivariate/covariate ablation

Finding: On 4,015 aligned secondary NIFTY 50/RELIANCE/TCS/HDFCBANK/HINDUNILVR rows from 2004-08-25 to 2021-01-25, with 80 identical origins, context 128 and five-session horizon, univariate NIFTY 50 produced log MAE 0.01849, RMSE 0.02166 and 70.0% directional accuracy. Native five-series multivariate produced MAE 0.01858 (+0.51%), RMSE 0.02257 (+4.21%) and 72.5% directional accuracy. NIFTY 50 plus four past-only covariates produced the same recorded metrics as univariate in this run.

Source: Phase 3 workflow run 64 and uploaded artifact; secondary Google Finance-derived GitHub snapshot, upstream commit c73de0e6c9acca1330a19cd41ee3d7dbd5100260.

Evidence grade: C — exploratory secondary-data result.

Relevance: provides direct exploratory evidence for H2/H3: cross-series inputs can change directional forecasts without improving point forecast error, while this particular past-only covariate configuration showed no recorded metric change.

Limitations: one dataset snapshot, one horizon, 80 origins, historical window ending 2021-01-25, no primary NSE data, no economic strategy test, no multiple-testing correction across a full model matrix. Not a strategy-promotion result.
