"""
data_audit.py - Comprehensive Data Audit for Spinny Seller Funnel
Analyzes seller_funnel_weekly.csv against all business and data quality dimensions.
"""

import pandas as pd
import numpy as np
import json
import os

def run_audit(csv_path="seller_funnel_weekly.csv"):
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"File not found: {csv_path}")

    df = pd.read_csv(csv_path)
    
    audit_results = {}
    
    # 1. Dimensions and columns
    n_rows, n_cols = df.shape
    columns = list(df.columns)
    audit_results["shape"] = {"rows": n_rows, "cols": n_cols, "columns": columns}
    
    # 2. Data types & missing values
    dtypes = {col: str(df[col].dtype) for col in df.columns}
    missing_counts = {col: int(df[col].isna().sum()) for col in df.columns}
    audit_results["dtypes"] = dtypes
    audit_results["missing_values"] = missing_counts
    
    # 3. Duplicate records & duplicate dimension keys
    dim_keys = ["week_start", "city", "channel", "car_age_band"]
    exact_duplicates = int(df.duplicated().sum())
    key_duplicates = int(df.duplicated(subset=dim_keys).sum())
    
    # Let's inspect where duplicate keys happen if any
    dup_key_records = df[df.duplicated(subset=dim_keys, keep=False)]
    audit_results["duplicates"] = {
        "exact_duplicates": exact_duplicates,
        "key_duplicates": key_duplicates,
        "dup_slices_count": len(dup_key_records)
    }
    
    # 4. Negative or impossible counts
    metric_cols = ["leads", "inspections_done", "offers_made", "stockins", "avg_offer_price", "avg_expected_price"]
    negative_counts = {col: int((df[col] < 0).sum()) for col in metric_cols}
    audit_results["negative_counts"] = negative_counts
    
    # 5, 6, 7. Funnel integrity violations
    # Check inspections > leads
    insp_gt_leads = df[df["inspections_done"] > df["leads"]]
    # Check offers > inspections
    offers_gt_insp = df[df["offers_made"] > df["inspections_done"]]
    # Check stockins > offers
    stockins_gt_offers = df[df["stockins"] > df["offers_made"]]
    
    audit_results["funnel_violations"] = {
        "inspections_gt_leads": len(insp_gt_leads),
        "offers_gt_inspections": len(offers_gt_insp),
        "stockins_gt_offers": len(stockins_gt_offers),
        "offers_gt_insp_details": offers_gt_insp[["week_start", "city", "channel", "car_age_band", "inspections_done", "offers_made"]].to_dict(orient="records")
    }
    
    # 8. Weekly date coverage
    unique_weeks = sorted(df["week_start"].unique())
    audit_results["date_coverage"] = {
        "min_week": unique_weeks[0],
        "max_week": unique_weeks[-1],
        "total_weeks": len(unique_weeks),
        "weeks_list": unique_weeks
    }
    
    # 9. City, Channel, Car Age distributions
    city_dist = df.groupby("city")[metric_cols].sum().to_dict(orient="index")
    channel_dist = df.groupby("channel")[metric_cols].sum().to_dict(orient="index")
    age_dist = df.groupby("car_age_band")[metric_cols].sum().to_dict(orient="index")
    
    audit_results["distributions"] = {
        "by_city": city_dist,
        "by_channel": channel_dist,
        "by_car_age_band": age_dist
    }
    
    # 10. Weekly summary and partial week inspection
    weekly_summary = df.groupby("week_start").agg(
        leads=("leads", "sum"),
        inspections=("inspections_done", "sum"),
        offers=("offers_made", "sum"),
        stockins=("stockins", "sum"),
        row_count=("leads", "count")
    ).reset_index()
    
    weekly_summary["inspection_rate"] = weekly_summary["inspections"] / weekly_summary["leads"]
    weekly_summary["offer_rate"] = weekly_summary["offers"] / weekly_summary["inspections"]
    weekly_summary["stockin_rate"] = weekly_summary["stockins"] / weekly_summary["offers"]
    weekly_summary["lead_to_stockin_rate"] = weekly_summary["stockins"] / weekly_summary["leads"]
    
    audit_results["weekly_totals"] = weekly_summary.to_dict(orient="records")
    
    # 11. Pune specific weekly breakdown (to investigate A1 and known caveat)
    pune_df = df[df["city"] == "Pune"]
    pune_weekly = pune_df.groupby("week_start").agg(
        leads=("leads", "sum"),
        inspections=("inspections_done", "sum"),
        offers=("offers_made", "sum"),
        stockins=("stockins", "sum"),
        avg_offer=("avg_offer_price", "mean"),
        avg_expected=("avg_expected_price", "mean")
    ).reset_index()
    pune_weekly["inspection_rate"] = pune_weekly["inspections"] / pune_weekly["leads"]
    pune_weekly["offer_rate"] = pune_weekly["offers"] / pune_weekly["inspections"]
    pune_weekly["stockin_rate"] = pune_weekly["stockins"] / pune_weekly["offers"]
    pune_weekly["lead_to_stockin_rate"] = pune_weekly["stockins"] / pune_weekly["leads"]
    pune_weekly["price_gap"] = pune_weekly["avg_expected"] - pune_weekly["avg_offer"]
    pune_weekly["offer_to_expected_ratio"] = pune_weekly["avg_offer"] / pune_weekly["avg_expected"]
    
    audit_results["pune_weekly"] = pune_weekly.to_dict(orient="records")
    
    # 12. Bengaluru unknown channel analysis (to verify known caveat)
    bengaluru_unknown = df[(df["city"] == "Bengaluru") & (df["channel"] == "unknown")]
    audit_results["bengaluru_unknown"] = {
        "total_unknown_rows": len(bengaluru_unknown),
        "unknown_weeks": sorted(bengaluru_unknown["week_start"].unique()),
        "unknown_leads": int(bengaluru_unknown["leads"].sum()),
        "total_bengaluru_leads_pre_aug3": int(df[(df["city"] == "Bengaluru") & (df["week_start"] < "2026-08-03")]["leads"].sum()),
        "unknown_ratio_pre_aug3": float(bengaluru_unknown["leads"].sum() / df[(df["city"] == "Bengaluru") & (df["week_start"] < "2026-08-03")]["leads"].sum())
    }
    
    # 13. Reconciliations across levels
    total_leads_raw = int(df["leads"].sum())
    total_leads_city = sum(v["leads"] for v in city_dist.values())
    total_leads_channel = sum(v["leads"] for v in channel_dist.values())
    total_leads_weekly = sum(w["leads"] for w in audit_results["weekly_totals"])
    reconciled = (total_leads_raw == total_leads_city == total_leads_channel == total_leads_weekly)
    audit_results["reconciliation"] = {
        "raw_sum": total_leads_raw,
        "city_sum": total_leads_city,
        "channel_sum": total_leads_channel,
        "weekly_sum": total_leads_weekly,
        "perfectly_reconciled": reconciled
    }

    return audit_results, df

if __name__ == "__main__":
    results, df = run_audit()
    print("=== AUDIT SUMMARY ===")
    print(f"Rows: {results['shape']['rows']}, Columns: {results['shape']['cols']}")
    print(f"Missing Values: {results['missing_values']}")
    print(f"Key Duplicates: {results['duplicates']['key_duplicates']}")
    print(f"Negative counts: {results['negative_counts']}")
    print(f"Funnel Violations (offers > insp): {results['funnel_violations']['offers_gt_inspections']}")
    print(f"Bengaluru Unknown Ratio pre-Aug 3: {results['bengaluru_unknown']['unknown_ratio_pre_aug3']:.2%}")
    print(f"Reconciliation: {results['reconciliation']['perfectly_reconciled']}")
    print("\nWeekly Totals:")
    w_df = pd.DataFrame(results["weekly_totals"])
    print(w_df[["week_start", "leads", "inspections", "offers", "stockins", "inspection_rate", "offer_rate", "stockin_rate", "lead_to_stockin_rate"]])
    print("\nPune Weekly:")
    p_df = pd.DataFrame(results["pune_weekly"])
    print(p_df[["week_start", "leads", "inspections", "offers", "stockins", "inspection_rate", "offer_rate", "stockin_rate", "price_gap", "offer_to_expected_ratio"]])
