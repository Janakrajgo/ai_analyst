# Spinny Applied AI Take-Home Assignment Submission

This folder contains the complete, official submission deliverables specified in **Section 6 ("What to send")** of `01_CANDIDATE_BRIEF.md`, along with the execution engine so evaluators can run and test everything out of the box.

---

## 1. Candidate Brief §6 Deliverables Mapping

| # | Item from Brief | File in This Folder | Description |
| :-: | :--- | :--- | :--- |
| **1** | `skill.md` | [`skill.md`](skill.md) | Reusable 2-page investigation skill answering *"Why did this metric move?"* across any city, metric, and period. |
| **2** | `readout_baseline.html` | [`readout_baseline.html`](readout_baseline.html) | Readout produced with **no skill** (the benchmark to beat). |
| **2** | `readout_v1.html` | [`readout_v1.html`](readout_v1.html) | Readout produced with **skill v1** unedited. |
| **2** | `readout_v2.html` | [`readout_v2.html`](readout_v2.html) | Final, perfected HTML readout complying with all §4 standards (30-sec verdict, denominators, waterfall, zero residual). |
| **3** | `critique.md` | [`critique.md`](critique.md) | 10 named defects identified on v1, and the complete audit of changes applied in v2. |
| **4** | `runs.md` | [`runs.md`](runs.md) | Detailed log and links for all evaluation runs: Baseline, A1 (v1 & v2), A2 (Hyderabad), A3 (Pressure test), A4 (Buyer deliveries refusal), and A5 (Bengaluru tracking bug). |
| **5** | `writeup.md` | [`writeup.md`](writeup.md) | 1-page executive reflection: value added over baseline, 3 core design decisions, what still fails, and audit strategy for 20 users. |
| **6** | `ai_log.md` | [`ai_log.md`](ai_log.md) | Working chat transcripts, prompt logs, 3 critical moments the AI was wrong/unhelpful, and how judgment overruled it. |
| **7** | Time Spent | Documented in `ai_log.md` & `writeup.md` | Transparent audit of time spent across planning, auditing, skill authoring, and refinement. |

---

## 2. How to Run and Verify the Submission

All source files are included directly in this folder. Zero external packages are needed (only standard library + pandas/numpy).

### A. Run Automated Assertions (All 5 Cases)
To verify all calculations, $Z$-scores, factor decompositions, and report isolation:
```bash
python test_all_runs.py
```
*Expected result:* All 6 test suites pass with 100% assertion integrity.

### B. Launch Live Interactive Web Server
To interactively ask business questions, view live iframe previews, and download reports:
```bash
python app.py
```
Then open your browser at **`http://127.0.0.1:8000`**.

### C. Open Standalone HTML Reports Offline
Double-click and open any of the following files directly in any web browser (zero CDN / zero internet required):
- `readout_v2.html` (Official A1 Pune stockin investigation)
- `readout_v1.html` (Skill v1 output)
- `readout_baseline.html` (Baseline unassisted output)
- `reports/readout_hyderabad.html` (Case A2 campaign investigation)
- `reports/readout_buyer_deliveries_refusal.html` (Case A4 Gate 1 refusal)
- `reports/readout_bengaluru_leads.html` (Case A5 agency bonus reclassification)

---

## 3. Companion Reference Files
- **`seller_funnel_weekly.csv`**: Official weekly seller funnel dataset (660 rows).
- **`DATA_NOTES.md`**: Official schema definitions, known logging glitches, and cohort maturity notes.

---

## 4. Live Repository
The complete project history, transcripts, and commit log are hosted at:  
👉 **https://github.com/Janakrajgo/ai_analyst**
