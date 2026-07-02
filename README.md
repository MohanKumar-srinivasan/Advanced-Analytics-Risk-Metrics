## Advanced Analytics + Risk Metrics

Risk and behavioral analytics layer built on top of the mutual fund star-schema
database, covering tail risk, rolling performance, investor cohorts, SIP
retention risk, fund recommendations, and portfolio concentration.

### What's inside
| File | Description |
|---|---|
| `Advanced_Analytics.ipynb` | Full analysis notebook — all 6 tasks + 5 insights |
| `var_cvar_report.csv` | Historical VaR & CVaR (95%) for all 40 schemes |
| `recommender.py` | Standalone fund recommender (top 3 by Sharpe ratio, filtered by risk appetite) |
| `rolling_sharpe_chart.png` | 90-day rolling Sharpe ratio, 5 key funds |

### Methodology
- **VaR (95%)**: 5th percentile of daily returns. **CVaR (95%)**: mean of returns at or below VaR — captures tail severity.
- **Rolling Sharpe**: `excess_returns.rolling(90).mean() / returns.rolling(90).std() * √252`, risk-free rate assumed at 6% p.a.
- **SIP continuity**: investors with 6+ SIP transactions; flagged "at-risk" if average gap between SIPs exceeds 35 days.
- **HHI**: `Σ(sector_weight²)` per fund — higher values indicate more concentrated sector exposure.

### Run it
```bash
python3 recommender.py "Moderate"   # or "Low" / "High"
jupyter nbconvert --to notebook --execute Advanced_Analytics.ipynb
```
