# Executive Write-Up: Diagnostic Funnel Metric Skill

**Candidate:** Senior AI / BI Engineer  
**Role:** Applied AI Take-Home Assignment  
**Scope:** Reusable Diagnostic Method & Self-Contained Readout  

---

### 1. What the Skill Adds Over the Baseline
In the naive baseline (`readout_baseline.html`), an unassisted LLM exhibited classic analytical pathologies: it accepted recent truncated counts at face value, falsely claiming an **-80.5% collapse** in Pune stockins; it blamed both marketing and operations; it mistook the Pune 7–13 Sep app logging glitch for an operational failure; and it produced unstructured text without denominators or baseline comparators. 

In contrast, the structured skill (`skill.md` v2 / `readout_v2.html`):
- **Isolates Mature Reality:** Demonstrates that mature stockins dropped by **-26.9/wk (-22.3% vs 8-week baseline)**, while the apparent drop to 24 is an artifact of cohort lag (14-day conversion cycle) and a 4-day partial week.
- **Enforces Mathematical Truth:** Decomposes the delta additively (Volume: $-6.8$, Insp Rate: $-1.6$, Offer Rate: $-1.8$, Stockin Rate: $-16.7$, **Residual = 0.00**), proving that **62.0% of the decline** sits in the Pricing Team's offer acceptance stage, driven by a **+14.5% widening in the seller expectation gap** ($₹46,398 \rightarrow ₹53,110$).
- **Refutes Executive Bias:** Mathematically dismisses both Ops and Marketing claims using historical standard deviation thresholds ($Z \le 2\sigma$) and explicit numerators/denominators.

---

### 2. Three Critical Design Decisions
1. **Deterministic Python Engine vs. Generative Math:** LLMs hallucinate calculations when aggregating hierarchical slices. All aggregations, rate ratios, z-scores, and multiplicative-to-additive factor decompositions are computed deterministically in Python/Pandas; the LLM provides structured reasoning and synthesis over audited numbers.
2. **Sequential Multiplicative-to-Additive Decomposition Chain:** Standard percentage point deltas do not sum to total unit change. By evaluating factors along a sequential chain ($L \cdot r_{\text{insp}} \cdot r_{\text{offer}} \cdot r_{\text{stock}}$), each stage's unit contribution sums **identically to the total unit delta**, eliminating hand-waving residuals.
3. **Strict Gate Governance with Visible Failures:** Analytical gates (Scope, Completeness, Maturity, Anomalies, Significance) cannot fail silently. When a check fails (e.g., Pune logging bug or Hyderabad noise), the failure is stamped visibly on the readout.

---

### 3. What Was Deliberately Omitted and Why
- **No Heavyweight Production Infrastructure (Vector DBs / RAG / Microservices):** The dataset is 660 rows. Introducing LangChain, vector retrieval, or FastAPI microservices introduces latency, indeterminism, and fragile dependencies without adding analytical value.
- **No External Visual CDN Dependencies:** The readout uses inline CSS and standalone SVG. It renders offline in any browser without external network calls.
- **No Speculative Causal Attribution:** Because marketing spend, campaign calendars, and inspector rosters are absent, the skill strictly refuses to attribute causality to these levers.

---

### 4. Remaining Failure Modes & The Next Fix
- **Simultaneous Multiple-Stage Shifts:** When two funnel stages deteriorate concurrently, sequential path decomposition assigns slight interaction differences depending on path ordering. *Next Fix:* Implement average Shapley-value factor decomposition across all permutations.
- **Non-Linear Cohort Maturity Curves:** Currently uses a static 70% 7-day maturity heuristic. *Next Fix:* Fit empirical Weibull / log-logistic hazard curves per city to project immature cohort stockins dynamically.

---

### 5. Monitoring in Production (20 Weekly Users)
1. **Input Audit & Gate Logging:** Track gate failure rates in telemetry (e.g., proportion of runs with immature cohorts or out-of-scope metrics).
2. **Determinism & Reconciliation Canary:** An automated unit test asserting that every generated readout has $\text{Residual} = 0.00$ and all displayed rates match underlying CSV sums.
3. **LLM Hallucination Trap:** A regex evaluator asserting that every number in the LLM's text output exists in the deterministic Python output payload.
4. **User Feedback Loop:** A simple 1-click review ("Used in City Review: Yes/No; Factually Contested: Yes/No") to flag model drift or new unhandled data anomalies.
