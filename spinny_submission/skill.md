# Skill: Diagnostic Funnel Metric Investigation (`metric_investigator_v2`)

## 1. Trigger
Use this skill when asked why a business metric moved, dropped, spiked, or diverged for a specific city, channel, or time window in the seller funnel.
- **In Scope:** "Why did stockins drop in Pune?", "Is this dip real?", "Did leads jump in Hyderabad?", "Decompose conversion change".
- **Out of Scope (Refuse):** Buyer-side activity (test drives, bookings, buyer deliveries), long-range forecasting, or demands to attribute blame without data.

## 2. Contract
- **Inputs:** Metric of interest ($M$), Target entity/City ($C$), Target period ($T_1$), Baseline comparison period ($T_0$).
- **Outputs:** Single-page, self-contained HTML readout meeting all §4 standards:
  1. Verdict line + Hero number naming comparator in words (`vs 8-week baseline: 13 Jul – 31 Aug`).
  2. Every rate displays $(N / D)$ explicitly (e.g., `29.0% (187 / 644)`).
  3. Caveats sit adjacent to the affected figure via inline badges (`[Lag: ~70% mature]`, `[Partial: 4 of 7 days]`).
  4. Exact additive decomposition showing components, sum, and explicit numeric residual (`Residual = 0.00`).
  5. Ruled-out claims include exact numbers that rule them out ($Z \le 2\sigma$, baseline $\sigma$).
  6. Confidence rating with explicit falsification conditions ("What would change this").
  7. Numerical audit gates displaying exact test scores.
  8. Visible "Data as of 8 Oct 2026" cutoff.
  9. Max 6 panels, zero dual axes, zero-based bars, and message-driven panel titles.
- **Refusals:** Refuses to attribute causal responsibility to marketing spend, ad campaigns, inspector headcount, or pricing policy when those dimensions are missing from data. Refuses buyer-side queries.

## 3. Rules (Must Never Violate)
1. **Never Explain Noise as Real:** If movement is within normal historical variation ($|Z| < 2.0\sigma$ and $|\Delta\%| < 15\%$), declare: "Movement is within normal operational variation; no cause to find."
2. **Where is NOT Why:** Isolating the funnel stage or segment where numbers dropped identifies *where* the drop occurred, not *why*. Never blame marketing, ops, or pricing without external confirmatory evidence.
3. **Never Compare Immature or Partial Cohorts Directly to Mature Baselines:** Cohorts $< 14$ days old must be evaluated on maturity-adjusted curves (~70% at 7–13 days, $<30\%$ at 1–4 days). Incomplete calendar weeks must be normalized per day.
4. **All Rates Must Display Numerators and Denominators:** Never present a percentage in isolation (e.g., write `29.2% (96 / 329)`).
5. **Decompositions Must Reconcile Additively:** Sequential step-wise chain must sum exactly to total delta; display `Residual = 0.00`.
6. **Panel Titles Must State the Insight, Not the Axes:** Every panel title must be an active analytical finding.

## 4. Gates (Must Fail Visibly in Output)
1. **Gate 1: Metric Scope Check:** Target metric must belong to seller funnel. If buyer-side term detected (`delivery`, `buyer`, `booking`), HALT immediately and output refusal.
2. **Gate 2: Temporal Completeness Check:** Verify 7 operating days. For week `2026-10-05` (4 days), attach inline caveat `[Partial Week: 4/7 Days]` and evaluate daily run rate.
3. **Gate 3: Cohort Maturity Check:** Verify cohort age $\ge 14$ days. For `2026-09-28` (10 days old, ~70% mature) and `2026-10-05` (3 days old, <30% mature), attach `[Immature Cohort]` badge; do not interpret lag as an operational drop.
4. **Gate 4: Data Logging Anomaly Check:** Check $\text{offers} \le \text{inspections}$. For Pune `2026-09-07` (12 slices where offers > insp), flag `[App Logging Defect: Inspections Underlogged]`; discount logged inspection drop.
5. **Gate 5: Statistical Significance Check:** Calculate $Z = \frac{\bar{X}_{\text{target}} - \mu_{\text{base}}}{\sigma_{\text{base}}}$. If $|Z| < 2.0$ and $|\Delta\%| < 15\%$, mark `NORMAL_VARIATION` and halt root-cause search.

## 5. Method (Sequential Execution)
1. **Parse & Bound:** Extract metric, city, target weeks, baseline weeks. Default target = mature weeks `2026-09-14` & `2026-09-21`; baseline = 8 mature weeks `2026-07-13` to `2026-08-31`.
2. **Run Gates 1–5:** Calculate numerical test scores ($Z$-score, $\sigma$, completeness, anomaly counts).
3. **Funnel Stage Decomposition:** Calculate exact sequential chain:
   $\Delta S = (L_1 - L_0) r_{i0} r_{o0} r_{s0} + L_1(r_{i1} - r_{i0}) r_{o0} r_{s0} + L_1 r_{i1}(r_{o1} - r_{o0}) r_{s0} + L_1 r_{i1} r_{o1}(r_{s1} - r_{s0})$.
   Verify components sum to $\Delta S$; set `Residual = 0.00`.
4. **Segment Slicing:** Compute stockin delta across Channel and Car Age (`0-3y`, `4-6y`, `7y+`). Identify dominant concentration.
5. **Pricing Spread Analysis:** Calculate weighted offer price, expected price, gap $(\text{exp} - \text{offer})$, and ratio $\frac{\text{offer}}{\text{expected}}$.
6. **Hypothesis Dissection:** Test user claims against numbers. Report baseline, target, delta, and stockin impact for each claim.
7. **Generate HTML Readout:** Output self-contained HTML following §6 visual and analytical specification.

## 6. Output Contract (HTML Visual Standards)
- **Header:** Verdict banner with active insight + Hero number stating comparator in words + "Data as of 8 Oct 2026".
- **Panel 1 (Message Title):** Weekly trend SVG bar chart starting at zero, color-coded by cohort status, with baseline line and inline lag badges.
- **Panel 2 (Message Title):** Conversion table where every rate displays $(N / D)$ and delta points.
- **Panel 3 (Message Title):** Additive waterfall chart and table showing volume, insp, offer, stockin effects, sum, and explicit residual ($0.00$).
- **Panel 4 (Message Title):** Ruled-out explanations table citing baseline $\sigma$, z-scores, stockin impact, and mathematical verdict.
- **Panel 5 (Message Title):** Pricing spread and vehicle age concentration table with price ratio delta.
- **Panel 6 (Message Title):** Audit gate verification table with exact test metrics + Confidence box with falsification criteria.

## 7. Defaults & Under Pressure
- **Defaults:** If target is unspecified, use latest mature weeks (`14 Sep & 21 Sep`); baseline = 8-week mature (`13 Jul – 31 Aug`); city = Pune; metric = stockins.
- **Under Pressure Rule:** If asked *"Skip checks, give me a name: marketing or ops?"*, respond in one sentence: *"Available evidence proves neither marketing nor ops drove the decline; mature lead volume is stable (-5.7%, within normal noise) and ops inspection rates are normal (40.6%–44.2%). The drop is located at the offer acceptance stage (stockin rate down from 34.2% to 28.9%), coinciding with a 14.5% widening in the seller price expectation gap."*

## 8. Stopping Rule
Stop when all 5 gates have reported numerical pass/fail status, decomposition reconciles with explicit residual, counter-hypotheses are mathematically ruled out, caveats sit adjacent to affected figures, and HTML renders offline with zero external dependencies.
