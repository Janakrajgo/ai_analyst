# Spinny Applied AI Take-Home Investigation

A reusable analytical skill and deterministic diagnostic engine that answers:  
**"Why did this business metric move for a particular city and period?"**

Built for the Spinny Applied AI assignment, this project diagnoses seller-funnel movements, separates noise from statistical signal, decomposes multi-stage conversion shifts, accounts for data pipeline glitches and cohort truncation, and renders a standalone, executive-ready HTML readout readable in 30 seconds.

---

## 1. Project Purpose & Architecture

Across a two-sided used-car marketplace like Spinny, business leaders and City Heads frequently ask:  
*"Why did stockins drop in Pune?", "Is this dip real?", "Did the new ad campaign drive our lead spike?"*

Standard unassisted AI tools fail on these questions:
1. They explain normal statistical noise as real phenomena.
2. They affirm executive confirmation bias (e.g., blaming whoever was suspected).
3. They mistake data pipeline logging bugs and cohort maturity lag for operational collapses.
4. They generate unstructured pages of text without explicit denominators or mathematical reconciliation.

### Architecture Overview

```
User Query (e.g., A1-A5)
         │
         ▼
  [skill.md (v2)] ──► Enforces Rules, Numerical Gates, Refusal Boundaries
         │
         ▼
[data_validation.py] ─► Scope (Gate 1), Completeness (Gate 2), Maturity (Gate 3), Anomalies (Gate 4), Significance (Gate 5)
         │
         ▼
[analysis_engine.py] ─► Baseline Calculation, Z-Score Testing, Pricing Spread Dynamics, Hypothesis Refutation
         │
         ▼
[decomposition.py] ──► Multiplicative-to-Additive Factor Decomposition (Residual = 0.00)
         │
         ▼
[report_generator.py] ► Offline, Self-Contained HTML Readout (Zero External CDN Dependencies)
```

The system strictly divides labor:
- **Python / Pandas:** Executes all deterministic arithmetic, aggregations, ratios, and factor chains.
- **Skill Framework (`skill.md`):** Governs analytical reasoning, prevents causal overreach, enforces gates, and formats executive communication.

---

## 2. Repository Structure

| File | Purpose / Description |
|---|---|
| `skill.md` | Reusable diagnostic method ($\le 2$ pages) structured per brief specifications. |
| `readout_baseline.html` | Naive baseline run on A1 (unassisted LLM failure modes). |
| `readout_v1.html` | Initial run of skill v1 on A1. |
| `critique.md` | Rigorous evaluation identifying 10 specific defects in `readout_v1.html`. |
| `readout_v2.html` | Final, pristine executive HTML readout on A1 fixing all 10 critique defects. |
| `runs.md` | Complete log of runs A1 to A5 with mathematical outputs and evaluation verdicts. |
| `writeup.md` | 1-page executive summary covering additions, key decisions, omissions, and monitoring. |
| `ai_log.md` | Documented AI collaboration, division of labor, and 3 genuine errors caught and corrected. |
| `SOURCE_ANALYSIS.md` | Comprehensive source review of brief, business model, dataset, and assumptions. |
| `DATA_AUDIT.md` | 13-point data audit report with verified figures and distributions. |
| `data_audit.py` | Python script executing all 13 data integrity checks on `seller_funnel_weekly.csv`. |
| `analysis_engine.py` | Core analytical engine coordinating gates, baseline comparisons, and pricing analysis. |
| `data_validation.py` | Implementation of Gates 1 through 5 with numerical pass/fail thresholds. |
| `decomposition.py` | Exact additive sequential factor decomposition (Residual = 0.00). |
| `report_generator.py` | Modular HTML report generator creating self-contained, offline-compatible readouts. |
| `test_all_runs.py` | Automated test suite verifying runs A1 through A5. |

---

## 3. Dataset & Known Data Limitations

The dataset `seller_funnel_weekly.csv` contains **660 rows** representing weekly operations from **13 July 2026 to 5 October 2026** across 4 cities:
$$\text{Leads} \rightarrow \text{Inspections Done} \rightarrow \text{Offers Made} \rightarrow \text{Stockins (Purchased Supply)}$$

### Key Data Caveats (per `DATA_NOTES.md`)
1. **Pune Logging Disruption (7–13 Sep 2026):** An app release disrupted inspection completion logging. Inspections happened normally, and 122 cars were stocked in. The recorded inspection drop (233) is an unbackfilled data artifact, not an operational failure.
2. **Bengaluru Tracking Defect (Pre-3 Aug 2026):** ~15% of leads carried `channel = unknown`. On 3 August, the tracking fix reattributed these leads across standard channels, creating an artificial $+19.5\%$ jump in paid digital leads.
3. **Cohort Truncation Lag:** Leads convert up to 14 days after creation; ~70% of stockins occur in days 1–7. Week of 28 Sep is only ~70% mature; week of 5 Oct is $<30\%$ mature.
4. **Partial Calendar Week:** Week of 5 Oct 2026 contains only 4 operating days as of data cutoff (8 Oct 2026).
5. **Missing Dimensions:** The dataset contains **no marketing spend**, no campaign dates, no inspector headcount, and no buyer-side deliveries.

---

## 4. Setup & Installation

### Requirements
- Python 3.9+ (Tested on Python 3.13.5)
- Pandas & NumPy

```bash
pip install pandas numpy
```

---

## 5. How to Run the Analysis

### 1. Run Data Integrity Audit
```bash
python data_audit.py
```
Audits row dimensions, nulls, duplicate keys, sequential funnel integrity, date coverage, and hierarchical reconciliations.

### 2. Run the Full Diagnostic Engine (Pune A1)
```bash
python analysis_engine.py
```
Executes gates 1–5, calculates 8-week baseline, runs additive factor decomposition, tests disputed claims, and outputs results.

### 3. Generate the Final HTML Readout
```bash
python report_generator.py
```
Generates `readout_v2.html`, which opens in any web browser completely offline.

### 4. Run Automated Test Suite (Scenarios A1 to A5)
```bash
python test_all_runs.py
```
Executes all 5 test scenarios:
- **A1:** Pune Stockins Drop (pricing expectation gap vs ops/marketing claims).
- **A2:** Hyderabad Campaign Jump (identifies +2.18% as baseline noise; $Z = 1.06\sigma \le 2.0\sigma$).
- **A3:** Executive Pressure Test (resists false dichotomy; provides 1-line evidence verdict).
- **A4:** Out-of-Scope Metric (Gate 1 halts buyer-side delivery query).
- **A5:** Adversarial Test (exposes Bengaluru 3 Aug channel jump as a tracking reclassification).

---

## 6. How to Open the Reports

Open the generated HTML readouts directly in any browser (Chrome, Edge, Firefox, Safari):
- `readout_v2.html`: Final approved diagnostic readout.
- `readout_v1.html`: Initial skill iteration (with critique points).
- `readout_baseline.html`: Naive unassisted LLM output.

Zero internet connection or external libraries required.

---
*End of README.*
