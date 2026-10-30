"""
decomposition.py - Mathematical Funnel & Segment Decomposition
Performs exact additive reconciliation of metric movements into stage and segment drivers.
"""

import pandas as pd
import numpy as np

def decompose_funnel_stages(df, city, baseline_weeks, target_weeks):
    """
    Decomposes total change in Stockins into:
    1. Volume Effect (Leads change)
    2. Inspection Rate Effect (inspections / leads)
    3. Offer Rate Effect (offers / inspections)
    4. Stockin Rate Effect (stockins / offers)
    
    Formula: Stockins = Leads * r_insp * r_offer * r_stockin
    Uses exact sequential path decomposition so that sum of components + residual == total delta.
    """
    b_df = df[(df["city"] == city) & (df["week_start"].isin(baseline_weeks))] if city else df[df["week_start"].isin(baseline_weeks)]
    t_df = df[(df["city"] == city) & (df["week_start"].isin(target_weeks))] if city else df[df["week_start"].isin(target_weeks)]
    
    # Baseline average per week
    b_n_weeks = len(baseline_weeks)
    t_n_weeks = len(target_weeks)
    
    L0 = b_df["leads"].sum() / b_n_weeks
    I0 = b_df["inspections_done"].sum() / b_n_weeks
    O0 = b_df["offers_made"].sum() / b_n_weeks
    S0 = b_df["stockins"].sum() / b_n_weeks
    
    L1 = t_df["leads"].sum() / t_n_weeks
    I1 = t_df["inspections_done"].sum() / t_n_weeks
    O1 = t_df["offers_made"].sum() / t_n_weeks
    S1 = t_df["stockins"].sum() / t_n_weeks
    
    r_insp0 = I0 / L0 if L0 > 0 else 0
    r_offer0 = O0 / I0 if I0 > 0 else 0
    r_stock0 = S0 / O0 if O0 > 0 else 0
    
    r_insp1 = I1 / L1 if L1 > 0 else 0
    r_offer1 = O1 / I1 if I1 > 0 else 0
    r_stock1 = S1 / O1 if O1 > 0 else 0
    
    total_delta = S1 - S0
    
    # Exact step-wise multiplicative chain:
    # Term 1: Volume effect
    c_volume = (L1 - L0) * r_insp0 * r_offer0 * r_stock0
    
    # Term 2: Inspection rate effect
    c_insp = L1 * (r_insp1 - r_insp0) * r_offer0 * r_stock0
    
    # Term 3: Offer rate effect
    c_offer = L1 * r_insp1 * (r_offer1 - r_offer0) * r_stock0
    
    # Term 4: Stockin rate effect
    c_stock = L1 * r_insp1 * r_offer1 * (r_stock1 - r_stock0)
    
    sum_components = c_volume + c_insp + c_offer + c_stock
    residual = total_delta - sum_components
    
    reconciled = abs(residual) < 1e-6
    
    return {
        "metric": "stockins",
        "baseline_period": f"{len(baseline_weeks)} weeks ({baseline_weeks[0]} to {baseline_weeks[-1]})",
        "target_period": f"{len(target_weeks)} week(s) ({target_weeks[0]} to {target_weeks[-1]})",
        "baseline_weekly_avg": round(S0, 2),
        "target_weekly_avg": round(S1, 2),
        "total_delta": round(total_delta, 2),
        "components": {
            "lead_volume_effect": round(c_volume, 2),
            "inspection_rate_effect": round(c_insp, 2),
            "offer_rate_effect": round(c_offer, 2),
            "stockin_rate_effect": round(c_stock, 2),
            "residual": round(residual, 4)
        },
        "sum_of_components": round(sum_components, 2),
        "reconciled": reconciled,
        "rates": {
            "baseline": {
                "leads": round(L0, 1),
                "inspections": round(I0, 1),
                "offers": round(O0, 1),
                "stockins": round(S0, 1),
                "inspection_rate": round(r_insp0 * 100, 2),
                "offer_rate": round(r_offer0 * 100, 2),
                "stockin_rate": round(r_stock0 * 100, 2),
                "lead_to_stockin_rate": round((S0 / L0) * 100, 2)
            },
            "target": {
                "leads": round(L1, 1),
                "inspections": round(I1, 1),
                "offers": round(O1, 1),
                "stockins": round(S1, 1),
                "inspection_rate": round(r_insp1 * 100, 2),
                "offer_rate": round(r_offer1 * 100, 2),
                "stockin_rate": round(r_stock1 * 100, 2),
                "lead_to_stockin_rate": round((S1 / L1) * 100, 2)
            }
        }
    }

def decompose_by_segment(df, city, baseline_weeks, target_weeks, segment_col="channel", metric_col="stockins"):
    """
    Decomposes total change in metric by categorical segment (e.g., channel or car_age_band).
    Reconciles exact segment sum to aggregate delta.
    """
    b_df = df[(df["city"] == city) & (df["week_start"].isin(baseline_weeks))] if city else df[df["week_start"].isin(baseline_weeks)]
    t_df = df[(df["city"] == city) & (df["week_start"].isin(target_weeks))] if city else df[df["week_start"].isin(target_weeks)]
    
    b_n = len(baseline_weeks)
    t_n = len(target_weeks)
    
    b_seg = b_df.groupby(segment_col)[metric_col].sum() / b_n
    t_seg = t_df.groupby(segment_col)[metric_col].sum() / t_n
    
    all_segs = sorted(list(set(b_seg.index).union(set(t_seg.index))))
    
    segment_results = []
    total_delta = 0.0
    
    agg_delta = (t_df[metric_col].sum()/t_n - b_df[metric_col].sum()/b_n)
    
    for seg in all_segs:
        b_val = b_seg.get(seg, 0.0)
        t_val = t_seg.get(seg, 0.0)
        delta = t_val - b_val
        total_delta += delta
        pct_contrib = (delta / agg_delta) * 100 if agg_delta != 0 else 0
        segment_results.append({
            "segment": seg,
            "baseline_avg": round(b_val, 2),
            "target_avg": round(t_val, 2),
            "delta": round(delta, 2),
            "pct_of_total_delta": round(pct_contrib, 1)
        })
        
    return {
        "metric": metric_col,
        "segment_dimension": segment_col,
        "segments": segment_results,
        "sum_of_segment_deltas": round(total_delta, 2),
        "actual_aggregate_delta": round(agg_delta, 2),
        "reconciled": abs(total_delta - agg_delta) < 1e-4
    }
