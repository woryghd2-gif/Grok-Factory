# Review — Micron Technology (`mu`), GF-4

Review date: 2026-10-25. Read as a check on the four gates, after the model and the valuation had already been accepted. The standard is the Gate 4 list: required sections, sourced figures, statement ties, a three-year forecast that carries the thesis drivers, a readable price target, a stated WACC and terminal method, a sensitivity table, why-this-is-right, what-others-miss, pillars that name model lines, dated killing conditions, and an action that starts from the target.

## Checklist

| Check | Result | Where |
| --- | --- | --- |
| Research, model, valuation, and thesis are present, with the required sections | Pass | `research.md` sections 1–10. `valuation.md` sections 1–8. `thesis.md` sections 1–8. Segment, income, balance, and cash-flow files are the model. |
| Node map is in memory | Pass | Already in `research.md` section 1. Not copied into a second file. `INDEX.md` points at that section. |
| Material numbers are sourced or marked `not obtained` | Pass after the fixes below | Model and valuation cite the 10-K, the September 30, 2026 release, and the market sources in `valuation.md` section 8. The poll is sourced in `consensus.md`. Open items stay marked. |
| Income is the sum of the segments | Pass | `income.md` roll: segment gross profit minus unallocated COGS equals company gross profit in every year. `build_model.py` asserts it. |
| Net income, the cash roll, and assets = liabilities + equity | Pass | 89 asserts, re-run on this pass. Balance-sheet gap row is 0.0 in all six years. Ending cash equals the balance-sheet cash total. |
| Three-year forecast carries the thesis drivers | Pass | FY2027E–FY2029E are bits × ASP, the three-point HBM cost gap, and the −30% ASP cut in FY2029E. The 45% mid-cycle margin is the terminal year, and section 1 of the thesis says so. FY2029E gross margin stays 82.4%. |
| Price target is readable as the idea | Pass | $620.28 versus the $877.55 close, with the $257.27 gap and the fact that $877.55 is above the top printed sensitivity cell of $817. |
| WACC components and the terminal method are stated | Pass | `valuation.md` section 3. Each WACC input has a source or is `not obtained`. Terminal g is 3.0% inside a 4.0% cap. Terminal gross margin is 45%. Terminal value is 31.7% of enterprise value. |
| Sensitivity is present, base marked | Pass | Section 4. Primary grid is WACC against mid-cycle gross margin. The base cell is marked BASE. The g grid is the narrower one ($161 per share versus $290). |
| Why this is right, and what others miss | Pass | `thesis.md` sections 4 and 5. The poll behind section 5 is `consensus.md`. |
| Pillars name the model lines they move | Pass | Four pillars in section 3, each with the file and the line. |
| Killing conditions are falsifiable and dated | Pass after the date fix below | Five conditions. Each has a break rule and an overdue date. Exact future IR dates that the company has not announced are `not obtained`. |
| Action starts from the target | Pass | Section 8 sizes capital to $620.28 because the close is $257.27 above it. No rating and no buy, sell, long, short, or pass label. |

## Failures found, and what changed

1. **Korean-won sentence in the valuation.** The generated line read “Won closes are not translated.” A reader can take “Won” as a typo, so the reason those peer prices stay in won was unclear. `build_model.py` now says “Prices quoted in Korean won are not translated into dollars.” The markdown was regenerated. No figure changed. Asserts still 89. Price target still $620.28.

2. **Thesis section 4 was leaning on the street.** The first draft used published revenue and EPS to argue that the view is right. Those figures are not model lines. They now sit only in section 5 and in `consensus.md`. Section 4 stands on the guide the model already follows, the arithmetic that a −30% ASP cut leaves gross margin at 82.4%, the terminal rebuild, and the statement ties.

3. **Killing-condition dates did not match the sentence that introduced them.** The first dates were round mid-month marks, and the sentence called them about two weeks after the prior-year releases. The FQ2 mark was about four weeks, not two. The rule now written into section 6 is explicit: prior-year release or filing date, shifted by the right number of years, plus 14 days. Checked: 2026-03-18 → 2027-04-01, 2026-06-24 → 2027-07-08, 2026-09-30 → 2027-10-14, 2026-10-09 → 2027-10-23, and 40 days after 2026-11-27 plus 14 days → 2027-01-20.

4. **The contract-liability test was hair-trigger, and it skipped the repayment year.** Any one-dollar difference would have counted as a break, and the FY2029E repayment to $8,597 million was not itself a test. Section 6 now uses a stated $500 million band around $12,895 million before FY2029E and the same band around $8,597 million at the FY2029E year-end. The band is a check threshold, not a model output. The 70% FY2028E gross-margin threshold and the $40–65 billion FY2027E capex band are labeled the same way.

5. **Research section 10 said StockAnalysis is not a source, and the poll uses it.** That reads as a contradiction. The sentence now says those sites are not sources for Micron’s reported figures, and that published estimates live only in `consensus.md` and are not model inputs.

## What was checked and left as it is

- The sensitivity base cell prints **$620 BASE**. The target in section 1 is $620.28. The dollar rounding is the same display convention as the statements, which warn that rounded lines can differ by $1 million. The cell was not rewritten.
- Gate 1 figures were not re-derived. This pass confirmed the ten sections and the node map, and it did not reopen the accepted filing pack.
- The close is above every printed sensitivity cell. The highest cell is $817, which is $60.55 below $877.55. The thesis states that, so the “longer or higher peak” sentence is the reading of a gap the grid does not cover, not a fitted target.
- `models/mu/build_model.py` was re-run after the wording change: 89 asserts passed. WACC 14.80%, g 3.0%, terminal value 31.7% of enterprise value, 12-month value $620.28.

## Still `not obtained`, and load-bearing where noted

Load-bearing for the target, carried forward from `valuation.md` section 8: strategic-agreement floor prices, full-year FY2027E capex dollars, HBM revenue and the wafer trade ratio, the October 2026 implied equity risk premium, and a market yield on the notes (the debt weight is about 0.5%). Peer multiples other than Sandisk’s FY2026 set. Those multiples have a zero weight.

Load-bearing for the poll, not for the target: fiscal 2029 published revenue and EPS. The names behind the $361 and $3,000 targets. The official FQ1 FY2027 earnings date. Third-party calendars that name December 16 or December 23, 2026 were not confirmed by Micron IR and are not used as the date. The overdue mark is 2026-12-31.
