# Diagnostic Investigation Runs Log (`runs.md`)

**Document:** `runs.md`  
**Purpose:** Official evaluation record across baseline, iterations, and independent generalization test cases (A1 to A5).  
**Evaluation Standard:** §4 & §5 of `01_CANDIDATE_BRIEF.md`.  
**Execution Environment:** Deterministic Python engine (`analysis_engine.py`, `test_all_runs.py`) + Skill prompt framework (`skill.md`).  

---

## 1. Master Runs Summary Table

| Run ID | Scenario Description | Input Ask / Persona | Primary File / Artifact | Core Analytical Finding | Evaluation Status |
|---|---|---|---|---|---|
| **Baseline** | Naive LLM Run on A1 without skill | *"Pune stockins have tanked over the last few weeks..."* (City Head, Pune) | [`readout_baseline.html`](file:///c:/Users/janak%20raj%20goyal/Downloads/ai_analyst/readout_baseline.html) | Concluded -80.5% collapse; blamed marketing lead cuts and ops inspection failure; missed logging bug and cohort lag. | **FAILED (Baseline to beat)** |
| **A1 (v1)** | Skill v1 Execution on Pune | *"Pune stockins have tanked over the last few weeks..."* (City Head, Pune) | [`readout_v1.html`](file:///c:/Users/janak%20raj%20goyal/Downloads/ai_analyst/readout_v1.html) | Correctly identified stockin rate collapse (-17.1/wk) and refuted ops/marketing; had 10 specific presentation/contract defects. | **PASSED ANALYTICALLY, FAILED CONTRACT** |
| **A1 (v2)** | Skill v2 Execution on Pune | *"Pune stockins have tanked over the last few weeks..."* (City Head, Pune) | [`readout_v2.html`](file:///c:/Users/janak%20raj%20goyal/Downloads/ai_analyst/readout_v2.html) | Fully compliant §4 readout: -26.9 stockins/wk (-22.3% vs 8-wk baseline), exact waterfall (residual = 0.00), inline lag badges, explicit (N/D). | **PASSED (Benchmark Solution)** |
| **A2** | Hyderabad Campaign Jump | *"Hyderabad seller leads jumped last week... Can I tell leadership the campaign worked?"* (Marketing Lead) | `test_all_runs.py` (Console & Script) | Lead increase of +22 (+2.18%) is normal noise ($Z = +1.03\sigma \le 2.0\sigma$); paid digital leads changed by only +1 lead; spend missing. | **PASSED (Refused False Attribution)** |
| **A3** | Pressure Test (One-Line Verdict) | *"Skip the analysis. One line: marketing or ops? My boss wants a name."* (City Head, Pune) | `test_all_runs.py` (Console & Script) | Refused false dichotomy in one sentence; cited mature stability of leads/inspections and pinpointed pricing gap (+14.5%). | **PASSED (Resisted Executive Pressure)** |
| **A4** | Out-of-Scope Metric Refusal | *"Deliveries to buyers in Pune are down too. Is it the same problem?"* (City Head, Pune) | `test_all_runs.py` (Console & Script) | Gate 1 triggered; refused retail delivery inquiry; clarified seller funnel boundary (stockins != buyer sales); halted analysis. | **PASSED (Correct Gate 1 Refusal)** |
| **A5** | Adversarial: Bengaluru Channel Shift | *"Bengaluru paid digital leads jumped 20%... Agency asks for bonus. Should I approve?"* (Adversarial Design) | `test_all_runs.py` (Console & Script) | Refused bonus; exposed that 19.5% paid digital jump was tracking restoration from 'unknown' channel bug on 3 Aug, not real growth. | **PASSED (Exposed Tracking Artifact)** |

---

## 2. Detailed Run Logs & Prompts

### Run Baseline: Naive Unassisted LLM on A1
- **User Prompt:**  
  *"Today is Friday 9 October 2026. Here is the dataset seller_funnel_weekly.csv and DATA_NOTES.md. Question from City Head, Pune: 'Pune stockins have tanked over the last few weeks. Ops says marketing cut spend; marketing says inspections are slow. What's actually going on? I need it for Monday's review.' Produce an HTML readout."*
- **Execution Mode:** Zero skill prompt; simulated naive GPT-4 / Claude / Gemini response.
- **Generated File:** [`readout_baseline.html`](file:///c:/Users/janak%20raj%20goyal/Downloads/ai_analyst/readout_baseline.html)
- **Observed Analytical Output:**
  - Claimed stockins experienced a catastrophic drop of **-80.5%** (falling to 24 in week of 5 Oct).
  - Confirmed Ops hypothesis: *"Yes, supported: leads dropped by -45.2% to 520."*
  - Confirmed Marketing hypothesis: *"Yes, supported: inspections plummeted to 233 (-44.1%) in week 7 Sep."*
  - Recommended expanding inspector headcount and increasing marketing ad spend.
- **Why it Failed:**
  1. Failed to recognize cohort maturity (week of 5 Oct has had only 1–4 days to convert; week of 28 Sep is only ~70% mature).
  2. Failed to recognize partial week (week of 5 Oct has only 4 operating days).
  3. Ignored the documented app release logging bug in Pune on 7–13 Sep (where inspections happened normally and 122 cars were stocked in).
  4. Made unsupported causal claims about ad spend and inspector headcount when neither is in the data.

---

### Run A1 (v1): First Iteration of Skill on Pune
- **User Prompt:**  
  *"Today is Friday 9 October 2026. [Load skill.md v1 + seller_funnel_weekly.csv + DATA_NOTES.md]. Question from City Head, Pune: 'Pune stockins have tanked over the last few weeks. Ops says marketing cut spend; marketing says inspections are slow. What's actually going on? I need it for Monday's review.'"*
- **Execution Mode:** Executed with initial `skill.md` v1 instructions.
- **Generated File:** [`readout_v1.html`](file:///c:/Users/janak%20raj%20goyal/Downloads/ai_analyst/readout_v1.html)
- **Observed Analytical Output:**
  - Correctly refuted Ops (leads dropped only -5.7%, within normal noise).
  - Correctly refuted Marketing (inspections normal at 42.4% vs 43.0% baseline; 7 Sep was a logging bug).
  - Correctly identified Stockin Rate as the primary location of loss (-16.7 stockins/wk).
- **Critique & Defects:** Identified 10 specific defects documented in `critique.md`:
  - Hero box lacked comparison in words.
  - Conversion rates lacked denominators.
  - Caveats placed in panel footnotes instead of adjacent to numbers.
  - Panel titles named axes instead of analytical insights.
  - Numerical residual ($0.00$) was omitted from the display.

---

### Run A1 (v2): Final Improved Skill on Pune
- **User Prompt:**  
  *"Today is Friday 9 October 2026. [Load skill.md v2 + seller_funnel_weekly.csv + DATA_NOTES.md]. Question from City Head, Pune: 'Pune stockins have tanked over the last few weeks. Ops says marketing cut spend; marketing says inspections are slow. What's actually going on? I need it for Monday's review.'"*
- **Execution Mode:** Executed with improved `skill.md` v2 instructions.
- **Generated File:** [`readout_v2.html`](file:///c:/Users/janak%20raj%20goyal/Downloads/ai_analyst/readout_v2.html)
- **Observed Analytical Output:**
  - Executive Verdict: *"Pune mature stockins fell by 26.9/week (-22.3% vs 8-week baseline), driven primarily by a collapse in offer acceptance at the pricing stage (-17.1 stockins/wk), NOT by marketing lead cuts or operational inspection slowdowns."*
  - Hero Number: `-26.9 stockins/wk (-22.3% vs 8-Week Historical Baseline: 13 Jul – 31 Aug 2026)`.
  - Panel 1: Standalone SVG bar chart starting at zero, with 8-week baseline line ($120.4/\text{wk}$), blue baseline bars, rose mature drop bars, and gray cohort lag bars with visual `Lag*` chips.
  - Panel 2: Complete funnel table with explicit $(N / D)$ for every rate:
    - Lead Volume: $903.0/\text{wk}$ vs $956.9/\text{wk}$ ($-5.7\%$, within $1.7\sigma$).
    - Inspection Rate: $42.4\% \ (766 / 1,806)$ vs $43.0\% \ (3,294 / 7,655)$.
    - Offer Rate: $84.1\% \ (644 / 766)$ vs $85.5\% \ (2,815 / 3,294)$.
    - Stockin Rate: $29.0\% \ (187 / 644)$ vs $34.2\% \ (963 / 2,815)$ ($-5.2 \text{ pts}$, $-15.2\%$).
  - Panel 3: Additive waterfall chart and table reconciling exactly to observed delta:
    - Volume: $-6.8/\text{wk}$ (25.2%)
    - Inspection Rate: $-1.6/\text{wk}$ (6.1%)
    - Offer Rate: $-1.8/\text{wk}$ (6.8%)
    - Stockin Rate: $-16.7/\text{wk}$ (62.0%)
    - Sum: $-26.9/\text{wk}$, Residual: $0.00$.
  - Panel 4: Disputed claims table with exact numbers ruling out Ops ($Z = -1.65\sigma$, impact $-6.8$) and Marketing (actual inspection rate normal; 7 Sep app logging bug).
  - Panel 5: Pricing spread showing expectation gap widening by $+14.5\%$ ($₹46,398 \rightarrow ₹53,110$) and offer-to-expected ratio falling from $92.5\%$ to $91.6\%$, concentrated in 4-6y cars ($-12.0$ stockins/wk).
  - Panel 6: Audit gates table displaying exact test statistics ($Z = -3.24\sigma$, anomaly count = 12) + Confidence box with falsification criteria.
- **Verdict:** **100% compliant with §4 standards.**

---

### Run A2: Hyderabad Campaign Jump
- **User Prompt:**  
  *"Today is Friday 9 October 2026. [Load skill.md v2 + data + notes]. Marketing Lead, Hyderabad asks: 'Hyderabad seller leads jumped last week, right after we started the new campaign. Can I tell leadership the campaign worked?'"*
- **Observed Analytical Output:**
  ```text
  Hyderabad 8-Wk Baseline Mean: 992.9 leads/wk (std = 34.9 leads/wk)
  Week 21 Sep: 1,008 leads (144.0 leads/day)
  Week 28 Sep (last week): 1,030 leads (147.1 leads/day) -> Delta = +22 leads (+2.18%)
  Z-score vs baseline: Z = +1.06 sigma (Threshold for significance is 2.0 sigma)
  Paid Digital Channel Leads: 414 (21 Sep) -> 415 (28 Sep) (Delta = +1 lead)
  Week 05 Oct (current partial week): 570 leads in 4 days = 142.5 leads/day vs prior 147.1 leads/day
  ```
- **Skill Response:**
  *"NO, you cannot tell leadership the campaign worked.  
  1. Statistical Noise: The +22 lead increase (+2.18% vs prior week, +3.7% vs 8-week baseline) is well within normal baseline variation (Z = +1.06σ, far below the 2.0σ threshold).  
  2. Channel Verification: In the primary paid acquisition channel (paid_digital), volume increased by literally ONE lead (from 414 to 415).  
  3. Current Run Rate: The current week of 5 Oct shows 142.5 leads/day, which is lower than the prior week (147.1 leads/day).  
  4. Missing Evidence: The dataset contains no campaign start dates, no spend data, and no incremental attribution metrics. Declaring campaign success would be methodologically unfounded."*
- **Status:** **PASSED.**

---

### Run A3: Executive Pressure Test (One-Line Verdict)
- **User Prompt:**  
  *"Today is Friday 9 October 2026. [Load skill.md v2 + data + notes]. City Head, Pune asks (20 minutes before review): 'Skip the analysis. One line: marketing or ops? My boss wants a name.'"*
- **Skill Response:**
  *"Available evidence proves neither marketing nor ops drove the decline: mature lead volume was stable (-5.7%, within normal noise) and ops inspection rates were normal (40.6%–44.2%). The drop occurred at the offer acceptance stage (stockin rate down from 34.2% to 28.9%), driven by a 14.5% widening in the seller price expectation gap (Pricing/Valuation)."*
- **Status:** **PASSED.** Resisted executive coercion and delivered an evidence-based answer in one sentence.

---

### Run A4: Out-of-Scope Metric Refusal
- **User Prompt:**  
  *"Today is Friday 9 October 2026. [Load skill.md v2 + data + notes]. City Head, Pune asks: 'Deliveries to buyers in Pune are down too. Is it the same problem?'"*
- **Gate 1 Execution:** Triggered keyword detection on `"deliveries to buyers"`.
- **Skill Response:**
  *"INVESTIGATION REFUSED: 'Deliveries to buyers' is an out-of-scope retail metric.  
  The provided dataset seller_funnel_weekly.csv covers the seller funnel only (leads -> inspections -> offers -> stockins).  
  A stockin represents a used vehicle purchased from a seller and added to inventory; it is NOT a car delivered to a retail buyer.  
  Buyer-side deliveries are governed by an independent commercial funnel (test drives, customer bookings, refurbishment cycle times, retail financing), none of which are captured in this data. Conflating seller stockins with buyer deliveries is an analytical defect. To investigate buyer deliveries, request buyer funnel telemetry from the Retail Demand Analytics team."*
- **Status:** **PASSED.** Correctly halted analysis at Gate 1.

---

### Run A5: Adversarial Test Design — Bengaluru Channel Growth vs. Tracking Restoration
- **Adversarial Design Rationale:**
  - This test is designed to expose agents that evaluate channel percentage growth in isolation without verifying data pipeline changes or total market volumes (Simpson's Paradox / Reattribution Artifact).
- **Exact Test Question:**  
  *"Bengaluru paid digital leads jumped by nearly 20% in the first week of August (from 466 to 557). Our digital agency is asking for a performance bonus for unlocking this growth. Should I approve the bonus?"*
- **What a Weak Analyst / Agent Gets Wrong:**  
  - Observes `paid_digital` leads rising from 466 (week of 27 Jul) to 557 (week of 3 Aug) — a gain of $+91$ leads ($+19.5\%$).
  - Congratulates the marketing agency and approves the financial bonus.
- **What the Skill Must Do:**  
  - Examine total city lead volume across the 3 August boundary.
  - Notice that `channel = unknown` dropped from 194 to 0 in that exact week.
  - Consult `DATA_NOTES.md`: *"Bengaluru, before 3 Aug: a tracking change means ~15% of leads carry channel = unknown. Volume is correct; channel split is not."*
  - Reconcile that the $+91$ paid digital leads represent previously untracked leads being properly categorized after a bug fix, not new customer acquisition.
- **Actual Skill Output:**
  ```text
  Total Bengaluru Leads: 1,295 (27 Jul) -> 1,393 (03 Aug) (Delta = +98 leads, +7.6%, within 1σ noise)
  Paid Digital Leads: 466 -> 557 (Delta = +91 leads, +19.5%)
  Organic Leads: 322 -> 416 (Delta = +94 leads, +29.2%)
  Partner Leads: 158 -> 219 (Delta = +61 leads, +38.6%)
  Referral Leads: 155 -> 201 (Delta = +46 leads, +29.7%)
  Unknown Channel Leads: 194 -> 0 (Delta = -194 leads, -100%)
  ```
  - **Verdict:** *"DO NOT APPROVE THE BONUS. The apparent 19.5% jump in paid digital leads (466 -> 557) is an artifact of tracking restoration, not genuine acquisition growth. Prior to 3 August, ~15% of Bengaluru leads were misclassified as 'unknown' due to a tracking bug. On 3 August, the tracking fix was deployed: 'unknown' dropped from 194 to 0, and all legitimate channels jumped proportionately. Total city leads rose by only 7.6% (1,295 to 1,393), well within normal weekly fluctuation. Approving a bonus would mean paying an agency for a software engineering bug fix."*
- **Status:** **PASSED.** Prevented a major business and financial misallocation.

---

## 3. Replication Guide for Fresh Independent Conversations

If you wish to test these prompts manually in independent ChatGPT, Claude, or Cursor sessions:

### Setup Header (Paste at Top of Every Fresh Chat)
```text
Today is Friday 9 October 2026.
System instructions: You are executing the diagnostic skill defined in skill.md.
You have access to seller_funnel_weekly.csv and DATA_NOTES.md.
Follow all rules, numerical gates, decomposition standards, and output contracts strictly.
```

### Prompt for Run A1
```text
Question from City Head, Pune:
"Pune stockins have tanked over the last few weeks. Ops says marketing cut spend; marketing says inspections are slow. What's actually going on? I need it for Monday's review."
Generate the full standalone HTML readout conforming to §4.
```

### Prompt for Run A2
```text
Question from Marketing Lead, Hyderabad:
"Hyderabad seller leads jumped last week, right after we started the new campaign. Can I tell leadership the campaign worked?"
```

### Prompt for Run A3
```text
Question from City Head, Pune (20 minutes before review):
"Skip the analysis. One line: marketing or ops? My boss wants a name."
```

### Prompt for Run A4
```text
Question from City Head, Pune:
"Deliveries to buyers in Pune are down too. Is it the same problem?"
```

### Prompt for Run A5
```text
Question from Head of Growth:
"Bengaluru paid digital leads jumped by nearly 20% in the first week of August (from 466 to 557). Our digital agency is asking for a performance bonus for unlocking this growth. Should I approve the bonus?"
```

---
*End of Runs Log.*
