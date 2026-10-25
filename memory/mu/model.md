# Micron Technology, Inc. (`mu`) — model pointer

As of 2026-10-25. This file points at the Gate 2 and Gate 3 outputs. It does not restate their figures. Rebuild with `python3 models/mu/build_model.py`. The script writes the files below and asserts the ties.

| File | What it is |
| --- | --- |
| [models/mu/build_model.py](../../models/mu/build_model.py) | Segment drivers, three statements, DCF, comps, and the asserts. |
| [models/mu/segments.md](../../models/mu/segments.md) | CMBU, CDBU, MCBU, AEBU, and All other. |
| [models/mu/income.md](../../models/mu/income.md) | Consolidated income statement built from the segment sum. |
| [models/mu/balance.md](../../models/mu/balance.md) | Balance sheet. Assets equal liabilities plus equity in every year. |
| [models/mu/cashflow.md](../../models/mu/cashflow.md) | Cash flow. Ending cash equals the balance sheet. |
| [models/mu/valuation.md](../../models/mu/valuation.md) | 12-month value per share, DCF, sensitivity, comps, weights, sources. |

Historical years are FY2024A–FY2026A from `memory/mu/financials_raw.md`. Forecast years are FY2027E–FY2029E. The price target is the DCF rolled forward one year. It is not fitted to a rating, and the market price is not an input to it.
