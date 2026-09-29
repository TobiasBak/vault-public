# Poly Trader

Poly Trader was Tobias's March-April 2026 experiment in trading Polymarket's five-minute Bitcoin Up/Down markets. It watched Binance BTCUSDT prices for short momentum or spike signals, compared them with the market's price to beat, and used configurable workers to buy the corresponding outcome. The Rust system grew into a capable trading laboratory with shared live and paper decisions, market capture, deterministic replay, real-order reconciliation, settlement tracking, dashboards, and automated strategy search.

The project was stronger as engineering than as a profitable strategy. The recovered real-trade snapshots contain 581 settled bets with about $581 of stake, 431 wins, 150 losses, and recorded realized P&L of **-$27.03**. Six positions were unresolved in the snapshots, and the records do not establish fees or final account-level P&L. The main production run from March 23-27 settled $575 and lost **$21.03**, or 3.66%. Its dominant Mar24 worker lost **$21.38** on 515 settled bets.

The central result was that apparent signal quality did not survive execution. On the 575 settled production bets, settlement P&L would have been about **+$24.82** if the decision-time quotes had been executable. Actual fills averaged 3.15 cents worse and produced **-$21.03**. This roughly $45.85 reversal suggests that Binance did identify information that Polymarket was repricing, but the apparent advantage mostly existed in stale or fleeting quotes rather than capturable prices. The paired paper run was even worse, so live execution was not simply underperforming an optimistic simulator.

Strategy research also selected too aggressively from a short, repeatedly reused history. The recovered corpus contains 1,272 SQLite files occupying about 196 GiB, with hundreds of related configurations and heavily gated workers. Replay sometimes reported large profits, but repeated searching made those results weak evidence without untouched walk-forward confirmation. The research documentation recognized overfitting, yet production candidates still reflected optimizer-shaped thresholds and many market-regime gates.

Repeated same-side buys amplified the consequence. The main worker made about six correlated bets per active cycle and could place as many as 24. Considering only its first settled trade per cycle would still have been unprofitable, but would have reduced the loss from about $21.38 to $3.54. The cycle, not the individual trade, was the meaningful independent exposure unit.

The durable lessons are:

- Evaluate strategies at executable fill prices, not the quote visible when a signal fires.
- Treat each five-minute cycle as one correlated outcome when measuring sample size and controlling exposure.
- Keep discovery, walk-forward screening, and untouched confirmation periods separate. Reusing one tape for many searches invalidates ordinary backtest confidence.
- Require hard per-cycle, daily, and account exposure limits before real trading.
- Enforce strategy odds limits in the submitted order itself.
- Prefer a small causal hypothesis with prospective evidence over a large collection of gates selected for historical P&L.
- A sophisticated replay and [[Autoresearch]] loop is only useful when its evaluator represents the real execution problem and is protected from repeated selection overfit.

The project is worth revisiting, but not by continuing the old gate search. A new attempt should begin from a different thesis about where an executable market advantage can exist and design its data collection, execution model, prospective test, and risk boundary around that thesis.

## Repositories and evidence

- Repository: `/home/tobias/code/poly-trader`

The recovered SQLite databases and trash snapshots that produced the numbers above are no longer on this machine. Treat those figures as the retrospective's record rather than as evidence a later agent can re-derive locally.
