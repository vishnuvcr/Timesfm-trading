# NSE data catalog — Phase 2

## P0: mandatory before TimesFM 3.0 forecast experiments

- Cash equity daily: NSE security-wise archives / historical reports.
- Index daily: NSE historical index data.
- India VIX: NSE historical data.
- F&O UDiFF bhavcopy: NSE.
- Participant OI/volume: NSE.
- Option chain snapshots: NSE interface, but historical research must use an authorized/licensed source.
- Corporate actions: NSE corporate actions/filings.
- Historical trade/order data: NSE Data & Analytics, licensed.

NSE historical reports expose security-wise price/volume archives, historical index data and India VIX history. NSE derivatives reports include UDiFF common bhavcopy, participant OI/volume and FII derivatives statistics. NSE also sells historical trade/order data for deeper CM/F&O studies. citeturn209752search0turn209752search1turn173596search2turn209752search3

## P1: contextual / cross-market

- FII/FPI and DII daily flows.
- GIFT NIFTY / NSE IX session and contract data.
- BSE EOD and historical datasets for cross-exchange lead/lag.
- USDINR, RBI/FBIL rates, crude, gold, major Asian/US indices and breadth.
- Timestamped corporate announcements/news.

NSE states that FII/FPI daily data are provisional and may change after custodial confirmation, so research must preserve publication vintages rather than silently overwrite old observations. citeturn676787search6turn676787search7

NSE IX documents GIFT NIFTY trading hours extending from the Indian pre-open period into the overnight period, making it a candidate lead/lag feature for BTST and next-open models. citeturn173596search63

BSE publishes EOD/reference data and historical market-data products for research/backtesting. citeturn992845search1turn992845search2

## P2: research expansion

Historical news/event feeds with publication timestamps; point-in-time company fundamentals and filings; listing/delisting and index-membership history; governance and investor-meeting events; additional rates, commodities and international futures.

## Licensing decision

The public repository will not redistribute restricted exchange raw data. NSE distinguishes market-data subscription/licensing and research use, and its historical EOD/trade products are licensed. The public repository therefore stores schemas, manifests, checksums, derived aggregates and permitted fixtures; restricted raw feeds remain in approved private storage referenced by hash. citeturn209752search10turn209752search7

## Critical options warning

NSE's public option-chain page exposes OI, change in OI, volume, IV, LTP and bid/ask, but its terms restrict copying/aggregation. The Phase 5 options engine will therefore use an authorized historical source rather than public-page scraping as the canonical database. citeturn173596search1
