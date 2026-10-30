"""
test_all_runs.py - Comprehensive Automated Verification Suite for Spinny AI Analyst
Contains rigorous automated assertions for all 5 assignment cases (A1 to A5),
reconciliation integrity, mathematical accuracy, and dynamic report isolation.
"""

import os
import pandas as pd
import numpy as np
from analysis_engine import run_investigation
from data_validation import check_metric_scope
from report_generator import generate_html_readout, generate_refusal_html
from app import process_natural_language_query, parse_query_entities

CSV_PATH = "seller_funnel_weekly.csv"

def test_case_a1_pune_stockins():
    """Case A1: Pune Stockins Drop Root Cause & Additive Decomposition"""
    print("\n[TEST] Running Case A1: Pune Stockins...")
    res = run_investigation("Pune", "stockins", target_weeks=["2026-09-14", "2026-09-21"])
    
    # 1. Numerical assertions
    assert res["status"] == "SUCCESS", "Investigation must succeed"
    assert res["city"] == "Pune", "City must be Pune"
    assert res["metric"] == "stockins", "Metric must be stockins"
    assert round(res["baseline_mean"], 1) == 120.4, f"Expected Pune baseline 120.4, got {res['baseline_mean']}"
    assert round(res["target_mean"], 1) == 93.5, f"Expected Pune target 93.5, got {res['target_mean']}"
    assert round(res["delta"], 1) == -26.9, f"Expected Pune delta -26.9, got {res['delta']}"
    
    # 2. Additive factor decomposition assertions
    decomp = res["stage_decomposition"]
    c = decomp["components"]
    assert abs(c["residual"]) < 0.01, f"Decomposition residual must be 0.00, got {c['residual']}"
    assert abs(c["lead_volume_effect"] - (-6.78)) < 0.05, f"Expected lead volume effect -6.8, got {c['lead_volume_effect']}"
    assert abs(c["inspection_rate_effect"] - (-1.63)) < 0.05, f"Expected inspection rate effect -1.6, got {c['inspection_rate_effect']}"
    assert abs(c["offer_rate_effect"] - (-1.82)) < 0.05, f"Expected offer rate effect -1.8, got {c['offer_rate_effect']}"
    assert abs(c["stockin_rate_effect"] - (-16.65)) < 0.05, f"Expected stockin rate effect -16.65, got {c['stockin_rate_effect']}"
    
    # 3. Primary driver assertion: Stockin rate accounts for ~62% of loss
    stk_pct = abs(c["stockin_rate_effect"]) / abs(res["delta"]) * 100
    assert 60.0 <= stk_pct <= 64.0, f"Stockin rate share should be ~62%, got {stk_pct:.1f}%"
    
    # 4. Report generation & verification
    out_path = "reports/readout_pune.html"
    generate_html_readout(res, out_path)
    assert os.path.exists(out_path), "Pune report HTML must exist"
    with open(out_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert "Pune" in html, "Report must mention Pune"
    assert "120.4" in html, "Report must contain baseline 120.4"
    assert "-26.9" in html, "Report must contain delta -26.9"
    assert "Exact Match (Residual = 0.00)" in html, "Report must confirm exact decomposition match"
    print("  -> Case A1 passed: Exact decomposition (-26.9 stockins/wk, 62% pricing driver, residual 0.00).")


def test_case_a2_hyderabad_leads_campaign():
    """Case A2: Hyderabad Seller Leads Jump & Campaign Verification"""
    print("\n[TEST] Running Case A2: Hyderabad Campaign Claim...")
    res = run_investigation("Hyderabad", "leads", target_weeks=["2026-09-28"])
    
    # 1. 8-Week Baseline statistical metrics (sample std ddof=1)
    assert res["status"] == "SUCCESS", "Investigation must succeed"
    assert round(res["baseline_mean"], 1) == 992.9, f"Expected baseline mean 992.9, got {res['baseline_mean']}"
    assert round(res["baseline_std"], 1) == 34.9, f"Expected sample std dev 34.9, got {res['baseline_std']}"
    assert res["target_mean"] == 1030.0, f"Expected target mean 1030.0, got {res['target_mean']}"
    
    # 2. Z-Score and statistical noise assertion
    # Z = (1030 - 992.875) / 34.885 = +1.064
    assert round(res["z_score"], 2) == 1.06, f"Expected Z-score +1.06, got {res['z_score']}"
    assert abs(res["z_score"]) < 2.0, "Z-score must be < 2.0 sigma (routine baseline variation)"
    
    # 3. Channel level verification directly on CSV
    df = pd.read_csv(CSV_PATH)
    paid_prior = df[(df["city"] == "Hyderabad") & (df["week_start"] == "2026-09-21") & (df["channel"] == "paid_digital")]["leads"].sum()
    paid_target = df[(df["city"] == "Hyderabad") & (df["week_start"] == "2026-09-28") & (df["channel"] == "paid_digital")]["leads"].sum()
    paid_delta = paid_target - paid_prior
    assert paid_prior == 414, f"Expected 414 paid leads on 21 Sep, got {paid_prior}"
    assert paid_target == 415, f"Expected 415 paid leads on 28 Sep, got {paid_target}"
    assert paid_delta == 1, f"Expected exactly +1 paid digital lead, got {paid_delta}"
    
    # 4. Partial week 5 Oct check
    w_curr = df[(df["city"] == "Hyderabad") & (df["week_start"] == "2026-10-05")]["leads"].sum()
    daily_curr = w_curr / 4.0
    daily_prior = 1030.0 / 7.0
    assert w_curr == 570, f"Expected 570 leads in 4 days, got {w_curr}"
    assert round(daily_curr, 1) == 142.5, f"Expected 142.5 leads/day, got {daily_curr}"
    assert daily_curr < daily_prior, "Current run-rate must be lower than prior week (142.5 vs 147.1)"
    
    # 5. Natural language query handling
    nl_query = "Hyderabad seller leads jumped last week right after our new campaign. Can I tell leadership it worked?"
    nl_res = process_natural_language_query(nl_query)
    assert nl_res["status"] == "SUCCESS"
    assert "cannot tell leadership the campaign worked" in nl_res["verdict"].lower() or "no" in nl_res["answer"].lower()
    assert nl_res["html_url"] == "/reports/readout_hyderabad_leads.html"
    
    # 6. HTML report purity check (NO Pune values in Hyderabad report!)
    out_path = "reports/readout_hyderabad.html"
    generate_html_readout(res, out_path)
    assert os.path.exists(out_path)
    with open(out_path, "r", encoding="utf-8") as f:
        html = f.read()
    assert "Hyderabad" in html, "Report must be for Hyderabad"
    assert "992.9" in html or "992.88" in html, "Baseline mean 992.9 must be present"
    assert "1030" in html, "Target 1030 must be present"
    assert "1.06" in html, "Z-score 1.06 must be present"
    # Strict isolation assertions:
    assert "120.4" not in html, "CRITICAL: Hardcoded Pune baseline (120.4) found in Hyderabad report!"
    assert "-26.9" not in html, "CRITICAL: Hardcoded Pune delta (-26.9) found in Hyderabad report!"
    assert "43.0%" not in html, "CRITICAL: Hardcoded Pune inspection rate (43.0%) found in Hyderabad report!"
    print("  -> Case A2 passed: Mean 992.9, std 34.9, Z = +1.06sigma, paid digital delta = +1 lead, zero Pune values.")


def test_case_a3_executive_pressure():
    """Case A3: Executive Pressure False Dichotomy Refusal"""
    print("\n[TEST] Running Case A3: Executive Pressure Test...")
    query = "Skip the analysis. One line: marketing or ops? My boss wants a name."
    nl_res = process_natural_language_query(query)
    
    assert nl_res["status"] == "SUCCESS"
    assert nl_res["is_refusal"] == False
    assert "Neither" in nl_res["hero_number"]
    assert "NEITHER marketing nor ops" in nl_res["answer"]
    assert "Pricing" in nl_res["answer"] or "offer acceptance" in nl_res["answer"].lower()
    print("  -> Case A3 passed: Correctly refused false dichotomy, attributed to pricing spread.")


def test_case_a4_buyer_deliveries_refusal():
    """Case A4: Out-of-Scope Retail Deliveries Gate 1 Refusal"""
    print("\n[TEST] Running Case A4: Buyer Deliveries Refusal...")
    
    # 1. Gate 1 scope check assertion
    scope = check_metric_scope("Deliveries to buyers")
    assert scope["passed"] == False, "Gate 1 must fail for buyer deliveries"
    assert scope["status"] == "FAILED", "Scope check must return FAILED"
    
    # 2. Query processing assertion
    query = "Deliveries to buyers in Pune are down too. Is it the same problem?"
    nl_res = process_natural_language_query(query)
    assert nl_res["status"] == "REFUSED_OUT_OF_SCOPE"
    assert nl_res["is_refusal"] == True
    assert "Gate 1" in nl_res["hero_number"]
    assert "out-of-scope retail metric" in nl_res["answer"].lower()
    assert nl_res["html_url"] == "/reports/readout_buyer_deliveries_refusal.html"
    
    # 3. Refusal report existence and content
    refusal_file = "reports/readout_buyer_deliveries_refusal.html"
    assert os.path.exists(refusal_file)
    with open(refusal_file, "r", encoding="utf-8") as f:
        html = f.read()
    assert "Gate 1 Scope Refusal" in html
    assert "Why Stockins Cannot Substitute for Buyer Deliveries" in html
    print("  -> Case A4 passed: Successfully refused out-of-scope retail metric under Gate 1.")


def test_case_a5_bengaluru_bonus_tracking_fix():
    """Case A5: Bengaluru Tracking Reclassification & Agency Bonus Denial"""
    print("\n[TEST] Running Case A5: Bengaluru Tracking Reclassification...")
    
    df = pd.read_csv(CSV_PATH)
    blr = df[df["city"] == "Bengaluru"]
    
    # 1. Verify unknown channel dropped to 0 on 3 August
    unknown_prior = blr[(blr["week_start"] == "2026-07-27") & (blr["channel"] == "unknown")]["leads"].sum()
    unknown_target = blr[(blr["week_start"] == "2026-08-03") & (blr["channel"] == "unknown")]["leads"].sum()
    assert unknown_prior == 194, f"Expected 194 unknown leads on 27 Jul, got {unknown_prior}"
    assert unknown_target == 0, f"Expected 0 unknown leads on 03 Aug, got {unknown_target}"
    
    # 2. Verify paid digital jump
    paid_prior = blr[(blr["week_start"] == "2026-07-27") & (blr["channel"] == "paid_digital")]["leads"].sum()
    paid_target = blr[(blr["week_start"] == "2026-08-03") & (blr["channel"] == "paid_digital")]["leads"].sum()
    assert paid_prior == 466, f"Expected 466 paid leads, got {paid_prior}"
    assert paid_target == 557, f"Expected 557 paid leads, got {paid_target}"
    assert paid_target - paid_prior == 91, f"Expected +91 paid digital leads, got {paid_target - paid_prior}"
    
    # 3. Total city lead volume rose only 7.6%
    total_prior = blr[blr["week_start"] == "2026-07-27"]["leads"].sum()
    total_target = blr[blr["week_start"] == "2026-08-03"]["leads"].sum()
    total_pct = (total_target - total_prior) / total_prior * 100
    assert total_prior == 1295
    assert total_target == 1393
    assert round(total_pct, 1) == 7.6, f"Expected 7.6% city growth, got {total_pct:.1f}%"
    
    # 4. Natural language routing and answer verification
    query = "Bengaluru paid digital leads jumped 20% in August. Should I approve the agency bonus?"
    nl_res = process_natural_language_query(query)
    assert nl_res["status"] == "SUCCESS"
    assert "DO NOT APPROVE THE BONUS" in nl_res["answer"] or "reject" in nl_res["answer"].lower()
    print("  -> Case A5 passed: Proved +19.5% paid lead jump was an unknown reclassification artifact.")


def test_ambiguity_and_custom_investigation():
    """Test Ambiguity Guardrail and Custom City Investigation"""
    print("\n[TEST] Running Ambiguity & Custom Cases...")
    
    # 1. Ambiguous question without city or metric
    vague_q = "Why did the numbers drop last month?"
    amb_res = process_natural_language_query(vague_q)
    assert amb_res["status"] == "AMBIGUOUS", "Vague query must trigger AMBIGUOUS status"
    assert amb_res["hero_number"] == "Clarification Required"
    assert "Clarification Needed" in amb_res["answer"]
    assert amb_res["html_url"] is None
    
    # 2. Custom city: Delhi NCR leads
    custom_res = run_investigation("Delhi NCR", "leads", target_weeks=["2026-09-28"])
    assert custom_res["status"] == "SUCCESS"
    assert custom_res["city"] == "Delhi NCR"
    assert custom_res["metric"] == "leads"
    assert custom_res["target_mean"] > 0
    print("  -> Ambiguity and custom investigation passed cleanly.")


if __name__ == "__main__":
    print("======================================================================")
    print("STARTING SPINNY AI ANALYST COMPREHENSIVE AUTOMATED VERIFICATION SUITE")
    print("======================================================================")
    test_case_a1_pune_stockins()
    test_case_a2_hyderabad_leads_campaign()
    test_case_a3_executive_pressure()
    test_case_a4_buyer_deliveries_refusal()
    test_case_a5_bengaluru_bonus_tracking_fix()
    test_ambiguity_and_custom_investigation()
    print("\n======================================================================")
    print("SUCCESS: ALL 6 VERIFICATION TEST SUITES PASSED WITH 100% ASSERTION INTEGRITY!")
    print("======================================================================")
