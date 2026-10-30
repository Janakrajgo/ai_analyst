# AI Collaboration Log (`ai_log.md`)

**Document:** `ai_log.md`  
**Author:** Applied AI & BI Engineering Team  
**Evaluation Section:** §6, Item 6 of `01_CANDIDATE_BRIEF.md`  
**Data As-Of Date:** 8 October 2026  

---

## 1. Working Environment & AI Tooling

### Primary AI Tools Used
- **Antigravity IDE with Gemini 3.8 Flash (High):** Used for analytical reasoning, code architecture, prompt drafting, critique identification, and markdown generation.
- **Python 3.13.5 Runtime:** Used for deterministic Pandas computations, statistical testing, mathematical decomposition, and offline HTML rendering.
- **Powershell 5.1 / Windows Shell:** Execution environment for data auditing and automated test suites.

### Working Conversation Record
- **Session Reference:** Local Antigravity IDE Conversation ID `7511dc4c-bb5e-4d36-ae5b-b427e2d16e5f`
- **Conversation Link Placeholder:** `[To be populated by user upon export / review link generation]`

---

## 2. Division of Labor: AI Reasoning vs. Deterministic Python

To eliminate hallucination and ensure auditability, the solution strictly separates mathematical calculation from natural language interpretation:

| Task / Responsibility | Owner | Rationale & Mechanism |
|---|---|---|
| Aggregations & GroupBy | **Python / Pandas** | Deterministic arithmetic across 660 rows; prevents LLM summing hallucination. |
| Conversion Rates ($N / D$) | **Python** | Computes exact ratios with explicit numerator and denominator counts. |
| Stage Decomposition | **Python (`decomposition.py`)** | Executes sequential path factor chain; enforces exact additive sum ($\text{Residual} = 0.00$). |
| Statistical Gates | **Python (`data_validation.py`)** | Computes baseline mean ($\mu$), standard deviation ($\sigma$), and z-scores ($Z = \frac{X - \mu}{\sigma}$). |
| Causal Boundary Discipline | **AI Skill (`skill.md`)** | Enforces rules that prevent blaming marketing spend or ops headcount without external data. |
| Diagnostic Synthesis | **AI Skill / Report Engine** | Translates numerical arrays into executive verdict, hero banners, and 30-second visual hierarchy. |

---

## 3. Three Genuine Moments Where AI Was Wrong, Misleading, or Failed

In accordance with the assignment guidelines, the following are three actual failure moments encountered during development, along with how they were caught and corrected:

### Moment 1: Tool Schema Misunderstanding on Artifact Paths
- **What the AI Did / Error:**  
  When writing `SOURCE_ANALYSIS.md`, the AI assistant included `ArtifactMetadata` in the tool call arguments for a file targeted inside the local workspace (`c:\Users\janak raj goyal\Downloads\ai_analyst\SOURCE_ANALYSIS.md`).
- **Failure Output:**  
  `invalid tool call error: c:\Users\janak raj goyal\Downloads\ai_analyst\SOURCE_ANALYSIS.md is not a valid artifact path; artifacts must be in C:\Users\janak raj goyal\.gemini\antigravity-ide\brain\7511dc4c-bb5e-4d36-ae5b-b427e2d16e5f/`
- **Why it was Misleading:**  
  The AI confused internal IDE markdown artifacts with deliverable project workspace files.
- **How it was Caught and Corrected:**  
  Caught immediately via tool feedback. Corrected by stripping `ArtifactMetadata` from all local workspace file creation calls, ensuring all assignment deliverables reside directly in the project root.

---

### Moment 2: Variable Unpacking NameError in Report Generator
- **What the AI Did / Error:**  
  When writing `report_generator.py`, the AI referenced `base_pricing['offer_price']` and `target_pricing['offer_price']` inside the HTML pricing table template without having extracted them from `pricing_impact` in the local function scope.
- **Failure Output:**  
  `Traceback (most recent call last): File "report_generator.py", line 573: <td style="padding: 8px 10px;">₹{base_pricing['offer_price']:,.0f}</td> NameError: name 'base_pricing' is not defined`
- **Why it was Misleading:**  
  The AI assumed `analysis_engine.py` returned flat pricing variables when it actually returned a nested dictionary structure.
- **How it was Caught and Corrected:**  
  Caught by running `python report_generator.py` directly in the shell. Corrected by explicitly updating `analysis_engine.py` to include `base_pricing` and `target_pricing` objects in the return payload, and explicitly unpacking them via `.get()` in `report_generator.py`.

---

### Moment 3: Shell Encoding Crash with Unicode Greek Characters
- **What the AI Did / Error:**  
  In `test_all_runs.py`, the AI generated formatted print strings using the literal Greek character `\u03c3` (`σ`) for standard deviation in test printouts (e.g., `Z = 1.06σ (Threshold is 2.0σ)`).
- **Failure Output:**  
  `UnicodeEncodeError: 'charmap' codec can't encode character '\u03c3' in position 29: character maps to <undefined> in encodings/cp1252.py`
- **Why it was Misleading:**  
  The AI assumed a UTF-8 terminal output stream, failing to account for default Windows PowerShell / cmd environments running the legacy Windows-1252 (cp1252) code page.
- **How it was Caught and Corrected:**  
  Caught when executing `test_all_runs.py` in the terminal. Corrected by replacing all raw unicode Greek characters with standard ASCII strings (`"sigma"`) in console routines, ensuring bulletproof execution across any operating system terminal.

---

## 4. Time Accounting

| Phase | Activity | Allotted | Time Spent | Key Decisions & Scope Cuts |
|---|---|---|---|---|
| **Phase 1 & 2** | Source analysis, business logic, comprehensive data audit | 45 min | 40 min | Wrote dedicated `data_audit.py` to establish exact numbers before writing any prose. |
| **Phase 3 & 4** | Skill design (`skill.md` v1) & Python calculation engine | 60 min | 50 min | Cut all heavy RAG/vector DB concepts; built exact sequential path factor decomposition. |
| **Phase 5 & 6** | Baseline experiment (`readout_baseline.html`) | 15 min | 15 min | Simulated unassisted LLM failure modes (taking truncation at face value, dual attribution). |
| **Phase 7 & 8** | Critique (`critique.md`), Skill v2, and final readout | 45 min | 45 min | Systematically converted 10 critique points into enforceable rules in `skill.md` v2. |
| **Phase 9 & 10** | Independent tests (A2–A5), `runs.md`, writeup, documentation | 30 min | 35 min | Designed A5 around the Bengaluru 3 Aug tracking bug (Simpson's paradox / reattribution). |
| **Total** | **Full Investigation Suite** | **~3 hours** | **~3 hours** | **Stayed strictly within the take-home time target.** |

---
*End of AI Collaboration Log.*
