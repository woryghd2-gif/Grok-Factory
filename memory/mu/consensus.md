# Micron Technology, Inc. (`mu`) — published estimates

As of 2026-10-25. This file is the poll of what others publish. It is not a Micron filing and it is not an input to `models/mu/build_model.py`. Dollars are as printed on the page. A figure that was not on a retrieved page is `not obtained`.

The model’s own lines stay in `models/mu/`. Where this file sets a published estimate next to a model line, the model line is a pointer, and the difference is arithmetic tagged **[DEDUCTED]**.

## 1. Price targets

Source: StockAnalysis forecast page, data from S&P Global Market Intelligence, last updated 2026-10-23, last checked 2026-10-23. The page shows the regular-session close of $877.55 on 2026-10-23, 4:00 p.m. EDT. https://stockanalysis.com/stocks/mu/forecast/

| | Low | Average | Median | High |
| --- | --- | --- | --- | --- |
| 12-month target, 49 analysts | $361 | $1,562 | $1,550 | $3,000 |
| Page’s change versus the $877.55 close | −58.86% | +77.99% | +76.63% | +241.86% |

The page also prints a consensus rating label. This file records the label and does not adopt it. October 2026 count on that page: Strong Buy 36, Buy 9, Hold 3, Sell 1, Strong Sell 0, total 49.

Named targets on the same page, individual rows attributed to TipRanks:

| Date | Firm | Analyst | Their label | Target |
| --- | --- | --- | --- | --- |
| 2026-10-23 | Wedbush | Matt Bryson | Buy | $1,400 |
| 2026-10-22 | Fubon Securities | not named on the page | Buy | not obtained |
| 2026-10-22 | RBC Capital | Srini Pajjuri | Buy | $1,500 |
| 2026-10-22 | Needham | Quinn Bolton | Buy | $1,650 |
| 2026-10-18 | Mizuho Securities | Vijay Rakesh | Buy | $1,400 |

The analyst behind the $361 low and the analyst behind the $3,000 high: `not obtained` on the retrieved page.

A second page, Kaplio, printed an average of $1,588.85 from 12 targets in the last quarter, between $1,200 and $3,000, against the same $877.55 close. https://kaplio.com/ticker/MU/estimates That sample is smaller than the 49-analyst set and is not used as the average below. The $1,562 figure is the one the comparison uses.

## 2. Revenue and EPS

Two aggregators, retrieved 2026-10-25, agree on the annual averages. Yahoo Finance analysis, page displaying the 2026-10-23 close: https://finance.yahoo.com/quote/MU/analysis/ StockAnalysis financial forecast, same URL as section 1, with the note “EPS and Forward PE are based on non-GAAP adjusted numbers.”

| Item | Published average | Low | High | Analysts | Where printed |
| --- | --- | --- | --- | --- | --- |
| Revenue, fiscal 2027 | $275.51 billion | $212.4 billion (StockAnalysis); $212.42 billion (Yahoo) | $314.0 billion (StockAnalysis); $313.96 billion (Yahoo) | 41 | Both pages |
| Revenue, fiscal 2028 | $318.88 billion | $224.16 billion | $396.62 billion | 43 | Yahoo. StockAnalysis header prints the same average; the high and low for 2028 on that page are behind a paywall and are `not obtained` there |
| Non-GAAP EPS, fiscal 2027 | $176.58 | $161.00 | $214.70 | 35 on the EPS row; the revenue row says 41 | Both pages. Basis: StockAnalysis states non-GAAP. Yahoo’s year-ago EPS is $75.52, which is the non-GAAP FY2026A figure in `financials_raw.md`, not GAAP diluted EPS of $74.33 |
| Non-GAAP EPS, fiscal 2028 | $206.89 | $136 | $335.50 | 36 | Yahoo. StockAnalysis header prints the same average; high and low for 2028 are `not obtained` on that page |
| Revenue, quarter labeled Nov 2026 (FQ1 FY2027) | $61.74 billion | $58.06 billion | $65.61 billion | 34 | Yahoo only |
| Non-GAAP EPS, same quarter | $38.29 | $35.85 | $40.47 | 30 | Yahoo only. Year-ago EPS on the page is $4.78, the non-GAAP FQ1 FY2026A figure |
| Revenue, quarter labeled Feb 2027 | $67.06 billion | $58.85 billion | $76.04 billion | 32 | Yahoo only |
| Non-GAAP EPS, same quarter | $42.25 | $39.71 | $49.79 | 29 | Yahoo only |

Fiscal 2029 revenue and EPS: `not obtained`. StockAnalysis marks the 2029 columns as a paid tier. The Yahoo page retrieved has no 2029 column. A search snippet from a WSJ ratings page showed different annual EPS figures and was not fetched, so those figures are not used.

StockAnalysis also prints, for fiscal 2027, gross margin 86.99%, operating income $230.30 billion, net income $196.35 billion, and free cash flow $143.09 billion. The page’s fiscal 2026 net income of $84.97 billion matches GAAP net income of $84,969 million. The page’s fiscal 2026 EPS of $75.52 does not match GAAP diluted EPS of $74.33. EPS and net income on that page are therefore not one basis. This note does not divide one by the other.

The page’s fiscal 2026 free cash flow of $58.96 billion does not match the company’s adjusted free cash flow of $62,308 million. The fiscal 2027 free-cash-flow average is recorded and is not treated as the company’s definition.

Period label: StockAnalysis heads fiscal 2027 as ending August 31, 2027. The model’s FY2027E year-end is 2027-09-02, the Thursday closest to August 31. The averages are used as the street’s fiscal 2027, with that label difference stated.

## 3. Next to the model

Model lines are the rounded figures in `models/mu/income.md`, `segments.md`, and `cashflow.md`. Published dollars in billions are converted at 1 billion = 1,000 million.

| | Model | Published average | Difference (model − published) |
| --- | --- | --- | --- |
| FY2027E revenue | $269,187 million | $275,510 million | −$6,323 million, which is 2.3% below the average **[DEDUCTED]** 6,323 / 275,510. The model sits inside the published low-to-high range |
| FY2028E revenue | $325,951 million | $318,880 million | +$7,071 million, 2.2% above the average **[DEDUCTED]** |
| FY2027E gross margin | 87.6% GAAP | 86.99% | about 0.6 percentage point higher on the model |
| FY2027E operating income | $225,137 million GAAP EBIT | $230,300 million | −$5,163 million **[DEDUCTED]** |
| FY2027E net income | $195,835 million GAAP | $196,350 million | −$515 million **[DEDUCTED]** |
| FY2027E EPS | $170.29 GAAP diluted | $176.58 non-GAAP | −$6.29 per share, different basis. The FY2026A gap between non-GAAP $75.52 and GAAP $74.33 was $1.19, so the bases are not far apart in the last reported year, and they are still not the same line |
| FY2028E EPS | $211.46 GAAP diluted | $206.89 non-GAAP | +$4.57 per share, different basis |
| FY2027E free cash flow | $157,966 million, operating cash flow minus net capex | $143,090 million, page definition | +$14,876 million **[DEDUCTED]**, definitions differ as stated above |
| FQ1 FY2027E revenue | $61,500 million, the guide midpoint | $61,740 million | −$240 million. The published average is inside the company’s $61,500 ± $1,500 band |
| 12-month value | $620.28, `valuation.md` section 1 | $1,562 average target | −$941.72 **[DEDUCTED]** 1,562 − 620.28 |

FY2029E published revenue and EPS remain `not obtained`, so there is no street line next to the model’s FY2029E revenue of $264,275 million or GAAP diluted EPS of $167.33.

## 4. What the poll is being used for

The near-term averages sit next to the model’s peak years. The published 12-month targets sit far above the model’s 12-month value. That split is the input to `thesis.md` section 5. Nothing in this file changes the model, the WACC, or the target.
