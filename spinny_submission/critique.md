# Phase 7: Diagnostic Critique of Skill Version 1 (`readout_v1.html`)

**Document:** `critique.md`  
**Auditor:** Senior Applied AI & BI Engineering Team  
**Evaluation Standard:** §4 of `01_CANDIDATE_BRIEF.md` (Readout Requirements)  
**Subject File:** `readout_v1.html` (produced by `skill.md` v1 on prompt A1)  

---

## Executive Assessment

The initial version of the skill (`skill.md` v1) successfully identified the core business truth:
- It refuted the Ops claim that marketing leads collapsed.
- It refuted the Marketing claim that ops inspections failed.
- It correctly located the drop in the stockin rate (offer acceptance) driven by a widening price expectation gap.
- It recognized the Pune app logging bug and recent cohort truncation.

However, a rigorous review against the ten mandatory readout standards in §4 of the brief reveals **ten specific defects** in presentation, numerical evidence, and contract enforcement. These defects are analyzed below with exact quoted text and required remediation.

---

## Detailed Defect Log (Up to 10 Named Defects)

### Defect 1: Hero Number Missing Explicit Comparison Phrasing in Words
- **Quoted Text / Location:** Hero Metric Box: `<div class="hero">-26.9 stockins/wk (-22.3%)</div>`
- **Why it is a Defect:** The number states an absolute and relative decline, but fails to state in words what period it is compared against. A reader cannot verify whether this is vs prior week, vs same month last year, or vs historical baseline.
- **Requirement Violated:** §4.2: *"Every number names what it's compared to, in words: 'vs 8-week baseline', 'vs same weeks last month'. A number with no comparison is a fact, not an answer."*
- **Defect Category:** Presentation / Contractual.
- **Skill Improvement Required:** Update `skill.md` Output Contract to enforce that every hero number must contain an explicit inline comparator string: `"-26.9 stockins/wk (-22.3% vs 8-week baseline: 13 Jul – 31 Aug 2026)"`.

---

### Defect 2: Conversion Rates Displayed Without Denominators
- **Quoted Text / Location:** Panel 2: `<tr><td>Inspection Rate</td><td>43.0%</td><td>42.4%</td><td>-0.6 pts</td></tr>` and `<tr><td>Stockin Rate</td><td>34.2%</td><td>29.0%</td><td>-5.2 pts</td></tr>`
- **Why it is a Defect:** Rates are presented as naked percentages. A City Head cannot tell whether the stockin rate dropped because fewer offers were accepted or because offers were artificially inflated.
- **Requirement Violated:** §4.3: *"Every rate shows its denominator. A rate can move because the denominator changed; the reader must be able to see that."*
- **Defect Category:** Analytical / Contractual.
- **Skill Improvement Required:** In `skill.md` Rules and Output Contract, mandate that no conversion rate may appear without its exact $(N / D)$ tuple, e.g., `34.2% (963 / 2,815) vs 29.0% (187 / 644)`.

---

### Defect 3: Critical Caveats Relegated to Panel Footnote
- **Quoted Text / Location:** Panel 1 Bottom: `<p style="font-size: 10px; color: #94a3b8; margin-top: 10px;">*Note: Week of 28 Sep is 70% mature; 5 Oct is 4 days complete.</p>`
- **Why it is a Defect:** Placing the cohort lag and partial week qualifications in a tiny footer note means a busy executive glancing at the table will see 63 and 24 and panic, believing stockins collapsed by 80%.
- **Requirement Violated:** §4.4: *"Caveats sit next to the number they qualify. Not in a footer, not in a tooltip. A partial or incomplete period is marked on the chart it appears in."*
- **Defect Category:** Data Governance / Visual Design.
- **Skill Improvement Required:** In `skill.md` Rules, require that caveats must be physically attached as inline visual badges directly adjacent to or inside the table rows and data bars (`28 Sep (63) [Lag: ~70% mature]`, `05 Oct (24) [Partial: 4 of 7 days]`).

---

### Defect 4: Panel Titles Name the Axes/Topics Instead of the Analytical Message
- **Quoted Text / Location:** Panel Headers: `<h3>Panel 1: Weekly Stockin Trend</h3>`, `<h3>Panel 2: Funnel Conversion Stages</h3>`, `<h3>Panel 3: Factor Decomposition</h3>`
- **Why it is a Defect:** The titles are passive labels describing the data structure rather than delivering the executive insight. A 30-second reader learns nothing from the headers.
- **Requirement Violated:** §4.10: *"Panel titles state the message, not the axes."*
- **Defect Category:** Analytical Communication.
- **Skill Improvement Required:** Update `skill.md` Method and Output sections to mandate active headline phrasing:
  - Panel 1: *"Mature Stockins Dropped 22.3%; Apparent 80% Collapse is Truncation Lag"*
  - Panel 2: *"Conversion Deteriorated Exclusively at Offer Acceptance (Pricing Stage)"*
  - Panel 3: *"Stockin Rate Collapse Explains 62% of Total Stockin Loss"*

---

### Defect 5: Decomposition Reconciled in Text Without Showing the Numerical Residual
- **Quoted Text / Location:** Panel 3: `<p style="font-size: 11px; color: #475569; margin-top: 8px;">Reconciles to observed delta.</p>`
- **Why it is a Defect:** The report claims reconciliation without explicitly displaying the residual number ($0.00$). The reader cannot audit whether the components truly sum to $-26.9$.
- **Requirement Violated:** §4.5: *"The split adds up. If the page says where the change came from, the pieces sum to the change, or the residual is shown as its own number."*
- **Defect Category:** Mathematical Transparency.
- **Skill Improvement Required:** In `skill.md` Rules and Decomposition section, mandate an explicit line item: `Residual = 0.00 stockins/wk (Exact Multiplicative-to-Additive Chain)`.

---

### Defect 6: Ruled-Out Hypotheses Lack Numerical Test Scores and Standard Deviations
- **Quoted Text / Location:** Panel 4: `<tr><td>Marketing cut spend</td><td>Refuted</td><td>Leads down 5.7%, which is within normal variation.</td></tr>`
- **Why it is a Defect:** Stating "within normal variation" without showing the baseline standard deviation or z-score turns an analytical proof into an unverified assertion.
- **Requirement Violated:** §4.6: *"What it isn't. The explanations ruled out, with the number that rules them out."*
- **Defect Category:** Analytical Rigor / Evidence.
- **Skill Improvement Required:** In `skill.md` Method, require that ruled-out claims must display the exact baseline distribution metrics: `Leads: 903.0 vs 956.9 baseline (Δ = -53.9 leads, Z = -1.65σ <= 2.0σ; baseline σ = 32.5 leads/wk; stockin impact = -6.8/wk)`.

---

### Defect 7: Reliance on Raw Tables Instead of Graphical Visuals
- **Quoted Text / Location:** Panels 1 and 3 in `readout_v1.html` rely entirely on plain HTML `<table>` elements with no SVG visuals.
- **Why it is a Defect:** Tables fail the 30-second executive cognition requirement. An executive cannot instantly contrast baseline stability against the pricing drop without visual bar and waterfall charts.
- **Requirement Violated:** §4 visual contract: *"Reader should understand the answer in approximately 30 seconds... Maximum six chart panels. Bars start at zero."*
- **Defect Category:** Presentation / UX.
- **Skill Improvement Required:** In `skill.md` Output Contract, mandate inline standalone SVG visual charts for Panels 1 and 3, featuring zero-based bars, distinct cohort shading, and visual waterfall flow.

---

### Defect 8: Omission of Offer-to-Expected Price Ratio and Car-Age Concentration
- **Quoted Text / Location:** Panel 5: Lists `Offer Price` and `Expected Price` in rupees, but omits the ratio `Offer / Expected` and vehicle age breakdown.
- **Why it is a Defect:** Absolute price movements are hard to evaluate without the percentage ratio ($92.5\% \rightarrow 91.6\%$). Additionally, omitting that 4-6y cars drove $-12.0$ stockins/wk of the decline obscures where the pricing problem was concentrated.
- **Requirement Violated:** §3 Method Step 5 & 6 (Segment Breakdown & Pricing Spread Analysis).
- **Defect Category:** Analytical Depth.
- **Skill Improvement Required:** In `skill.md` Method, require reporting the price ratio ($\frac{\text{offer}}{\text{expected}}$) and identifying the dominant segment contributor.

---

### Defect 9: Gate Reporting Lacks Numerical Thresholds and Test Scores
- **Quoted Text / Location:** Panel 6: `<tr><td>Statistical Significance</td><td>SIGNIFICANT (>2σ)</td></tr>`
- **Why it is a Defect:** Stating `>2σ` is a label, not evidence. The gate must display the calculated number ($Z = -3.24\sigma$).
- **Requirement Violated:** §3 Gates: *"Checks that can fail visibly. Each one says what evidence proves it passed (a number, not 'checked')."*
- **Defect Category:** Analytical Governance.
- **Skill Improvement Required:** In `skill.md` Gates, mandate that Gate 5 must output: `Observed: Z = -3.24σ (Target 93.5 vs Base 120.4, σ = 8.3). Passed: Exceeds 2.0σ threshold.`

---

### Defect 10: Incomplete Confidence Framing (Missing Falsification Conditions)
- **Quoted Text / Location:** Panel 6 Footer: `<p style="font-size: 11px; margin-top: 10px;">Confidence: High on stage, moderate on causality.</p>`
- **Why it is a Defect:** Stating confidence without explicitly stating what external facts would alter the conclusion fails the executive review standard.
- **Requirement Violated:** §4.7: *"Confidence, and what would change it."*
- **Defect Category:** Epistemic Integrity.
- **Skill Improvement Required:** In `skill.md` Output Contract, mandate an explicit "What would change it" clause specifying required missing data (e.g., competitor pricing, inspector schedules).

---

## Action Plan for Skill Version 2 (`skill.md` v2)

1. Enforce strict string templates for hero numbers with explicit comparators in words.
2. Mandate $(N / D)$ for every single rate displayed in the report.
3. Require visual caveat chips placed directly adjacent to affected figures.
4. Replace passive panel headers with active, message-driven headlines.
5. Require explicit numerical display of the mathematical residual ($0.00$).
6. Mandate z-scores and baseline $\sigma$ in ruled-out explanations.
7. Mandate inline, standalone SVG charts with zero-based axes.
8. Add offer-to-expected ratio and segment concentration analysis.
9. Require exact numeric test values in all gate checks.
10. Add explicit falsification conditions to the confidence section.

---
*End of Critique.*
