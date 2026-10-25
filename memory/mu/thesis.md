# Micron Technology, Inc. (`mu`) — thesis

As of 2026-10-25. Every claim about the business or the value is a line in `models/mu/`. If a figure is not in those files, it is not a claim here. Units match the model: US$ millions except per share. Years marked E are the model.

## 1. Claim

The model’s 12-month value is **$620.28 per share** (`valuation.md` section 1, horizon 2027-10-25). The close recorded in that section is **$877.55** on 2026-10-23. The difference is **$257.27** per share (877.55 − 620.28). The same section’s value on the valuation date, before the one-year equity roll, is $540.56, which is $336.99 below that close.

That gap is the model saying the close prices a longer or higher peak than the mid-cycle normalization. The explicit years already keep the peak. `income.md` gross margin is 87.6% in FY2027E, 87.4% in FY2028E, and 82.4% in FY2029E after the −30% ASP cut. The normalization is the terminal year: `valuation.md` sets that year’s GAAP gross margin at 45%, and the present value of the terminal value is 31.7% of enterprise value ($182,591 of $576,063).

The close also sits above every cell in the printed sensitivity grid. The highest cell is $817, at an 11.80% WACC and a 55% mid-cycle gross margin. Against that printed cell the close is still $60.55 higher (877.55 − 817). A peak long enough, or a mid-cycle margin high enough, to support $877.55 is a case the model does not print.

The close is the print this claim is measured against. `valuation.md` section 1 states that the close is not an input to the target.

## 2. Price target

The target, the horizon, the share count, and the bridge are in [`models/mu/valuation.md`](../../models/mu/valuation.md) section 1 and section 2. This section does not restate them.

## 3. Pillars

### Peak years stay in the forecast; the 45% margin is the terminal year

Mechanism. Cash cost is a small share of the peak price, so a 30% ASP cut in FY2029E leaves gross margin in the low 80s. `valuation.md` therefore does not grow FY2029E at g. It rebuilds a mid-cycle year whose GAAP gross margin is 45%, five points above the FY2025A gross margin of 39.8%, because the strategic-agreement floors were not obtained.

Magnitude. Present value of FY2027E–FY2029E unlevered free cash flow is $393,471. Present value of the terminal value is $182,591, **31.7% of enterprise value**. The 12-month value in section 1 is the equity claim on that enterprise value, rolled one year.

Lines moved. `income.md` gross margin for FY2027E, FY2028E, and FY2029E. `valuation.md` terminal method, the FY2030E column of the unlevered free-cash-flow table ($31,912), and the terminal-value percent of enterprise value.

### FY2027E and FY2028E revenue is still a price year on top of bits

Mechanism. `segments.md` sets FY2027E revenue as quarterly bits × ASP, scaled onto the guided $61,500 million first quarter, then reads ASP as the residual of annual bits. The residuals are CMBU ASP +51.0% on bits +28%, CDBU ASP +77.4% on bits +40%, MCBU ASP +53.3% on bits +6%, AEBU ASP +66.6% on bits +25%. HBM mix is not a revenue split. It is the three-point gap in cash-cost deflation: CMBU −5% versus CDBU and MCBU −8%. FY2028E holds the FY2027E exit price. The ASP change versus the FY2027E average is only the intra-year ramp, +2.9% to +3.5% by segment.

Magnitude. Company revenue goes from $133,188 million in FY2026A to $269,187 million in FY2027E and $325,951 million in FY2028E (`income.md`).

Lines moved. `segments.md` driver row for each segment. `income.md` revenue.

### The FY2029E price cut does not do the normalization

Mechanism. `income.md` states that the −30% ASP cut only moves gross margin from the high 80s to about 82%, because cash cost is a small share of the peak price. The mid-cycle reset is the terminal year, not FY2029E.

Magnitude. FY2029E revenue is $264,275 million, gross margin 82.4%, EBIT $204,566 million. Unlevered free cash flow that year is $160,785 million, against $31,912 million in the normalized year (`valuation.md` unlevered free-cash-flow table).

Lines moved. `income.md` FY2029E revenue, gross margin, and EBIT. `segments.md` FY2029E driver, ASP −30% on CMBU, CDBU, MCBU, and AEBU. `valuation.md` FY2029E and FY2030E unlevered free cash flow.

### The explicit cash is already in the value, so the gap is the duration of the margin

Mechanism. Free cash flow in the explicit years is large after the capex step-up: $157,966 million, $208,396 million, and $181,967 million (`cashflow.md`). The bridge adds the September 3, 2026 cash, restricted cash, and marketable investments once ($73,480 million) and subtracts debt ($5,179 million), noncurrent customer contract liabilities ($12,895 million), and the noncurrent tax payable ($9,820 million). Interest income of $6,730 million, $14,782 million, and $23,270 million is inside net income and outside unlevered free cash flow (`income.md`, `valuation.md` section 2). Ending cash of $576,917 million in FY2029E is the roll of that explicit cash. It is not a second claim on top of the present value.

Magnitude. Enterprise value $576,063 million. Equity value at 2026-10-25 is the bridge result in `valuation.md` section 2. The primary sensitivity range is $290 per share across mid-cycle gross margin, against $161 per share across g (`valuation.md` section 4). Margin duration moves the target more than g does.

Lines moved. `cashflow.md` free cash flow and ending cash. `income.md` interest income. `valuation.md` bridge table and section 4.

## 4. Why this view is right

The explicit forecast follows the company’s own near-term statements as they are written into the model: FQ1 revenue at the $61,500 million midpoint, each later FY2027E quarter higher than the one before it, FY2027E gross margin above the guided floor of about 85.95% (the model prints 87.6% and the script asserts the floor), and a more moderate price path after FQ1 that still produces the ASP residuals above. Granting that peak is what makes the terminal year do the work. A model that cut prices in FY2027E would be arguing with the guide. This one does not.

The −30% ASP cut is then not enough, on the model’s own arithmetic, to restore a mid-cycle margin. Cash cost has to be rebuilt against a lower price before gross margin can land at 45%. That is why the terminal year is a rebuilt year and why g, capped at 4.0% and set at 3.0%, moves the 12-month value by less than the margin grid.

The statements tie. `income.md` builds company gross profit as the sum of segment gross profit minus unallocated cost of goods sold. `balance.md` shows assets equal to liabilities plus equity in every year. `cashflow.md` rolls ending cash to the balance-sheet cash total. Those ties are what the 12-month value sits on. The capitalization of the peak is the 45% terminal and the 31.7% weight of terminal value inside enterprise value.

## 5. What others miss or get wrong

The poll is `consensus.md`. Summarized here without a second model:

Published 12-month targets average $1,562, with a median of $1,550, a low of $361, and a high of $3,000 (S&P Global, via the StockAnalysis page last updated 2026-10-23). Named targets dated October 18–23, 2026 are $1,400, $1,500, $1,650, and $1,400. The average target is $941.72 above this model’s 12-month value. The close of $877.55 is between the model and that average, and it is still above the top of the printed grid.

What those targets miss is the line the model had to add because a 30% price cut does not normalize the margin. Street fiscal 2027 and fiscal 2028 revenue and EPS, on the pages retrieved, describe the same two peak years the model has. Fiscal 2029 published revenue and EPS are `not obtained`. The model’s first down year, FY2029E revenue $264,275 million and gross margin still 82.4%, is the year the free columns on those pages do not show, and the year after that is the 45% rebuild those targets do not print.

A peak-year multiple does the same thing from the other direction. `valuation.md` section 6 records Sandisk’s trailing P/E of 16.78× and states that applying it to Micron’s FY2026A diluted EPS of $74.33 is an unweighted arithmetic and is not the target. Comps carry a zero weight because the other peers’ multiples are `not obtained`.

The low published target of $361 sits below the model. The average target, and the close, both require a longer or higher peak than the 45% terminal, and the close is outside the cases in section 4 of the valuation.

## 6. Killing conditions

Each one names the line that breaks and the date the check happens. An exact company announcement that was not in the model is marked `not obtained`, and the overdue date is the date used so the check cannot slip.

1. **FQ1 FY2027E revenue or the gross-margin floor.** False if reported FQ1 revenue is outside $60,000–$63,000 million (the $61,500 ± $1,500 guide the model’s $61,500 quarter sits on), or if FQ1 GAAP gross margin is below about 85.95%. The year-margin line that depends on this floor is `income.md` FY2027E gross margin of 87.6%. Check: the FQ1 FY2027 earnings release. The company date is `not obtained` as of 2026-10-25. Prior FQ1 releases were 2024-12-18 and 2025-12-17 (`research.md` section 10), which is why the window is December. The check is overdue if no release has appeared by **2026-12-31**.

2. **Sequential growth through FY2027E.** False if a later quarter’s revenue is less than or equal to the prior quarter. The model path is $61,500, $65,196, $69,140, $73,351 million (`segments.md`). Check: the FQ2, FQ3, and FQ4 FY2027 releases. Official dates are `not obtained`. Overdue dates are the prior-year release date plus one year plus 14 days (`research.md` section 10): **2027-04-01** (from 2026-03-18), **2027-07-08** (from 2026-06-24), and **2027-10-14** (from 2026-09-30).

3. **Contract-liability path.** False if a filed balance sheet shows noncurrent customer contract liabilities more than $500 million away from the model path: above $13,395 million before FY2029E (new deposits the model sets to zero), or below $12,395 million before FY2029E (a repayment the model dates to that year). The $500 million band is the materiality for this check. A smaller difference does not break the line. The model holds $12,895 million through FY2028E and repays one-third, to $8,597 million, in FY2029E (`balance.md`). At that year-end the same $500 million band applies around $8,597 million. First check: the FQ1 FY2027 Form 10-Q. The FY2027 quarter-end date is `not obtained`. The overdue date is **2027-01-20**, which is 40 days after the prior-year quarter-end anniversary of 2026-11-27, plus 14 days. Annual checks use the FY2026 Form 10-K filing date of 2026-10-09 plus one year plus 14 days: FY2027 Form 10-K overdue **2027-10-23**, FY2028 Form 10-K overdue **2028-10-23**, FY2029 Form 10-K overdue **2029-10-23**.

4. **The price path.** False if the company reports DRAM ASP or NAND ASP down for FY2027E, or if FY2028E GAAP gross margin prints below 70% while the model still has 87.4%. The 70% line is the threshold for this check. It is not a model output. Either print means the normalization arrived inside the explicit window and the 45% terminal is built on the wrong base. ASP check: FY2027 Form 10-K MD&A, overdue **2027-10-23** on the same 10-K rule as condition 3. Margin check: FY2028 results release, overdue **2028-10-14**, the FY2026 results date of 2026-09-30 plus two years plus 14 days.

5. **FY2027E net capex.** False if reported company net capex is above $65,000 million or below $40,000 million. That band is the threshold for this check. It is wider than a rounding difference and it is not a company guide. The model uses $55,000 million, of which only the $25,000 million first half is guided (`cashflow.md`). Check: the FY2027 results release, overdue **2027-10-14** on the same results-release rule as condition 2.

## 7. Catalysts

Dates are included only where the model states them. An undated item stays undated.

- **2026-12-09.** Discretionary repurchase capacity of $35.16 billion becomes available (`balance.md`). The forecast includes none of that capacity. `valuation.md` section 7 says spending it changes the share count and the cash in the bridge.
- **FQ1 FY2027E release.** Date `not obtained`. This is the print for killing conditions 1 and the start of condition 2. The numerical content is already in the model: revenue midpoint $61,500 million and the gross-margin floor of about 85.95%.
- **Mid-calendar 2027.** ID1 first wafers, the event `segments.md` uses for MCBU bit growth stepping up to +10% in FY2028E. No day is given.
- **Late calendar 2028.** ID2, Hiroshima, and the Singapore NAND fab start. That is the cleanroom timing `segments.md` gives for the FY2029E −30% ASP cut. No day is given.
- **Fiscal year-ends 2027-09-02, 2028-08-31, and 2029-08-30.** The dates in `valuation.md` at which each explicit unlevered free cash flow is assumed to arrive, and the statement dates the explicit forecast is tested against.

First New York wafers are not given a date in the model files. The cash-flow note says New York is still being built through the explicit years. The date is `not obtained` here.

## 8. Action

The decision value is the 12-month target in `valuation.md` section 1: $620.28 per share at 2027-10-25. Worked backward from that figure, the October 23 close of $877.55 pays $257.27 per share more than the target. At that close, this model underwrites none of the extra $257.27. Capital that uses the model is sized to $620.28. The amount of any existing holding above what $620.28 supports is the amount the mid-cycle case does not underwrite.

The size changes when the price meets the target, or when a check in section 6 moves the lines that set it. The lines with the largest recorded effect are the mid-cycle gross margin and, second, the WACC (`valuation.md` section 4 and section 7).
