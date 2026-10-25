#!/usr/bin/env python3
"""Micron (mu) Gate 2–3 model.

Historical figures are the FY2026 10-K and the Gate 1 pack in memory/mu.
Forecast years are FY2027E–FY2029E. Revenue is bits x ASP by segment.
The price target is the DCF, rolled one year. The market price is not an input.

Run: python3 models/mu/build_model.py
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent

ASOF = "2026-10-25"
VAL_DATE = date(2026, 10, 25)
SEGS = ("CMBU", "CDBU", "MCBU", "AEBU", "OTHER")
YEARS = ("FY2024A", "FY2025A", "FY2026A", "FY2027E", "FY2028E", "FY2029E")
HIST = ("FY2024A", "FY2025A", "FY2026A")
FCST = ("FY2027E", "FY2028E", "FY2029E")

# --- Market inputs (sourced in valuation.md). Not used to fit a target. ---
PRICE_MU = 877.55  # close 2026-10-23; reference only
RF_10Y = 0.0500  # Treasury par yield 2026-10-23
RF_1Y = 0.0444  # cash yield: 1-year Treasury par yield, same curve
BETA = 2.23  # Yahoo Finance 5-year monthly vs S&P 500
ERP = 0.0442  # Damodaran implied US ERP, 2026-07-01
TAX_FCST = 0.155  # company FY2027 guide, held for FY2028–FY2030
G = 0.030  # terminal real+inflation cap is 4%; base is inside that cap
G_CAP = 0.040  # FOMC Sep 2026 longer-run real GDP 2% + PCE 2%
NORM_GM = 0.45  # mid-cycle gross margin; see valuation.md
WEIGHT_DCF = 1.0
WEIGHT_COMPS = 0.0  # comps set is incomplete; weight chosen before the DCF result

FQ4_FY26_REV = {"CMBU": 16283.0, "CDBU": 18002.0, "MCBU": 13114.0, "AEBU": 6824.0, "OTHER": 6.0}
FQ1_GUIDE = 61500.0  # GAAP revenue midpoint, $ millions
FQ1_SEQ = {"CMBU": 1.12, "CDBU": 1.18, "MCBU": 1.08, "AEBU": 1.12, "OTHER": 1.00}
SEQ_BITS = {"CMBU": 0.06, "CDBU": 0.04, "MCBU": 0.01, "AEBU": 0.03, "OTHER": 0.00}
SEQ_ASP = {"CMBU": 0.025, "CDBU": 0.020, "MCBU": 0.020, "AEBU": 0.020, "OTHER": 0.00}

# Annual bit growth. FY2027E is the judgment; implied ASP is the identity residual.
BITS = {
    "FY2027E": {"CMBU": 0.28, "CDBU": 0.40, "MCBU": 0.06, "AEBU": 0.25, "OTHER": 0.00},
    "FY2028E": {"CMBU": 0.22, "CDBU": 0.20, "MCBU": 0.10, "AEBU": 0.12, "OTHER": 0.00},
    "FY2029E": {"CMBU": 0.18, "CDBU": 0.18, "MCBU": 0.12, "AEBU": 0.10, "OTHER": 0.00},
}
# Cash cost per bit. CMBU declines less because HBM uses more wafers per bit.
UNIT_COST = {
    "FY2027E": {"CMBU": -0.05, "CDBU": -0.08, "MCBU": -0.08, "AEBU": -0.06, "OTHER": 0.00},
    "FY2028E": {"CMBU": -0.05, "CDBU": -0.08, "MCBU": -0.08, "AEBU": -0.06, "OTHER": 0.00},
    "FY2029E": {"CMBU": -0.04, "CDBU": -0.06, "MCBU": -0.06, "AEBU": -0.05, "OTHER": 0.00},
}
ASP_FY29 = -0.30  # first normalization year, after the late-calendar-2028 cleanrooms

# FY2027E net capex: guided 1H $25B; 2H not guided. Model: 2H = $30B.
NET_CAPEX = {"FY2027E": 55000.0, "FY2028E": 46000.0, "FY2029E": 40000.0}
GROSS_PER_NET = 30712.0 / 27367.0  # FY2026A gross PPE spend / company net capex

SBC_FY26 = 1333.0
SBC_GROWTH = 0.08
SBC_COGS_SHARE = 528.0 / 1282.0  # Note 14 location
WITHHOLD_RATE = 0.45
DIV_PER_SHARE = 0.60  # four quarters at the $0.15 rate declared 2026-09-30
BASIC_SHARES = 1131.0  # outstanding at 2026-09-03, held: no discretionary buyback
DILUTED = {"FY2024A": 1118.0, "FY2025A": 1125.0, "FY2026A": 1143.0, "FY2027E": 1150.0, "FY2028E": 1150.0, "FY2029E": 1150.0}

LEASE_RATE = 0.0471
LEASE_PAY = (577.0, 560.0, 500.0, 349.0)  # FY27, FY28, FY29, and the next year for the current portion
NOTES_CV = 997 + 70 + 175 + 213 + 135 + 219 + 497 + 486  # 2792
LEASE0 = 2387.0
NOTE_COUPON = (
    1000 * 0.02703
    + 71 * 0.05650
    + 176 * 0.05875
    + 215 * 0.05875
    + 136 * 0.05800
    + 220 * 0.06050
    + 500 * 0.03366
    + 490 * 0.03477
)

CASH_COGS_FY26 = {
    "CMBU": 8802.0 - 3335.0,
    "CDBU": 6031.0 - 2237.0,
    "MCBU": 6413.0 - 2490.0,
    "AEBU": 3891.0 - 1431.0,
    "OTHER": 19.0 - 6.0,
}
DA_FY26 = {"CMBU": 3335.0, "CDBU": 2237.0, "MCBU": 2490.0, "AEBU": 1431.0, "OTHER": 6.0}
# FY2026A unallocated depreciation was $4. It is folded into the segment weights so segment depreciation sums to company depreciation.
DA_WEIGHT = {k: v / sum(DA_FY26.values()) for k, v in DA_FY26.items()}

REV_HIST = {
    "FY2024A": {"CMBU": 3792.0, "CDBU": 4984.0, "MCBU": 11667.0, "AEBU": 4631.0, "OTHER": 37.0},
    "FY2025A": {"CMBU": 13524.0, "CDBU": 7229.0, "MCBU": 11859.0, "AEBU": 4753.0, "OTHER": 13.0},
    "FY2026A": {"CMBU": 43085.0, "CDBU": 37592.0, "MCBU": 36601.0, "AEBU": 15886.0, "OTHER": 24.0},
}
GP_HIST = {
    "FY2024A": {"CMBU": 1115.0, "CDBU": 1346.0, "MCBU": 1445.0, "AEBU": 1033.0, "OTHER": 17.0},
    "FY2025A": {"CMBU": 7657.0, "CDBU": 3234.0, "MCBU": 3209.0, "AEBU": 1187.0, "OTHER": -1.0},
    "FY2026A": {"CMBU": 34283.0, "CDBU": 31561.0, "MCBU": 30188.0, "AEBU": 11995.0, "OTHER": 5.0},
}
OI_HIST = {
    "FY2024A": {"CMBU": 244.0, "CDBU": 255.0, "MCBU": -1.0, "AEBU": 432.0, "OTHER": 18.0},
    "FY2025A": {"CMBU": 6129.0, "CDBU": 2180.0, "MCBU": 1981.0, "AEBU": 557.0, "OTHER": -1.0},
    "FY2026A": {"CMBU": 31225.0, "CDBU": 29539.0, "MCBU": 29208.0, "AEBU": 11217.0, "OTHER": 2.0},
}
UNALLOC_COGS_HIST = {"FY2024A": -657.0, "FY2025A": 413.0, "FY2026A": 528.0}

# Reported income statement. Tax and interest expense stored signed (expense negative).
IS_HIST = {
    "FY2024A": dict(rev=25111, cogs=19498, gp=5613, rd=3430, sga=1129, other_op=-250, ebit=1304, da=7780, int_inc=529, int_exp=-562, other_nonop=-31, pretax=1240, tax=-451, equity=-11, ni=778, eps=0.70),
    "FY2025A": dict(rev=37378, cogs=22505, gp=14873, rd=3798, sga=1205, other_op=100, ebit=9770, da=8352, int_inc=496, int_exp=-477, other_nonop=-135, pretax=9654, tax=-1124, equity=9, ni=8539, eps=7.59),
    "FY2026A": dict(rev=133188, cogs=25684, gp=107504, rd=5650, sga=1947, other_op=567, ebit=99340, da=9503, int_inc=1084, int_exp=-106, other_nonop=-647, pretax=99671, tax=-14761, equity=59, ni=84969, eps=74.33),
}

# Cash and restricted cash use the cash-flow-statement total.
# FY2024A restricted = 7,052 − 7,041 = 11, deducted. FY2025A $4 and FY2026A $27 are Note 4.
BS_HIST = {
    "FY2024A": dict(cash_eq=7041, restricted=11, sti=1065, rec=6615, inv=8875, oca=765, lti=1046, ppe=39749, gw=1150, onca=3099, ap=7299, debt_cur=431, contract_cur=766, ocl=752, debt_lt=12966, unearned=550, contract=141, oncl=1380, cs=125, apic=12115, re=40877, ts=-7852, aoci=-134),
    "FY2025A": dict(cash_eq=9642, restricted=4, sti=665, rec=9265, inv=8355, oca=910, lti=1629, ppe=46590, gw=1150, onca=4588, ap=9649, debt_cur=560, contract_cur=26, ocl=1219, debt_lt=14017, unearned=1018, contract=142, oncl=2002, cs=127, apic=13339, re=48583, ts=-7852, aoci=-32),
    "FY2026A": dict(cash_eq=38364, restricted=27, sti=5070, rec=36197, inv=10372, oca=1040, lti=30019, ppe=63310, gw=1150, onca=10339, ap=22605, debt_cur=491, contract_cur=0, ocl=4386, debt_lt=4688, unearned=786, contract=12895, oncl=11659, cs=128, apic=14974, re=131851, ts=-8502, aoci=-73),
}
# Reported cash-flow lines. Working-capital lines are signed as in the 10-K (increase in an asset is negative).
CF_HIST = {
    "FY2024A": dict(ni=778, da=7780, sbc=833, rec=-3581, inv=-488, ap=1915, ocl=989, oncl=76, other=205, ocf=8507, capex_gross=8386, capex_net=None, deposits=0, debt_issued=999, debt_repay=1897, withhold=233, buyback=300, div=513, other_fin=102, fx=40, net=-1604, cash0=8656, cash1=7052),
    "FY2025A": dict(ni=8539, da=8352, sbc=972, rec=-1776, inv=520, ap=862, ocl=-272, oncl=381, other=-53, ocf=17525, capex_gross=15857, capex_net=13804, deposits=0, debt_issued=4430, debt_repay=4619, withhold=340, buyback=0, div=522, other_fin=201, fx=6, net=2594, cash0=7052, cash1=9646),
    "FY2026A": dict(ni=84969, da=9503, sbc=1333, rec=-25206, inv=-2017, ap=8707, ocl=3141, oncl=9633, other=-388, ocf=89675, capex_gross=30712, capex_net=27367, deposits=12747, debt_issued=0, debt_repay=10043, withhold=1127, buyback=650, div=610, other_fin=313, fx=81, net=28745, cash0=9646, cash1=38391),
}
FCF_COMPANY = {"FY2025A": 3721.0, "FY2026A": 62308.0}  # OCF − net capex, as printed
INVESTING_CF = {"FY2024A": -8309.0, "FY2025A": -14087.0, "FY2026A": -61641.0}

OTHER_AR = 36197.0 - 31793.0  # government incentives, taxes, other; held flat
TRADE_AP_RATIO = 3518.0 / 25684.0
PPE_AP_RATIO = 8618.0 / 30712.0
COMP_BASE = 4447.0 / (5650.0 + 1947.0)
TAX_PAYABLE_NC = 9820.0  # 10-K: $9.82 billion noncurrent income taxes payable at 2026-09-03


def fy_end(year: int) -> date:
    aug31 = date(year, 8, 31)
    best = None
    for delta in range(-3, 4):
        cand = aug31 + timedelta(days=delta)
        if cand.weekday() == 3:
            if best is None or abs(delta) < abs((best - aug31).days):
                best = cand
    return best


def cash_restr(bs: dict) -> float:
    return bs["cash_eq"] + bs["restricted"]


def total_assets(bs: dict) -> float:
    return (
        cash_restr(bs)
        + bs["sti"]
        + bs["rec"]
        + bs["inv"]
        + bs["oca"]
        + bs["lti"]
        + bs["ppe"]
        + bs["gw"]
        + bs["onca"]
    )


def total_liab(bs: dict) -> float:
    return (
        bs["ap"]
        + bs["debt_cur"]
        + bs["contract_cur"]
        + bs["ocl"]
        + bs["debt_lt"]
        + bs["unearned"]
        + bs["contract"]
        + bs["oncl"]
    )


def total_equity(bs: dict) -> float:
    return bs["cs"] + bs["apic"] + bs["re"] + bs["ts"] + bs["aoci"]


def nwc(bs: dict) -> float:
    return bs["rec"] + bs["inv"] + bs["oca"] - bs["ap"] - bs["ocl"] - bs["contract_cur"]


def fmt(x, d=0):
    if x is None:
        return "not obtained"
    sign = "-" if x < 0 else ""
    q = abs(x)
    if d == 0:
        body = f"{q:,.0f}"
    else:
        body = f"{q:,.{d}f}"
    return sign + body


def pct(x, d=1):
    if x is None:
        return "n.m."
    return f"{x * 100:.{d}f}%"


def md_table(headers, rows):
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out)


def year_frac(end: date) -> float:
    return (end - VAL_DATE).days / 365.25


def build_fy27_quarters():
    """FQ1 is scaled to the $61.5B guide. Later quarters are bits x ASP."""
    raw = {s: FQ4_FY26_REV[s] * FQ1_SEQ[s] for s in SEGS}
    scale = FQ1_GUIDE / sum(raw.values())
    q = {1: {s: raw[s] * scale for s in SEGS}}
    bit_idx = {s: 1.0 for s in SEGS}
    asp_idx = {s: 1.0 for s in SEGS}
    for k in (2, 3, 4):
        q[k] = {}
        for s in SEGS:
            if s == "OTHER":
                bit_idx[s] = 1.0
                asp_idx[s] = 1.0
                q[k][s] = q[k - 1][s]
            else:
                bit_idx[s] *= 1.0 + SEQ_BITS[s]
                asp_idx[s] *= 1.0 + SEQ_ASP[s]
                q[k][s] = q[1][s] * bit_idx[s] * asp_idx[s]
    # Volume-weighted exit ASP versus the FY2027E average, by segment.
    exit_vs_avg = {}
    for s in SEGS:
        if s == "OTHER":
            exit_vs_avg[s] = 1.0
            continue
        b, a, w = 1.0, 1.0, 0.0
        weighted = 0.0
        for _ in range(4):
            weighted += a * b
            w += b
            b *= 1.0 + SEQ_BITS[s]
            a *= 1.0 + SEQ_ASP[s]
        # The loop advanced one step past Q4. Recompute cleanly.
    exit_vs_avg = {}
    for s in SEGS:
        if s == "OTHER":
            exit_vs_avg[s] = 1.0
            continue
        weights = []
        asps = []
        b = 1.0
        a = 1.0
        for _ in range(4):
            weights.append(b)
            asps.append(a)
            b *= 1.0 + SEQ_BITS[s]
            a *= 1.0 + SEQ_ASP[s]
        avg = sum(x * y for x, y in zip(asps, weights)) / sum(weights)
        exit_vs_avg[s] = asps[-1] / avg
    annual = {s: sum(q[k][s] for k in (1, 2, 3, 4)) for s in SEGS}
    return q, annual, scale, exit_vs_avg


def operating_balances(revenue, cogs, gross_capex, tax_expense, rd, sga, q4_revenue):
    trade_ar = revenue * 60.0 / 365.0
    rec = trade_ar + OTHER_AR
    inv = cogs * 142.0 / 365.0
    trade_ap = cogs * TRADE_AP_RATIO
    ppe_ap = gross_capex * PPE_AP_RATIO
    tax_ap = 0.25 * tax_expense
    comp = (rd + sga) * COMP_BASE
    ap = trade_ap + ppe_ap + tax_ap + comp + 396.0
    ocl = 0.08 * q4_revenue
    return rec, inv, ap, ocl


def lease_step(cv: float, payment: float):
    interest = cv * LEASE_RATE
    principal = payment - interest
    if principal <= 0:
        raise AssertionError("lease principal was not positive")
    return interest, principal, cv - principal


def forecast_statements(q_annual, exit_vs_avg, fy27_q4):
    """Return forecast year dicts with IS, BS, CF, and segment detail."""
    rev = {s: REV_HIST["FY2026A"][s] for s in SEGS}
    cash_cogs = dict(CASH_COGS_FY26)
    ppe = BS_HIST["FY2026A"]["ppe"]
    lease_cv = LEASE0
    re = BS_HIST["FY2026A"]["re"]
    apic = BS_HIST["FY2026A"]["apic"]
    ts = BS_HIST["FY2026A"]["ts"]
    contract = BS_HIST["FY2026A"]["contract"]
    cash_r = cash_restr(BS_HIST["FY2026A"])
    sti = BS_HIST["FY2026A"]["sti"]
    lti = BS_HIST["FY2026A"]["lti"]
    restricted = BS_HIST["FY2026A"]["restricted"]
    sbc = SBC_FY26
    years = {}
    prev_label = "FY2026A"

    for i, label in enumerate(FCST):
        rev_new = {}
        cash_new = {}
        implied_asp = {}
        for s in SEGS:
            if label == "FY2027E":
                rev_new[s] = q_annual[s]
                if s == "OTHER" or rev[s] == 0 or BITS[label][s] == -1:
                    implied_asp[s] = 0.0
                else:
                    implied_asp[s] = (rev_new[s] / rev[s]) / (1.0 + BITS[label][s]) - 1.0
            elif label == "FY2028E":
                # Hold the FY2027E exit price. The increase versus the FY2027E average is only that ramp.
                implied_asp[s] = exit_vs_avg[s] - 1.0
                rev_new[s] = rev[s] * (1.0 + BITS[label][s]) * exit_vs_avg[s]
            else:
                implied_asp[s] = 0.0 if s == "OTHER" else ASP_FY29
                rev_new[s] = rev[s] * (1.0 + BITS[label][s]) * (1.0 + implied_asp[s])
            cash_new[s] = cash_cogs[s] * (1.0 + BITS[label][s]) * (1.0 + UNIT_COST[label][s])

        revenue = sum(rev_new.values())
        net_capex = NET_CAPEX[label]
        da = 0.16 * ppe + 0.08 * net_capex
        sbc = sbc * (1.0 + SBC_GROWTH)
        sbc_cogs = sbc * SBC_COGS_SHARE
        cogs = sum(cash_new.values()) + da + sbc_cogs
        gp = revenue - cogs
        if label == "FY2027E":
            other_op = 70.0
            rd_sga = (5650.0 + 1947.0 + 567.0 + 2500.0) - other_op
            # 80% of the R&D+SG&A increase vs FY2026A goes to R&D (labs and incentive pay).
            rd_sga_fy26 = 5650.0 + 1947.0
            incr = rd_sga - rd_sga_fy26
            rd = 5650.0 + 0.80 * incr
            sga = 1947.0 + 0.20 * incr
        else:
            other_op = 70.0
            rd = years[prev_label]["rd"] + 1000.0
            sga = years[prev_label]["sga"] * 1.08
        ebit = gp - rd - sga - other_op
        gross_capex = net_capex * GROSS_PER_NET
        interest, principal, lease_next = lease_step(lease_cv, LEASE_PAY[i])
        # Next year's principal is the current-debt piece. One extra step on the post-pay balance.
        _, next_principal, _ = lease_step(lease_next, LEASE_PAY[i + 1])
        repay_contract = contract / 3.0 if label == "FY2029E" else 0.0
        withhold = WITHHOLD_RATE * sbc
        dividend = DIV_PER_SHARE * BASIC_SHARES

        int_inc = 0.0
        for _ in range(25):
            int_exp = -NOTE_COUPON
            pretax = ebit + int_inc + int_exp
            tax_exp = pretax * TAX_FCST
            tax = -tax_exp
            ni = pretax + tax
            q4 = fy27_q4 if label == "FY2027E" else revenue / 4.0
            rec, inv, ap, ocl = operating_balances(revenue, cogs, gross_capex, tax_exp, rd, sga, q4)
            # Cash roll. Lease interest is cash but not in net income (it is capitalized).
            d_rec = rec - (BS_HIST[prev_label]["rec"] if prev_label in HIST else years[prev_label]["rec"])
            d_inv = inv - (BS_HIST[prev_label]["inv"] if prev_label in HIST else years[prev_label]["inv"])
            d_ap = ap - (BS_HIST[prev_label]["ap"] if prev_label in HIST else years[prev_label]["ap"])
            d_ocl = ocl - (BS_HIST[prev_label]["ocl"] if prev_label in HIST else years[prev_label]["ocl"])
            ocf = ni + da + sbc - interest - d_rec - d_inv + d_ap + d_ocl
            net = ocf - net_capex - principal - withhold - dividend - repay_contract
            cash_end = cash_r + net
            liquid0 = cash_r + sti + lti
            liquid1 = cash_end + sti + lti
            int_inc_new = RF_1Y * 0.5 * (liquid0 + liquid1)
            if abs(int_inc_new - int_inc) < 1e-6:
                int_inc = int_inc_new
                break
            int_inc = int_inc_new
        else:
            raise AssertionError(f"interest income did not converge in {label}")

        ppe_end = ppe + net_capex + interest - da
        debt_total = NOTES_CV + lease_next
        debt_cur = next_principal
        debt_lt = debt_total - debt_cur
        contract_end = contract - repay_contract
        re_end = re + ni - dividend
        apic_end = apic + sbc
        ts_end = ts - withhold
        bs = dict(
            cash_eq=cash_end - restricted,
            restricted=restricted,
            sti=sti,
            rec=rec,
            inv=inv,
            oca=BS_HIST["FY2026A"]["oca"],
            lti=lti,
            ppe=ppe_end,
            gw=1150.0,
            onca=BS_HIST["FY2026A"]["onca"],
            ap=ap,
            debt_cur=debt_cur,
            contract_cur=0.0,
            ocl=ocl,
            debt_lt=debt_lt,
            unearned=BS_HIST["FY2026A"]["unearned"],
            contract=contract_end,
            oncl=BS_HIST["FY2026A"]["oncl"],
            cs=BS_HIST["FY2026A"]["cs"],
            apic=apic_end,
            re=re_end,
            ts=ts_end,
            aoci=BS_HIST["FY2026A"]["aoci"],
        )
        seg = {}
        da_alloc = {s: da * DA_WEIGHT[s] for s in SEGS}
        for s in SEGS:
            gp_s = rev_new[s] - cash_new[s] - da_alloc[s]
            seg[s] = dict(
                rev=rev_new[s],
                bits=BITS[label][s],
                asp=implied_asp[s],
                uc=UNIT_COST[label][s],
                cash_cogs=cash_new[s],
                da=da_alloc[s],
                gp=gp_s,
                gm=(gp_s / rev_new[s]) if rev_new[s] else None,
            )
        years[label] = dict(
            rev=revenue,
            cogs=cogs,
            gp=gp,
            rd=rd,
            sga=sga,
            other_op=other_op,
            ebit=ebit,
            da=da,
            ebitda=ebit + da,
            int_inc=int_inc,
            int_exp=-NOTE_COUPON,
            other_nonop=0.0,
            equity=0.0,
            pretax=pretax,
            tax=tax,
            tax_exp=tax_exp,
            ni=ni,
            eps=ni / DILUTED[label],
            sbc=sbc,
            sbc_cogs=sbc_cogs,
            net_capex=net_capex,
            gross_capex=gross_capex,
            lease_int=interest,
            lease_prin=principal,
            withhold=withhold,
            dividend=dividend,
            repay_contract=repay_contract,
            ocf=ocf,
            fcf=ocf - net_capex,
            d_rec=d_rec,
            d_inv=d_inv,
            d_ap=d_ap,
            d_ocl=d_ocl,
            cash0=cash_r,
            cash1=cash_end,
            net=net,
            seg=seg,
            **bs,
        )
        # Advance stocks.
        rev = rev_new
        cash_cogs = cash_new
        ppe = ppe_end
        lease_cv = lease_next
        re = re_end
        apic = apic_end
        ts = ts_end
        contract = contract_end
        cash_r = cash_end
        prev_label = label
    # Stash Q4 revenue on the quarter builder's annual dict via a side channel already used.
    return years


def ufcf_of(year_bs_prior_nwc: float, ebit: float, da: float, net_capex: float, bs: dict) -> float:
    nopat = ebit * (1.0 - TAX_FCST)
    return nopat + da - net_capex - (nwc(bs) - year_bs_prior_nwc)


def terminal_ufcf(fy29: dict, g: float, norm_gm: float):
    ppe = fy29["ppe"]
    capex = (0.16 + g) / 0.92 * ppe
    da = 0.16 * ppe + 0.08 * capex
    ppe_end = ppe + capex - da
    cash = 0.0
    for s in SEGS:
        cut = 0.95 if s != "OTHER" else 1.0
        cash += fy29["seg"][s]["cash_cogs"] * (1.0 + g) * cut
    sbc = fy29["sbc"] * (1.0 + g)
    sbc_cogs = sbc * SBC_COGS_SHARE
    cogs = cash + da + sbc_cogs
    rev = cogs / (1.0 - norm_gm)
    gp = rev - cogs
    rd = fy29["rd"] * (1.0 + g)
    sga = fy29["sga"] * (1.0 + g)
    other_op = 70.0
    ebit = gp - rd - sga - other_op
    tax_exp = ebit * TAX_FCST  # unlevered; interest is not in the terminal tax
    q4 = rev / 4.0
    rec, inv, ap, ocl = operating_balances(rev, cogs, capex * GROSS_PER_NET, tax_exp, rd, sga, q4)
    bs = dict(rec=rec, inv=inv, oca=fy29["oca"], ap=ap, ocl=ocl, contract_cur=0.0)
    d_nwc = nwc(bs) - nwc(fy29)
    ufcf = ebit * (1.0 - TAX_FCST) + da - capex - d_nwc
    return dict(rev=rev, cogs=cogs, gp=gp, gm=gp / rev, rd=rd, sga=sga, ebit=ebit, da=da, capex=capex, ppe_end=ppe_end, ppe_check=ppe * (1.0 + g), ufcf=ufcf, d_nwc=d_nwc, nopat=ebit * (1.0 - TAX_FCST), sbc=sbc)


def capital_structure():
    equity_mkt = PRICE_MU * BASIC_SHARES  # reference market cap; not a model input to the target
    debt = NOTES_CV + LEASE0
    ke = RF_10Y + BETA * ERP
    kd_pre = (NOTE_COUPON + LEASE0 * LEASE_RATE) / debt
    kd_after = kd_pre * (1.0 - TAX_FCST)
    v = equity_mkt + debt
    we = equity_mkt / v
    wd = debt / v
    wacc = we * ke + wd * kd_after
    return dict(equity_mkt=equity_mkt, debt=debt, ke=ke, kd_pre=kd_pre, kd_after=kd_after, we=we, wd=wd, wacc=wacc, v=v)


def dcf(years, wacc, g, norm_gm, ke):
    """Enterprise value at 2026-10-25 and the 12-month equity value per share.

    Price is not an argument. ke is the equity roll, wacc discounts unlevered flows.
    """
    ends = {2027: fy_end(2027), 2028: fy_end(2028), 2029: fy_end(2029)}
    labels = ["FY2027E", "FY2028E", "FY2029E"]
    prior_nwc = nwc(BS_HIST["FY2026A"])
    pv = 0.0
    rows = []
    for lab, yr in zip(labels, (2027, 2028, 2029)):
        y = years[lab]
        flow = ufcf_of(prior_nwc, y["ebit"], y["da"], y["net_capex"], y)
        t = year_frac(ends[yr])
        disc = flow / (1.0 + wacc) ** t
        pv += disc
        rows.append(dict(label=lab, end=ends[yr], t=t, ufcf=flow, pv=disc, ebit=y["ebit"], da=y["da"], capex=y["net_capex"], nwc=nwc(y), dnwc=nwc(y) - prior_nwc))
        prior_nwc = nwc(y)
    term = terminal_ufcf(years["FY2029E"], g, norm_gm)
    t_tv = rows[-1]["t"]
    tv = term["ufcf"] / (wacc - g)
    pv_tv = tv / (1.0 + wacc) ** t_tv
    ev = pv + pv_tv
    # Bridge uses 2026-09-03 balances. Opening cash is not equity's if it is owed back.
    cash_inv = cash_restr(BS_HIST["FY2026A"]) + BS_HIST["FY2026A"]["sti"] + BS_HIST["FY2026A"]["lti"]
    equity = ev - (NOTES_CV + LEASE0) + cash_inv - BS_HIST["FY2026A"]["contract"] - TAX_PAYABLE_NC
    per_share_today = equity / DILUTED["FY2027E"]
    # 12-month horizon: roll equity one year at the cost of equity, after the dividend.
    dividend_total = DIV_PER_SHARE * BASIC_SHARES
    equity_fwd = equity * (1.0 + ke) - dividend_total
    pt = equity_fwd / DILUTED["FY2027E"]
    return dict(rows=rows, term=term, tv=tv, pv_explicit=pv, pv_tv=pv_tv, ev=ev, equity=equity, per_share_today=per_share_today, pt=pt, cash_inv=cash_inv, tv_share=pv_tv / ev, t_tv=t_tv, dividend_total=dividend_total)


def sandisk_multiples():
    """FY2026 Sandisk, year ended 2026-07-03, price at 2026-10-23. One complete peer."""
    price = 1238.03
    shares = 149.0  # million, issued and outstanding at 2026-07-03
    cash = 4762.0
    mkt_sec = 1777.0
    debt = 20.0 + 1829.0
    rev = 20248.0
    ebit = 12389.0
    eps = 73.76
    mkt = price * shares
    ev = mkt + debt - cash - mkt_sec
    return dict(price=price, shares=shares, ev=ev, ebit=ev / ebit, pe=price / eps, sales=ev / rev, rev=rev, oi=ebit, eps=eps, mkt=mkt)


def assert_model(q, q_annual, scale, years, cap, result):
    checks = []

    def check(name, cond):
        checks.append(name)
        if not cond:
            raise AssertionError(name)

    check("fy2026 ends 2026-09-03", fy_end(2026) == date(2026, 9, 3))
    check("fy2025 ends 2025-08-28", fy_end(2025) == date(2025, 8, 28))
    check("fy2024 ends 2024-08-29", fy_end(2024) == date(2024, 8, 29))
    check("notes plus leases equal 5179", abs((NOTES_CV + LEASE0) - 5179) < 1e-6)
    check("coupon is about 109", abs(NOTE_COUPON - 109.078) < 0.01)

    for lab in HIST:
        check(f"{lab} segment revenue sums", abs(sum(REV_HIST[lab].values()) - IS_HIST[lab]["rev"]) < 1e-6)
        gp_seg = sum(GP_HIST[lab].values()) - UNALLOC_COGS_HIST[lab]
        check(f"{lab} segment gross profit sums", abs(gp_seg - IS_HIST[lab]["gp"]) < 1e-6)
        bs = BS_HIST[lab]
        check(f"{lab} A = L + E", abs(total_assets(bs) - total_liab(bs) - total_equity(bs)) < 1e-6)
        isr = IS_HIST[lab]
        ni = isr["ebit"] + isr["int_inc"] + isr["int_exp"] + isr["other_nonop"] + isr["tax"] + isr["equity"]
        check(f"{lab} net income ties", abs(ni - isr["ni"]) < 1e-6)
        check(f"{lab} diluted EPS ties", abs(isr["ni"] / DILUTED[lab] - isr["eps"]) < 0.015)
        cf = CF_HIST[lab]
        ocf = cf["ni"] + cf["da"] + cf["sbc"] + cf["rec"] + cf["inv"] + cf["ap"] + cf["ocl"] + cf["oncl"] + cf["other"]
        check(f"{lab} operating cash flow ties", abs(ocf - cf["ocf"]) < 1e-6)
        check(f"{lab} cash roll ties", abs(cf["cash0"] + cf["net"] - cf["cash1"]) < 1e-6)
        check(f"{lab} ending cash equals balance sheet", abs(cf["cash1"] - cash_restr(bs)) < 1e-6)
    check("reported totals", abs(total_assets(BS_HIST["FY2024A"]) - 69416) < 1e-6 and abs(total_assets(BS_HIST["FY2026A"]) - 195888) < 1e-6)
    check("company FCF FY2025 and FY2026", abs(CF_HIST["FY2025A"]["ocf"] - 13804 - 3721) < 1e-6 and abs(CF_HIST["FY2026A"]["ocf"] - 27367 - 62308) < 1e-6)
    for lab in HIST:
        cf = CF_HIST[lab]
        rolled = cf["ocf"] + INVESTING_CF[lab] + cf["deposits"] + cf["debt_issued"] - cf["debt_repay"] - cf["withhold"] - cf["buyback"] - cf["div"] + cf["other_fin"] + cf["fx"]
        check(f"{lab} cash-flow column adds to the net change", abs(rolled - cf["net"]) < 1e-6)
    for lab in FCST:
        y = years[lab]
        rolled = y["ocf"] - y["net_capex"] - y["repay_contract"] - y["lease_prin"] - y["withhold"] - y["dividend"]
        check(f"{lab} cash-flow column adds to the net change", abs(rolled - y["net"]) < 1e-3)

    check("FQ1 sums to the guide", abs(sum(q[1].values()) - FQ1_GUIDE) < 1e-6)
    qtot = [sum(q[k].values()) for k in (1, 2, 3, 4)]
    check("sequential revenue growth in FY2027E", qtot[1] > qtot[0] and qtot[2] > qtot[1] and qtot[3] > qtot[2])
    check("FY2027E revenue is the quarter sum", abs(sum(q_annual[s] for s in SEGS) - years["FY2027E"]["rev"]) < 1e-6)
    check("scale is an allocation, not a new total", abs(scale - FQ1_GUIDE / sum(FQ4_FY26_REV[s] * FQ1_SEQ[s] for s in SEGS)) < 1e-9)

    for lab in FCST:
        y = years[lab]
        check(f"{lab} revenue sums from segments", abs(sum(y["seg"][s]["rev"] for s in SEGS) - y["rev"]) < 1e-4)
        gp_from_seg = sum(y["seg"][s]["gp"] for s in SEGS) - y["sbc_cogs"]
        check(f"{lab} gross profit sums from segments", abs(gp_from_seg - y["gp"]) < 1e-3)
        check(f"{lab} EBIT identity", abs((y["gp"] - y["rd"] - y["sga"] - y["other_op"]) - y["ebit"]) < 1e-4)
        check(f"{lab} EBITDA identity", abs(y["ebitda"] - y["ebit"] - y["da"]) < 1e-6)
        check(f"{lab} net income identity", abs(y["ebit"] + y["int_inc"] + y["int_exp"] + y["tax"] - y["ni"]) < 1e-3)
        check(f"{lab} A = L + E", abs(total_assets(y) - total_liab(y) - total_equity(y)) < 1e-3)
        check(f"{lab} cash roll equals balance sheet", abs(y["cash1"] - cash_restr(y)) < 1e-3)
        check(f"{lab} FCF is OCF minus net capex", abs(y["fcf"] - (y["ocf"] - y["net_capex"])) < 1e-6)
        check(f"{lab} no discretionary buyback", True)
        for s in SEGS:
            if s == "OTHER":
                continue
            # Revenue identity: rev = prior x (1+bits) x (1+asp), asp is the residual in FY27 and the driver after.
            check(f"{lab} {s} ASP finite", y["seg"][s]["asp"] == y["seg"][s]["asp"])
    check("FY2027E gross margin at or above the guided floor", years["FY2027E"]["gp"] / years["FY2027E"]["rev"] + 1e-9 >= 0.8595)
    check("g at or under long-run nominal growth", G <= G_CAP + 1e-12)
    check("weights sum to 1 and comps are not fitted in", abs(WEIGHT_DCF + WEIGHT_COMPS - 1.0) < 1e-12 and WEIGHT_COMPS == 0.0)
    check("terminal PPE grows at g", abs(result["term"]["ppe_end"] - result["term"]["ppe_check"]) < 1e-3)
    check("terminal margin is the mid-cycle gross margin", abs(result["term"]["gm"] - NORM_GM) < 1e-9)
    check("WACC exceeds g", cap["wacc"] > G)
    check("price target is positive and is not the market price", result["pt"] > 0 and abs(result["pt"] - PRICE_MU) > 1.0)
    check("TV share is between 0 and 1", 0.0 < result["tv_share"] < 1.0)
    # The target function's numeric result must match a second call. Guards a silent overwrite.
    again = dcf(years, cap["wacc"], G, NORM_GM, cap["ke"])
    check("DCF is reproducible", abs(again["pt"] - result["pt"]) < 1e-6)
    return checks


def sensitivity(years, cap):
    """Two grids. The wider one is the primary table."""
    waccs = [cap["wacc"] + d for d in (-0.03, -0.015, 0.0, 0.015, 0.03)]
    gms = [0.35, 0.40, 0.45, 0.50, 0.55]
    gs = [0.020, 0.025, 0.030, 0.035, 0.040]
    def ke_for(w):
        # Hold capital structure and after-tax debt cost; solve the equity cost that produces this WACC.
        return (w - cap["wd"] * cap["kd_after"]) / cap["we"]

    grid_gm = []
    for w in waccs:
        row = []
        for gm in gms:
            row.append(dcf(years, w, G, gm, ke_for(w))["pt"])
        grid_gm.append(row)
    grid_g = []
    for w in waccs:
        row = []
        for g in gs:
            row.append(dcf(years, w, g, NORM_GM, ke_for(w))["pt"])
        grid_g.append(row)
    span = lambda grid: max(max(r) for r in grid) - min(min(r) for r in grid)
    primary = "gm" if span(grid_gm) >= span(grid_g) else "g"
    return dict(waccs=waccs, gms=gms, gs=gs, grid_gm=grid_gm, grid_g=grid_g, span_gm=span(grid_gm), span_g=span(grid_g), primary=primary)


def write_segments(q, q_annual, scale, exit_vs_avg, years):
    lines = []
    a = lines.append
    a("# Micron Technology, Inc. (`mu`) — segments")
    a("")
    a(f"As of {ASOF}. Units: US$ millions except percents and drivers. Years marked A are reported. Years marked E are the model. Generated by `models/mu/build_model.py` from `memory/mu/financials_raw.md`. Do not edit the figures by hand.")
    a("")
    a("Reportable units are the FY2026 Form 10-K units: Cloud Memory (CMBU), Core Data Center (CDBU), Mobile and Client (MCBU), Automotive and Embedded (AEBU), and All other. Revenue in the forecast is prior revenue × (1 + bit growth) × (1 + ASP change). FY2027E bit growth is the judgment. FY2027E ASP is the residual of that identity once quarterly revenue is set. It is not a third independent assumption.")
    a("")
    a("## Quarterly path into FY2027E")
    a("")
    a("FQ4 FY2026A revenue is the base. FQ1 sequential rates are the mix (CMBU +12%, CDBU +18%, MCBU +8%, AEBU +12%). They sum to $61,291 before a scale of " + f"{scale:.6f}" + f" that lands the company on the guided midpoint of ${FQ1_GUIDE/1000:.1f} billion. The scale is an allocation of a known total, not a new revenue assumption. FQ2–FQ4 are sequential bits × ASP: CMBU bits +6% and ASP +2.5% (HBM bits grow faster, and calendar-2027 HBM prices are still guided up); CDBU bits +4% and ASP +2%; MCBU bits +1% and ASP +2% (supply stays tilted to the data center); AEBU bits +3% and ASP +2%. All other stays at $6 million a quarter. Each quarter's company revenue is higher than the quarter before it, which is the September 30, 2026 statement that revenue grows sequentially through FY2027E.")
    a("")
    headers = ["Segment", "FQ4 FY2026A", "FQ1 FY2027E", "FQ2 FY2027E", "FQ3 FY2027E", "FQ4 FY2027E", "FY2027E"]
    rows = []
    for s in SEGS:
        name = "All other" if s == "OTHER" else s
        rows.append([name, fmt(FQ4_FY26_REV[s]), fmt(q[1][s]), fmt(q[2][s]), fmt(q[3][s]), fmt(q[4][s]), fmt(q_annual[s])])
    rows.append(["Total", fmt(sum(FQ4_FY26_REV.values())), fmt(sum(q[1].values())), fmt(sum(q[2].values())), fmt(sum(q[3].values())), fmt(sum(q[4].values())), fmt(sum(q_annual[s] for s in SEGS))])
    a(md_table(headers, rows))
    a("")
    a("Source for FQ4 FY2026A: earnings release, September 30, 2026, except All other, which is the $6 million residual of $54,229 − $54,223. FQ1 company total: same release, midpoint. Later columns: model.")
    a("")
    reasons = {
        "CMBU": "Hyperscale DRAM and all HBM. FY2027E bits +28%: company DRAM supply is guided in line with industry growth in the mid-20s for calendar 2026 and the low-20s for calendar 2027–2028, and HBM bits grow faster than conventional DRAM through calendar 2028, so this unit is above the company DRAM rate. Cash cost per bit −5%, three points less deflation than CDBU and MCBU, because a higher HBM mix uses more wafers per bit. That gap is the HBM-mix driver. HBM revenue dollars were not obtained, so mix is not a revenue split. FY2028E holds the FY2027E exit price (the small ASP change versus the FY2027E average is only the intra-year ramp of +2.5% a quarter) and grows bits 22%. FY2029E cuts ASP 30% as ID1 is in volume and ID2, Hiroshima, and the Singapore NAND fab start, and grows bits 18%.",
        "CDBU": "Data-center SSDs and NAND components, plus OEM, enterprise, and NeoCloud DRAM. FY2027E bits +40%: FQ4 data-center SSD revenue was nearly $10 billion and more than 10× the prior year, so a large part of the exit rate is volume that was not in the FY2026A average. Annualizing that ramp, plus NAND bits still growing, is a faster bit year than the company-wide NAND comment (Micron NAND supply grows less than the industry). Cash cost per bit −8% (G8/G9 bit cost, not a disclosed cost-per-bit). FY2028E bits +20% at the FY2027E exit price. FY2029E bits +18% and ASP −30%, same cleanroom timing as CMBU. Share of the data-center SSD market was not obtained.",
        "MCBU": "Smartphones, client PCs, and component DRAM and NAND. FY2026A bits fell because wafers moved to other units. FY2027E bits +6%: the allocation does not fully reverse while data-center demand is still short, and 1γ mobile is shipping. ASP does the rest of the revenue bridge. Cash cost per bit −8%. FY2028E bits +10% once ID1 wafers (mid-calendar 2027) start to ease the allocation. FY2029E bits +12% and ASP −30%.",
        "AEBU": "Automotive, industrial, and embedded. FY2026A grew on ASP and bits; FQ4 grew 47% sequentially on both. FY2027E bits +25% annualizes that exit-rate volume and keeps content growth, below CMBU because this is not where HBM goes. Cash cost per bit −6% (legacy mix slows the node gain). FY2028E bits +12% at the exit price. FY2029E bits +10% and ASP −30%. The Level 4+ content comment is not a TAM and is not used as a dollar driver.",
        "OTHER": "Immaterial. FY2026A revenue was $24 million. The forecast holds $6 million a quarter, $24 million a year. No bit or ASP driver. Gross profit stays a rounding item.",
    }
    for s in SEGS:
        title = "All other" if s == "OTHER" else s
        a(f"## {title}")
        a("")
        a(reasons[s])
        a("")
        headers = ["", *YEARS]
        rev_row = ["Revenue"]
        yoy_row = ["YoY revenue"]
        mix_row = ["Mix of company revenue"]
        driver_row = ["Driver"]
        gm_row = ["Gross margin"]
        prev = None
        for lab in YEARS:
            if lab in HIST:
                r = REV_HIST[lab][s]
                gm = GP_HIST[lab][s] / r if r else None
                if lab == "FY2024A":
                    driver = "Reported. Segment bit and ASP split: not obtained."
                elif lab == "FY2025A":
                    driver = "Reported. See research.md §3.2 for the 10-K direction."
                else:
                    driver = "Reported. Company DRAM ASP about +180% and NAND ASP about +200%; segment split not obtained."
            else:
                r = years[lab]["seg"][s]["rev"]
                gm = years[lab]["seg"][s]["gm"]
                driver = f"Bits {pct(years[lab]['seg'][s]['bits'])}, ASP {pct(years[lab]['seg'][s]['asp'])}, cash cost/bit {pct(years[lab]['seg'][s]['uc'])}."
            total = IS_HIST[lab]["rev"] if lab in HIST else years[lab]["rev"]
            rev_row.append(fmt(r))
            yoy_row.append("—" if prev is None else pct(r / prev - 1))
            mix_row.append(pct(r / total))
            driver_row.append(driver)
            gm_row.append("n.m." if gm is None else pct(gm))
            prev = r
        a(md_table(headers, [rev_row, yoy_row, mix_row, gm_row, driver_row]))
        a("")
        if s != "OTHER":
            a(f"FY2028E exit-versus-average price factor used on this segment: {exit_vs_avg[s]:.4f} (1.0000 means the FY2027E average price).")
            a("")
    a("Historical gross margin is Note 20 gross profit ÷ revenue. Forecast gross margin is segment gross profit ÷ revenue after segment cash cost and allocated depreciation. Unallocated stock-based compensation sits below the segment sum, in the income statement. Historical segment operating income is in `financials_raw.md` and is not rebuilt here, because quarterly segment operating-income dollars were not disclosed and the forecast operating expenses are guided at the company, not the unit.")
    a("")
    a("Source line: FY2024A–FY2026A Note 20 and the September 30, 2026 release and prepared remarks, via `memory/mu/financials_raw.md` and `memory/mu/research.md`. FY2027E–FY2029E: this model. As of 2026-10-25.")
    a("")
    (OUT / "segments.md").write_text("\n".join(lines), encoding="utf-8")


def write_income(years):
    lines = []
    a = lines.append
    a("# Micron Technology, Inc. (`mu`) — income statement")
    a("")
    a(f"As of {ASOF}. Units: US$ millions except per share, share counts (millions), and percents. A = reported. E = model. Depreciation is inside cost of goods sold and is also shown as a memo, so EBITDA = EBIT + depreciation. Generated by `models/mu/build_model.py`.")
    a("")
    a("Forecast revenue and gross profit are the sum of the five segments in `segments.md`, minus unallocated cost of goods sold. Unallocated cost of goods sold in the forecast is the stock-based-compensation portion that Note 14 records in cost of goods sold (528 / 1,282 of total SBC). FY2027E R&D + SG&A + other operating expense equals FY2026A operating expenses plus the guided $2.5 billion, and the $500 patent-license charge does not repeat (other operating expense is set at $70). Eighty percent of the remaining R&D and SG&A increase is R&D. FY2028E and FY2029E add $1.0 billion of R&D a year (the announced Micron Research Labs plan is about $10 billion over a decade) and grow SG&A 8%. The tax rate is the guided 15.5% in each forecast year. Interest expense is the coupon on the notes that remain after the FY2026A prepayments ($109 million). Finance-lease interest is capitalized while construction is heavy, which is why FQ3 and FQ4 FY2026A printed no interest expense. Interest income is the 1-year Treasury par yield of 4.44% on the average of opening and ending cash, restricted cash, and marketable investments.")
    a("")

    def get(lab, key):
        if lab in HIST:
            return IS_HIST[lab][key]
        return years[lab][key]

    rows_spec = [
        ("Revenue", "rev", 0),
        ("Cost of goods sold", "cogs", 0),
        ("Gross profit", "gp", 0),
        ("Research and development", "rd", 0),
        ("Selling, general, and administrative", "sga", 0),
        ("Other operating expense (income)", "other_op", 0),
        ("EBIT (GAAP operating income)", "ebit", 0),
        ("Depreciation and amortization (memo, inside COGS)", "da", 0),
        ("EBITDA", "ebitda", 0),
        ("Interest income", "int_inc", 0),
        ("Interest expense", "int_exp", 0),
        ("Other non-operating income (expense)", "other_nonop", 0),
        ("Equity in net income (loss) of investees", "equity", 0),
        ("Income before tax", "pretax", 0),
        ("Income tax (provision) benefit", "tax", 0),
        ("Net income", "ni", 0),
        ("Diluted weighted-average shares (millions)", "shares", 0),
        ("Diluted EPS ($)", "eps", 2),
    ]
    headers = ["", *YEARS]
    table = []
    for label, key, dec in rows_spec:
        row = [label]
        for lab in YEARS:
            if key == "shares":
                row.append(fmt(DILUTED[lab], 0))
            elif key == "eps":
                row.append(fmt(get(lab, "eps"), 2))
            elif key == "ebitda":
                if lab in HIST:
                    row.append(fmt(IS_HIST[lab]["ebit"] + IS_HIST[lab]["da"]))
                else:
                    row.append(fmt(years[lab]["ebitda"]))
            elif key == "equity":
                row.append(fmt(IS_HIST[lab]["equity"] if lab in HIST else 0))
            else:
                row.append(fmt(get(lab, key), dec))
        table.append(row)
    a(md_table(headers, table))
    a("")
    margin_rows = []
    for name, num, den in (
        ("Gross margin", "gp", "rev"),
        ("EBIT margin", "ebit", "rev"),
        ("EBITDA margin", "ebitda", "rev"),
        ("Net margin", "ni", "rev"),
    ):
        row = [name]
        for lab in YEARS:
            if lab in HIST:
                n_ = IS_HIST[lab]["ebit"] + IS_HIST[lab]["da"] if num == "ebitda" else IS_HIST[lab][num]
                d_ = IS_HIST[lab][den]
            else:
                n_ = years[lab][num]
                d_ = years[lab][den]
            row.append(pct(n_ / d_))
        margin_rows.append(row)
    row = ["Effective tax rate"]
    for lab in YEARS:
        if lab in HIST:
            row.append(pct(-IS_HIST[lab]["tax"] / IS_HIST[lab]["pretax"]))
        else:
            row.append(pct(TAX_FCST))
    margin_rows.append(row)
    a(md_table(headers, margin_rows))
    a("")
    a("FY2027E gross margin has to clear the guided floor of about 85.95%. The script asserts that. The FY2029E ASP cut of 30% only moves gross margin from the high 80s to about 82%, because cash cost is a small share of the peak price. That is the explicit-year step. The mid-cycle reset to a 45% gross margin is the terminal year in `valuation.md`, not FY2029E. FY2026A other operating expense includes the $500 patent-license charge; FY2024A other operating income includes a $200 cross-license gain. Those are not repeated. Equity-method income is held at zero in the forecast because $59 million in FY2026A is not a driver and the investment asset is not modeled as a separate line. Other non-operating expense in FY2026A includes the $510 loss on debt prepayment, which is not repeated.")
    a("")
    a("Segment gross profit rolls to company gross profit as follows. Historical unallocated cost of goods sold is the Note 20 plug (a credit in FY2024A because of the $987 million benefit from selling inventory written down in FY2023A).")
    a("")
    roll_headers = ["", *YEARS]
    seg_sum = ["Sum of segment gross profit"]
    unalloc = ["Unallocated COGS (subtracted)"]
    company = ["Company gross profit"]
    for lab in YEARS:
        if lab in HIST:
            seg_sum.append(fmt(sum(GP_HIST[lab].values())))
            unalloc.append(fmt(UNALLOC_COGS_HIST[lab]))
            company.append(fmt(IS_HIST[lab]["gp"]))
        else:
            seg_sum.append(fmt(sum(years[lab]["seg"][s]["gp"] for s in SEGS)))
            unalloc.append(fmt(years[lab]["sbc_cogs"]))
            company.append(fmt(years[lab]["gp"]))
    a(md_table(roll_headers, [seg_sum, unalloc, company]))
    a("")
    a("Source: FY2024A–FY2026A FY2026 Form 10-K statements of operations, Note 7, Note 14, and Note 20. FY2027E–FY2029E: this model. As of 2026-10-25. Displays are rounded to $1 million; the script asserts the unrounded identities.")
    a("")
    (OUT / "income.md").write_text("\n".join(lines), encoding="utf-8")


def bs_view(lab, years):
    if lab in HIST:
        return BS_HIST[lab]
    return years[lab]


def write_balance(years):
    lines = []
    a = lines.append
    a("# Micron Technology, Inc. (`mu`) — balance sheet")
    a("")
    a(f"As of {ASOF}. Units: US$ millions. A = reported, presented on the FY2026 10-K classification. E = model. Restricted cash is broken out of other current assets so the cash-flow total (cash, equivalents, and restricted cash) is a visible line. FY2024A restricted cash of $11 is deducted: cash-flow total $7,052 minus balance-sheet cash $7,041. FY2024A noncurrent contract liabilities of $141 and current contract liabilities of $766 are the FY2025 10-K revenue-note split of $907. FY2025A uses the face amounts $26 current and $142 noncurrent (the revenue note prints $169; the $1 difference is the presentation gap already in the Gate 1 pack). FY2026A current contract liabilities are not a face line; the noncurrent line is $12,895. Generated by `models/mu/build_model.py`.")
    a("")
    a("Forecast policy, each one stated so none of them is a silent plug:")
    a("")
    a("- Trade receivables = 60 days of annual revenue, next to the FQ4 FY2026A exit of 57.5 days. The FY2026A year-average of 88.6 days is the ramp, not the collection cycle. Other receivables (government incentives, taxes, other) stay at $4,404.")
    a("- Inventory = 142 days of annual cost of goods sold. That matches FQ4 FY2026A inventory against FQ4 cost of goods sold. The company's 129-day DIO is a different definition and is not used.")
    a("- Trade payables keep the FY2026A ratio to cost of goods sold. PPE payables = 28.1% of gross capex, the FY2026A ratio. Current income-tax payable = 25% of the year's tax provision. Compensation accruals scale with R&D + SG&A. The $396 of other accrued expenses stays flat.")
    a("- Other current liabilities = 8% of FQ4 revenue (the FY2026A price-protection accrual was $4,320 inside a $4,386 line, and 8% of FQ4 revenue reproduces it). FY2028E and FY2029E use one quarter of annual revenue as FQ4.")
    a("- Short-term and long-term marketable investments stay at the September 3, 2026 balances. Maturities are reinvested. Surplus cash stays in cash equivalents. No further customer deposits are forecast, because the timing of the undrawn commitment was not obtained. One-third of the $12,895 contract liability is repaid in FY2029E, the first of the three fiscal years inside the 2029–2031 window. The 10-K does not give a fiscal-year schedule; the one-third is the model timing.")
    a("- Goodwill, other noncurrent assets, unearned government incentives, and other noncurrent liabilities (including the $9.82 billion noncurrent tax payable) stay flat. Payment dates for that payable were not obtained, so it is not paid inside the forecast and it is subtracted in the valuation bridge instead.")
    a("- Debt: notes stay at carrying value $2,792. Finance leases amortize at the 4.71% effective rate against the undiscounted maturity schedule. No new borrowing and no discretionary note prepayment.")
    a("- Equity: retained earnings plus net income minus the dividend; additional capital plus stock-based compensation; treasury stock minus withholding at 45% of SBC. No open-market buyback. The $35.16 billion authorization is capacity from December 9, 2026, not a committed program, and the CHIPS award limits buybacks until that date. Diluted shares stay at the FQ1 guide of 1,150 million. Basic shares for the dividend stay at 1,131 million outstanding.")
    a("")
    items = [
        ("Cash and cash equivalents", "cash_eq"),
        ("Restricted cash", "restricted"),
        ("Short-term investments", "sti"),
        ("Receivables", "rec"),
        ("Inventories", "inv"),
        ("Other current assets", "oca"),
        ("Total current assets", "tca"),
        ("Long-term marketable investments", "lti"),
        ("Property, plant, and equipment, net", "ppe"),
        ("Goodwill", "gw"),
        ("Other noncurrent assets", "onca"),
        ("Total assets", "ta"),
        ("Accounts payable and accrued expenses", "ap"),
        ("Current debt", "debt_cur"),
        ("Customer contract liabilities, current", "contract_cur"),
        ("Other current liabilities", "ocl"),
        ("Total current liabilities", "tcl"),
        ("Long-term debt", "debt_lt"),
        ("Noncurrent unearned government incentives", "unearned"),
        ("Noncurrent customer contract liabilities", "contract"),
        ("Other noncurrent liabilities", "oncl"),
        ("Total liabilities", "tl"),
        ("Common stock", "cs"),
        ("Additional capital", "apic"),
        ("Retained earnings", "re"),
        ("Treasury stock", "ts"),
        ("Accumulated other comprehensive income (loss)", "aoci"),
        ("Total equity", "te"),
        ("Total liabilities and equity", "tle"),
        ("Assets − liabilities − equity (unrounded)", "gap"),
    ]
    headers = ["", *YEARS]
    table = []
    for label, key in items:
        row = [label]
        for lab in YEARS:
            bs = bs_view(lab, years)
            ta = total_assets(bs)
            tl = total_liab(bs)
            te = total_equity(bs)
            tca = cash_restr(bs) + bs["sti"] + bs["rec"] + bs["inv"] + bs["oca"]
            tcl = bs["ap"] + bs["debt_cur"] + bs["contract_cur"] + bs["ocl"]
            values = dict(tca=tca, ta=ta, tcl=tcl, tl=tl, te=te, tle=tl + te, gap=ta - tl - te)
            if key == "gap":
                gapv = values["gap"]
                row.append("0.0" if abs(gapv) < 1e-4 else fmt(gapv, 1))
            elif key in values:
                row.append(fmt(values[key], 0))
            else:
                row.append(fmt(bs[key]))
        table.append(row)
    a(md_table(headers, table))
    a("")
    a("The gap row is the unrounded identity. The script asserts it is zero in every year. Displayed lines are rounded to $1 million, so a column of rounded lines can differ from the rounded total by $1 million.")
    a("")
    a("Source: FY2024A–FY2026A FY2026 and FY2025 Forms 10-K, as assembled in `memory/mu/financials_raw.md`. FY2027E–FY2029E: this model. As of 2026-10-25.")
    a("")
    (OUT / "balance.md").write_text("\n".join(lines), encoding="utf-8")


def write_cashflow(years):
    lines = []
    a = lines.append
    a("# Micron Technology, Inc. (`mu`) — cash flow")
    a("")
    a(f"As of {ASOF}. Units: US$ millions. A = reported. E = model. Cash is cash, cash equivalents, and restricted cash, the cash-flow-statement total. Ending cash equals that balance-sheet sum in every year. Generated by `models/mu/build_model.py`.")
    a("")
    a("Forecast operating cash flow starts at net income and adds depreciation and stock-based compensation. It subtracts finance-lease interest, which is capitalized into PP&E and therefore is not in net income, and it subtracts the increases in receivables and inventory and adds the increases in payables and other current liabilities. There is no unidentified 'other' line in the forecast. Customer-deposit repayment is financing, matching the FY2026A classification of deposit proceeds. The operating lines sum to operating cash flow. Operating cash flow plus investing, financing, and the exchange-rate line equal the net change, and beginning cash plus that change is ending cash. Gross capex and free cash flow sit below the roll so they are not a second cash outflow.")
    a("")
    a("Net capex: FY2027E $55,000 = guided first-half $25,000 + a model second half of $30,000. The remarks said the second half is higher and that construction grows faster than equipment, and they did not give the year. $30,000 is $5,000 above the first half, not a doubling. FY2028E $46,000 and FY2029E $40,000 step down from that construction year and stay above FY2026A net capex of $27,367 because Idaho 2, New York, Hiroshima, and Singapore are still being built. Gross cash spend in the working-capital forecast equals net capex × (30,712 / 27,367), the FY2026A ratio of gross spend to net capex. Book PP&E increases by net capex plus capitalized lease interest and decreases by depreciation. Depreciation = 16% of opening net PP&E + 8% of the year's net capex (half-year convention). On FY2026A that rule returns $9,643 against reported depreciation of $9,503.")
    a("")
    headers = ["", *YEARS]
    # Build display rows.
    def row_hist_fcst(label, hkey, fkey, signed_outflow=False):
        row = [label]
        for lab in YEARS:
            if lab in HIST:
                v = CF_HIST[lab][hkey]
                if v is None:
                    row.append("not obtained")
                else:
                    row.append(fmt(-v if signed_outflow else v))
            else:
                v = years[lab][fkey]
                row.append(fmt(-v if signed_outflow else v))
        return row

    table = []
    table.append(row_hist_fcst("Net income", "ni", "ni"))
    table.append(row_hist_fcst("Depreciation and amortization", "da", "da"))
    table.append(row_hist_fcst("Stock-based compensation", "sbc", "sbc"))
    # WC lines: historical are already signed; forecast deltas need the cash-flow sign (asset increase negative).
    for label, hkey, fkey, asset in (
        ("Receivables", "rec", "d_rec", True),
        ("Inventories", "inv", "d_inv", True),
        ("Accounts payable and accrued expenses", "ap", "d_ap", False),
        ("Other current liabilities", "ocl", "d_ocl", False),
    ):
        row = [label]
        for lab in YEARS:
            if lab in HIST:
                row.append(fmt(CF_HIST[lab][hkey]))
            else:
                delta = years[lab][fkey]
                row.append(fmt(-delta if asset else delta))
        table.append(row)
    row = ["Finance-lease interest (capitalized, cash)"]
    for lab in YEARS:
        row.append("—" if lab in HIST else fmt(-years[lab]["lease_int"]))
    table.append(row)
    row = ["Other operating (historical residual)"]
    for lab in YEARS:
        if lab in HIST:
            # Combine oncl + other so the historical OCF still sums, and show them.
            row.append(fmt(CF_HIST[lab]["oncl"] + CF_HIST[lab]["other"]))
        else:
            row.append(fmt(0))
    table.append(row)
    table.append(row_hist_fcst("Operating cash flow", "ocf", "ocf"))
    row = ["Investing cash flow"]
    for lab in YEARS:
        if lab in HIST:
            row.append(fmt(INVESTING_CF[lab]))
        else:
            row.append(fmt(-years[lab]["net_capex"]))
    table.append(row)
    row = ["Customer contract-liability deposits (repayment)"]
    for lab in YEARS:
        if lab in HIST:
            row.append(fmt(CF_HIST[lab]["deposits"]))
        else:
            row.append(fmt(-years[lab]["repay_contract"]))
    table.append(row)
    row = ["Debt proceeds"]
    for lab in YEARS:
        row.append(fmt(CF_HIST[lab]["debt_issued"]) if lab in HIST else fmt(0))
    table.append(row)
    row = ["Debt repayment (notes, historical; finance-lease principal, forecast)"]
    for lab in YEARS:
        if lab in HIST:
            row.append(fmt(-CF_HIST[lab]["debt_repay"]))
        else:
            row.append(fmt(-years[lab]["lease_prin"]))
    table.append(row)
    row = ["Open-market buyback"]
    for lab in YEARS:
        row.append(fmt(-CF_HIST[lab]["buyback"]) if lab in HIST else fmt(0))
    table.append(row)
    table.append(row_hist_fcst("Tax withholding on equity awards", "withhold", "withhold", signed_outflow=True))
    table.append(row_hist_fcst("Dividends paid", "div", "dividend", signed_outflow=True))
    row = ["Other financing (historical)"]
    for lab in YEARS:
        row.append(fmt(CF_HIST[lab]["other_fin"]) if lab in HIST else fmt(0))
    table.append(row)
    row = ["Effect of exchange rates"]
    for lab in YEARS:
        row.append(fmt(CF_HIST[lab]["fx"]) if lab in HIST else fmt(0))
    table.append(row)
    table.append(row_hist_fcst("Net change in cash, equivalents, and restricted cash", "net", "net"))
    table.append(row_hist_fcst("Beginning cash, equivalents, and restricted cash", "cash0", "cash0"))
    table.append(row_hist_fcst("Ending cash, equivalents, and restricted cash", "cash1", "cash1"))
    a(md_table(headers, table))
    a("")
    a("Capex and free cash flow, not part of the roll above:")
    a("")
    memo = []
    memo.append(row_hist_fcst("Gross PP&E spend", "capex_gross", "gross_capex", signed_outflow=True))
    row = ["Net capex (company definition)"]
    for lab in YEARS:
        if lab in HIST:
            v = CF_HIST[lab]["capex_net"]
            row.append("not obtained" if v is None else fmt(-v))
        else:
            row.append(fmt(-years[lab]["net_capex"]))
    memo.append(row)
    row = ["Free cash flow (operating cash flow − net capex)"]
    for lab in YEARS:
        if lab == "FY2024A":
            row.append("not obtained")
        elif lab in HIST:
            row.append(fmt(FCF_COMPANY[lab]))
        else:
            row.append(fmt(years[lab]["fcf"]))
    memo.append(row)
    a(md_table(headers, memo))
    a("")
    a("Historical investing cash flow is the 10-K total, which includes securities purchases and government-incentive proceeds as well as gross PP&E spend. Forecast investing cash flow is net capex only: marketable securities are held flat, and incentive proceeds are already inside the company's net-capex definition. Historical 'other operating' is other noncurrent liabilities plus the 10-K other line, so the operating block still sums to reported operating cash flow. The forecast has no residual. Free cash flow is operating cash flow minus net capex, which is the company's adjusted free-cash-flow definition. FY2025A $3,721 and FY2026A $62,308 reproduce the release. FY2024A company net capex was not obtained.")
    a("")
    a("Dividend forecast: $0.60 a share on 1,131 million basic shares. That is four quarters at the $0.15 declared on September 30, 2026. It is not a company full-year dividend guide. Withholding is 45% of stock-based compensation. The FY2026A withholding ratio was higher because awards were withheld at a high share price (912 shares at $983.12 in July 2026); that ratio is not run forward.")
    a("")
    a("Source: FY2024A–FY2026A FY2026 Form 10-K cash-flow statement and the September 30, 2026 net-capex reconciliation. FY2027E–FY2029E: this model. As of 2026-10-25.")
    a("")
    (OUT / "cashflow.md").write_text("\n".join(lines), encoding="utf-8")


def write_valuation(years, cap, result, sens, sndk):
    lines = []
    a = lines.append
    a("# Micron Technology, Inc. (`mu`) — valuation")
    a("")
    a(f"As of {ASOF}. Horizon: 12 months, to 2027-10-25. Units: US$ millions except per share and percents. Generated by `models/mu/build_model.py`. The market price is a reference. It is not an input to the target. No rating.")
    a("")
    a("## 1. Price target")
    a("")
    a(f"**${result['pt']:,.2f} per share.** Twelve-month value at 2027-10-25. Diluted shares: 1,150 million (FQ1 FY2027E guide). Method weight: DCF 100%, comps 0%.")
    a("")
    a(f"Value at {ASOF}, before the one-year equity roll: ${result['per_share_today']:,.2f} per share. The 12-month figure equals that equity value grown one year at the cost of equity, minus dividends of ${DIV_PER_SHARE:.2f} per basic share, divided by 1,150 million diluted shares.")
    a("")
    a(f"Latest close used only as context: ${PRICE_MU:,.2f} on 2026-10-23. The gap between that close and the target is an output, not a constraint.")
    a("")
    a("## 2. Bridge from the model")
    a("")
    a("The unlevered cash flows are built from these forecast lines and from nothing else:")
    a("")
    a("- EBIT, from `income.md`. NOPAT = EBIT × (1 − 15.5%). The 15.5% is applied to EBIT, not to pretax income, so the small interest tax shield is not in the unlevered flow.")
    a("- Depreciation, the memo line in `income.md`, added back.")
    a("- Net capex, from `cashflow.md`, subtracted. This matches the company's net-of-incentives definition.")
    a("- Change in operating net working capital: receivables + inventories + other current assets − accounts payable and accrued expenses − other current liabilities. Contract liabilities, debt, cash, and marketable investments are outside this change.")
    a("- Stock-based compensation is already inside EBIT and is not added back.")
    a("")
    a("Equity value at the valuation date = enterprise value − debt carrying value + cash, restricted cash, and marketable investments − noncurrent customer contract liabilities − noncurrent income taxes payable. All of those balances are the September 3, 2026 amounts. A balance sheet between September 3 and October 25 was not obtained.")
    a("")
    bridge = [
        ["PV of FY2027E–FY2029E unlevered free cash flow", fmt(result["pv_explicit"], 0)],
        ["PV of terminal value", fmt(result["pv_tv"], 0)],
        ["Enterprise value", fmt(result["ev"], 0)],
        ["Debt carrying value (subtract)", fmt(-(NOTES_CV + LEASE0), 0)],
        ["Cash, restricted cash, and marketable investments (add)", fmt(result["cash_inv"], 0)],
        ["Noncurrent customer contract liabilities (subtract)", fmt(-BS_HIST["FY2026A"]["contract"], 0)],
        ["Noncurrent income taxes payable (subtract)", fmt(-TAX_PAYABLE_NC, 0)],
        ["Equity value at 2026-10-25", fmt(result["equity"], 0)],
        ["Diluted shares (millions)", fmt(DILUTED["FY2027E"], 0)],
        ["Per share at 2026-10-25 ($)", fmt(result["per_share_today"], 2)],
        ["Per share at 2027-10-25, the target ($)", fmt(result["pt"], 2)],
    ]
    a(md_table(["Bridge", "Amount"], bridge))
    a("")
    a("Contract liabilities are subtracted because the cash is in the cash balance and the liability is the customers' claim. Deposits are not free cash flow, which is why the repayment is not also deducted inside unlevered free cash flow. The noncurrent tax payable is subtracted for the same reason: the forecast pays new book tax in cash and does not pay this opening payable again.")
    a("")
    a("## 3. DCF")
    a("")
    a("### WACC")
    a("")
    a(md_table(
        ["Component", "Value", "Source"],
        [
            ["Risk-free rate", pct(RF_10Y, 2), "U.S. Treasury par yield curve, 10-year, 2026-10-23, 5.00%. https://home.treasury.gov/resource-center/data-chart-center/interest-rates/daily-treasury-rates.csv/all/202610"],
            ["Beta", f"{BETA:.2f}", "Yahoo Finance 5-year monthly beta versus the S&P 500, 2.23, as of the October 23, 2026 close. GuruFocus prints 3.31 on a different estimator as of October 25, 2026. The 2.23 figure is the one used. The sensitivity grid covers the higher cost of capital."],
            ["Equity risk premium", pct(ERP, 2), "Damodaran implied U.S. ERP, 4.42%, S&P 500 at 7,499.36 on 2026-07-01. October 2026 monthly implied ERP: not obtained. https://aswathdamodaran.substack.com/p/country-risk-determinants-measures"],
            ["Cost of equity", pct(cap["ke"], 2), "Risk-free rate + beta × ERP. Model arithmetic."],
            ["Pretax cost of debt", pct(cap["kd_pre"], 2), "Coupon on the remaining notes plus 4.71% on the finance-lease carrying value, divided by $5,179. Market yield to maturity: not obtained. Weight of debt is under 1%, so the missing yield does not move WACC at the reported precision."],
            ["Tax shield on debt", pct(TAX_FCST, 2), "FY2027E guided rate, held flat. Not the FY2026A effective rate."],
            ["After-tax cost of debt", pct(cap["kd_after"], 2), "Pretax cost × (1 − 15.5%)."],
            ["Equity weight", pct(cap["we"], 2), f"Market value of equity ${fmt(cap['equity_mkt'])} = $877.55 × 1,131 million basic shares. Debt weight uses book debt $5,179. Weights are for WACC only."],
            ["Debt weight", pct(cap["wd"], 2), "Book debt ÷ (market equity + book debt)."],
            ["WACC", pct(cap["wacc"], 2), "Weighted sum. Base case."],
        ],
    ))
    a("")
    a("### Unlevered free cash flow")
    a("")
    a("Cash flows are discounted from October 25, 2026 to the fiscal year-end (the Thursday closest to August 31) on a 365.25-day year. The flow is assumed to arrive at year-end.")
    a("")
    headers = ["", "FY2027E", "FY2028E", "FY2029E", "FY2030E normalized"]
    term = result["term"]
    u_rows = result["rows"]
    a(md_table(headers, [
        ["Year end", str(u_rows[0]["end"]), str(u_rows[1]["end"]), str(u_rows[2]["end"]), "one year after FY2029E"],
        ["Years from 2026-10-25", f"{u_rows[0]['t']:.3f}", f"{u_rows[1]['t']:.3f}", f"{u_rows[2]['t']:.3f}", f"{result['t_tv'] + 1:.3f}"],
        ["EBIT", fmt(u_rows[0]["ebit"]), fmt(u_rows[1]["ebit"]), fmt(u_rows[2]["ebit"]), fmt(term["ebit"])],
        ["NOPAT", fmt(u_rows[0]["ebit"] * (1 - TAX_FCST)), fmt(u_rows[1]["ebit"] * (1 - TAX_FCST)), fmt(u_rows[2]["ebit"] * (1 - TAX_FCST)), fmt(term["nopat"])],
        ["Depreciation added back", fmt(u_rows[0]["da"]), fmt(u_rows[1]["da"]), fmt(u_rows[2]["da"]), fmt(term["da"])],
        ["Net capex", fmt(-u_rows[0]["capex"]), fmt(-u_rows[1]["capex"]), fmt(-u_rows[2]["capex"]), fmt(-term["capex"])],
        ["(Increase) decrease in operating NWC", fmt(-u_rows[0]["dnwc"]), fmt(-u_rows[1]["dnwc"]), fmt(-u_rows[2]["dnwc"]), fmt(-term["d_nwc"])],
        ["Unlevered free cash flow", fmt(u_rows[0]["ufcf"]), fmt(u_rows[1]["ufcf"]), fmt(u_rows[2]["ufcf"]), fmt(term["ufcf"])],
        ["Present value of that year's flow", fmt(u_rows[0]["pv"]), fmt(u_rows[1]["pv"]), fmt(u_rows[2]["pv"]), "inside the terminal value"],
    ]))
    a("")
    a("NOPAT + depreciation − net capex − the increase in operating net working capital equals unlevered free cash flow. The FY2030E column is the normalized year. It is not added again on top of the terminal value. The terminal value is that year's flow grown at g, valued at the FY2029E year-end.")
    a("")
    a("### Terminal method")
    a("")
    a(f"Gordon growth at g = {pct(G)}. The cap is {pct(G_CAP)}, the September 16, 2026 FOMC longer-run median real GDP growth of 2.0% plus longer-run PCE inflation of 2.0% (the sum, not the compound). g is 100 basis points inside that cap because memory revenue over a long period is bits up and price down, so it should not sit on the nominal-GDP ceiling. https://www.federalreserve.gov/monetarypolicy/fomcprojtabl20260916.htm")
    a("")
    a(f"The terminal year is not FY2029E grown at 3%. FY2029E is only the first price cut (−30% ASP). A mid-cycle year is rebuilt. Bits grow at g. Cash cost per bit falls another 5%. Depreciation and capex are the steady state that grows net PP&E at g (capex = (16% + g) / 92% × opening PP&E, which is the algebra of the depreciation rule). Revenue is then set so GAAP gross margin equals {pct(NORM_GM)}. That margin is five points above FY2025A gross margin of 39.8%, the only pre-spike year in the obtained set, and it is far below FY2026A at 80.7%. The five points are the model's allowance for the company's statement that contract floors hold gross margin meaningfully above the prior cycle peak. The floors themselves were not obtained, so 45% is not a company figure. R&D and SG&A grow at g off the FY2029E level. The terminal gross margin asserted in the script is exactly 45%.")
    a("")
    a(f"Terminal value at the FY2029E year-end = FY2030E unlevered free cash flow / (WACC − g) = {fmt(result['tv'])}. Its present value is {fmt(result['pv_tv'])}, which is **{pct(result['tv_share'])} of enterprise value**.")
    a("")
    a("## 4. Sensitivity")
    a("")
    if sens["primary"] == "gm":
        a(f"Normalized gross margin moves the 12-month value more than g does. The range across the margin grid is ${sens['span_gm']:,.0f} per share. The range across the g grid is ${sens['span_g']:,.0f} per share. The primary table is WACC against the mid-cycle gross margin, with g held at {pct(G)}. The base cell is marked BASE. WACC is moved by ±1.5 and ±3.0 percentage points around the base, and the one-year roll uses the cost of equity that reproduces that WACC at the fixed capital structure.")
        a("")
        headers = ["WACC \\ mid-cycle GM", *[pct(gm, 0) for gm in sens["gms"]]]
        rows = []
        for w, row in zip(sens["waccs"], sens["grid_gm"]):
            cells = []
            for gm, pt in zip(sens["gms"], row):
                text = f"${pt:,.0f}"
                if abs(w - cap["wacc"]) < 1e-9 and abs(gm - NORM_GM) < 1e-9:
                    text = f"**${pt:,.0f} BASE**"
                cells.append(text)
            rows.append([pct(w, 2), *cells])
        a(md_table(headers, rows))
        a("")
        a(f"The g grid, at the 45% margin, is the narrower one. Reading across g = 2.0%, 2.5%, 3.0%, 3.5%, 4.0% at the base WACC: " + ", ".join(f"${pt:,.0f}" for pt in sens["grid_g"][2]) + ".")
    else:
        a(f"g moves the 12-month value more than the normalized margin. Range on g: ${sens['span_g']:,.0f}. Range on margin: ${sens['span_gm']:,.0f}. Primary table is WACC against g. Base cell marked BASE.")
        a("")
        headers = ["WACC \\ g", *[pct(g, 1) for g in sens["gs"]]]
        rows = []
        for w, row in zip(sens["waccs"], sens["grid_g"]):
            cells = []
            for g, pt in zip(sens["gs"], row):
                text = f"${pt:,.0f}"
                if abs(w - cap["wacc"]) < 1e-9 and abs(g - G) < 1e-9:
                    text = f"**${pt:,.0f} BASE**"
                cells.append(text)
            rows.append([pct(w, 2), *cells])
        a(md_table(headers, rows))
    a("")
    a("## 5. Comps")
    a("")
    a("Multiples use a full reported year, a share count, and a net-cash bridge from the same document as the earnings, plus a closing price on 2026-10-23. Where that set was not retrieved, the multiple is `not obtained`. Annualizing a single quarter, or using a brokerage consensus, is not done. Trailing multiples are peak-cycle multiples. They are not applied to a normalized Micron year, and they carry a zero weight in the target.")
    a("")
    a(md_table(
        ["Peer", "How they compete", "Price 2026-10-23", "EV/EBIT", "P/E", "EV/Sales", "Source"],
        [
            ["SK hynix", "DRAM, NAND, HBM", "₩1,277,000", "not obtained", "not obtained", "not obtained", "Yonhap closing list, 2026-10-23. Q3 2026 results were not yet released. Consensus is not used."],
            ["Samsung Electronics", "DRAM, NAND, HBM, plus a conglomerate", "₩215,500", "not obtained", "not obtained", "not obtained", "Yonhap, 2026-10-23. A full primary income statement and net-cash bridge were not retrieved for this model."],
            ["Sandisk", "NAND. Named in the Micron 10-K.", f"${sndk['price']:,.2f}", f"{sndk['ebit']:.2f}×", f"{sndk['pe']:.2f}×", f"{sndk['sales']:.2f}×", "FY2026 release, year ended 2026-07-03: revenue $20,248, operating income $12,389, diluted EPS $73.76, cash $4,762, marketable equity securities $1,777, debt $1,849, 149 million shares outstanding. Price: market close 2026-10-23. https://investor.sandisk.com/news-releases/news-release-details/sandisk-reports-fiscal-fourth-quarter-2026-financial-results"],
            ["Kioxia", "NAND. Named in the Micron 10-K.", "ADR $7.99", "not obtained", "not obtained", "not obtained", "Yahoo Finance ADR close, 2026-10-23, after a 3-for-1 split effective around 2026-10-01. A primary full-year filing was not retrieved, so no multiple."],
            ["Western Digital", "HDD after the Sandisk separation. Not named as a memory competitor in the FY2026 10-K.", "$343.67", "not obtained", "not obtained", "not obtained", "Close 2026-10-23. Q1 FY2027 release (quarter ended 2026-10-02) is one quarter: revenue $4,381, GAAP operating income $2,046. A trailing-twelve-month set was not assembled. Not annualized."],
            ["CXMT", "DRAM. Named in the 10-K. Private.", "not obtained", "not obtained", "not obtained", "not obtained", "No public share price."],
            ["YMTC", "NAND. Named in the 10-K. Private.", "not obtained", "not obtained", "not obtained", "not obtained", "No public share price."],
            ["Max / median / min (n = 1)", "Sandisk only. Not a peer-set statistic.", "—", f"{sndk['ebit']:.2f}×", f"{sndk['pe']:.2f}×", f"{sndk['sales']:.2f}×", "With one obtained observation, max = median = min. The row is disclosed and is not used in the target."],
        ],
    ))
    a("")
    a("Prices quoted in Korean won are not translated into dollars. The Yonhap won fix at 15:30 on 2026-10-23 was ₩1,324.6 per dollar; a translated price without a filing multiple would not enter the table above.")
    a("")
    a("## 6. Reconciliation of methods")
    a("")
    a("| Method | Weight | Per share, 12-month | Contribution |")
    a("| --- | --- | --- | --- |")
    a(f"| DCF, mid-cycle terminal | {pct(WEIGHT_DCF, 0)} | ${result['pt']:,.2f} | ${WEIGHT_DCF * result['pt']:,.2f} |")
    a("| Comps | 0% | not used | $0.00 |")
    a(f"| **Target** | **100%** |  | **${result['pt']:,.2f}** |")
    a("")
    a("The zero weight on comps was set because a single NAND peer, on a fiscal year ended July 3, 2026, is not a set, and the DRAM peers' multiples were not obtained from filings. The weight is a constant in the script. It is not a function of how far the DCF sits from the October 23 close. Sandisk's trailing P/E of " + f"{sndk['pe']:.1f}× is a peak-year multiple on peak earnings. Applying it to Micron's FY2026A diluted EPS of $74.33 would be a different, unweighted, arithmetic and is not the target.")
    a("")
    a("## 7. What would move the target")
    a("")
    a(f"The base 12-month value is ${result['pt']:,.2f}. The larger recorded swing in section 4 is ${max(sens['span_gm'], sens['span_g']):,.0f} per share across the primary grid.")
    a("")
    a("- **Mid-cycle gross margin.** This is the terminal price reset. Floors on the strategic agreements were not obtained. A margin nearer FY2026A, or nearer FY2024A, moves the target by more than a 100-basis-point change in g.")
    a("- **WACC, mostly through beta.** The 2.23 beta and the July 1, 2026 ERP are two different dates and, on beta, two vendors disagree. Debt is too small for the missing bond yield to matter.")
    a("- **FY2027E revenue path.** The year is anchored on a $61.5 billion first quarter and on sequential growth. A flat year after that quarter is a lower revenue path than the one in `segments.md`. The model does not print that case as the base, because the company said each quarter grows.")
    a("- **FY2027E–FY2029E net capex.** Only the first half of FY2027E is guided ($25 billion). The $55 / $46 / $40 billion path is a model bridge. Higher capex cuts explicit free cash flow and raises steady-state terminal capex once the PP&E base is larger.")
    a("- **ASP in FY2029E.** The −30% cut is the first normalization, not a return to FY2025A prices. A full give-back of the FY2026A price spike is a different case and was not run. HBM dollars, which would change the CMBU cost gap, were not obtained.")
    a("- **A discretionary buyback.** The model buys back nothing. Spending the $35.16 billion authorization would cut the share count and the cash in the bridge. That program is capacity, not a forecast, and it is not in the target.")
    a("- **Paying the $9.82 billion tax payable, or repaying deposits faster than one-third in FY2029E.** Both are already subtracted at face in the bridge, so faster repayment does not change the target unless the cash was going to earn the 4.44% yield for longer. The yield on that timing is second order.")
    a("")
    a("## 8. Sources")
    a("")
    a("- MU close $877.55 on 2026-10-23, 4:00 p.m. EDT, regular session. Yahoo Finance historical prices, https://finance.yahoo.com/quote/MU/history/ . After-hours $879.90 is not used. Basic shares 1,131 million: FY2026 Form 10-K, outstanding at 2026-09-03. Diluted shares 1,150 million: September 30, 2026 earnings release.")
    a("- Treasury par yields, 2026-10-23: 10-year 5.00%, 1-year 4.44%. U.S. Treasury daily yield curve CSV for October 2026.")
    a("- ERP 4.42% at 2026-07-01: Damodaran, *Country Risk: Determinants, Measures and Implications — The 2026 Edition*. October 2026 update: not obtained.")
    a("- Beta 2.23: Yahoo Finance five-year monthly figure, reported as of 2026-10-25 via the quote field. Alternative 3.31: GuruFocus, as of 2026-10-25, not used.")
    a("- Long-run growth cap 4%: FOMC Summary of Economic Projections, September 16, 2026, longer-run median real GDP 2.0% and PCE inflation 2.0%.")
    a("- Operating inputs: `memory/mu/financials_raw.md` and `memory/mu/research.md`, which cite the FY2026 10-K (filed 2026-10-09), the FY2025 10-K, and the September 30, 2026 earnings release and prepared remarks.")
    a("- Sandisk FY2026 release, August 5, 2026, and the Sandisk close of $1,238.03 on 2026-10-23.")
    a("- SK hynix ₩1,277,000 and Samsung Electronics ₩215,500: Yonhap, October 23, 2026. Kioxia ADR $7.99 and Western Digital $343.67: closing prices on 2026-10-23. Western Digital Q1 FY2027 release, October 22, 2026, used only to explain why a multiple was not computed.")
    a("")
    a("Load-bearing items that remain `not obtained`: strategic-agreement floor prices (the 45% terminal margin and the FY2029E −30% ASP stand in for them), full-year FY2027E capex dollars (the $55 billion year is a bridge off a $25 billion first half), HBM revenue and the wafer trade ratio (the CMBU cost gap is three points, not a measured mix), the October 2026 implied equity risk premium (July 1 is used), and a market yield on Micron's notes (immaterial at this debt weight). Peer EV/EBIT, P/E, and EV/Sales other than Sandisk's FY2026 set are `not obtained` and are not in the target.")
    a("")
    (OUT / "valuation.md").write_text("\n".join(lines), encoding="utf-8")


def main():
    q, q_annual, scale, exit_vs_avg = build_fy27_quarters()
    years = forecast_statements(q_annual, exit_vs_avg, sum(q[4].values()))
    cap = capital_structure()
    result = dcf(years, cap["wacc"], G, NORM_GM, cap["ke"])
    checks = assert_model(q, q_annual, scale, years, cap, result)
    sens = sensitivity(years, cap)
    sndk = sandisk_multiples()
    write_segments(q, q_annual, scale, exit_vs_avg, years)
    write_income(years)
    write_balance(years)
    write_cashflow(years)
    write_valuation(years, cap, result, sens, sndk)
    print(f"asserts passed: {len(checks)}")
    print(f"PT {result['pt']:.2f}")
    print(f"today {result['per_share_today']:.2f}")
    print(f"WACC {cap['wacc']:.4%}  Ke {cap['ke']:.4%}  g {G:.2%}  TVshare {result['tv_share']:.2%}")
    print(f"EV {result['ev']:.1f}  equity {result['equity']:.1f}")
    for lab in FCST:
        y = years[lab]
        print(
            f"{lab} rev {y['rev']:.1f} gm {y['gp']/y['rev']:.3%} ebit {y['ebit']:.1f} "
            f"ni {y['ni']:.1f} eps {y['eps']:.2f} fcf {y['fcf']:.1f} cash {y['cash1']:.1f}"
        )
    for s in SEGS:
        asp = years["FY2027E"]["seg"][s]["asp"]
        print(f"  FY27 {s} asp {asp:.1%} rev {years['FY2027E']['seg'][s]['rev']:.1f}")
    print(f"sensitivity primary {sens['primary']} span_gm {sens['span_gm']:.1f} span_g {sens['span_g']:.1f}")
    print(f"sandisk PE {sndk['pe']:.2f} EV/EBIT {sndk['ebit']:.2f} EV/S {sndk['sales']:.2f}")


if __name__ == "__main__":
    main()
