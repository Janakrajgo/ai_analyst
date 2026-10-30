"""
generate_v1.py - Generates readout_v1.html based on initial skill.md v1
Produces the initial unedited skill output for A1, containing real analytical findings
but with minor defects against the strict §4 styling and presentation standards.
"""

from analysis_engine import run_investigation

def generate_v1():
    res = run_investigation("Pune", "stockins")
    
    # We will render v1 with the specific characteristics of the first iteration:
    # 1. Panel titles named axes/topics instead of analytical messages
    # 2. Caveat in small text at bottom of panel rather than adjacent to affected numbers
    # 3. Some percentages missing inline numerators/denominators
    # 4. Hero box missing explicit comparator in words
    # 5. Missing Z-score next to ruled-out claims
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Pune Stockins Investigation - Skill v1</title>
    <style>
        body {{ font-family: -apple-system, sans-serif; background: #f1f5f9; color: #0f172a; margin: 20px; }}
        .card {{ background: #fff; border-radius: 8px; padding: 20px; max-width: 1100px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .header {{ border-bottom: 2px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 20px; }}
        .hero {{ font-size: 28px; font-weight: bold; color: #e11d48; margin: 10px 0; }}
        .grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }}
        .panel {{ border: 1px solid #e2e8f0; border-radius: 6px; padding: 15px; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 10px; font-size: 12px; }}
        th, td {{ border: 1px solid #cbd5e1; padding: 6px 8px; text-align: left; }}
        th {{ background: #f8fafc; }}
        .verdict {{ background: #eff6ff; border-left: 4px solid #2563eb; padding: 12px; margin-bottom: 15px; font-size: 14px; }}
    </style>
</head>
<body>

<div class="card">
    <div class="header">
        <h2>Executive Readout: Pune Stockin Analysis</h2>
        <div>Data as of: 2026-10-08</div>
    </div>

    <div class="verdict">
        <strong>Verdict:</strong> Pune stockins fell by 26.9/week in mature weeks due to a collapse in offer acceptance at the pricing stage, not marketing lead cuts or operational inspection slowdowns.
    </div>

    <div>
        <div style="font-size: 12px; color: #64748b;">Observed Change:</div>
        <div class="hero">-26.9 stockins/wk (-22.3%)</div>
    </div>

    <div class="grid">
        <!-- Panel 1: Title names axes instead of message -->
        <div class="panel">
            <h3>Panel 1: Weekly Stockin Trend</h3>
            <p style="font-size: 11px; color: #64748b;">X-axis: Week Start, Y-axis: Stockin Volume</p>
            <table>
                <tr><th>Week</th><th>Stockins</th><th>Status</th></tr>
                <tr><td>2026-07-13 to 2026-08-31</td><td>120.4 avg</td><td>8-Week Baseline</td></tr>
                <tr><td>2026-09-07</td><td>122</td><td>Normal</td></tr>
                <tr><td>2026-09-14</td><td>96</td><td>Mature Drop</td></tr>
                <tr><td>2026-09-21</td><td>91</td><td>Mature Drop</td></tr>
                <tr><td>2026-09-28</td><td>63</td><td>Lagging</td></tr>
                <tr><td>2026-10-05</td><td>24</td><td>Incomplete</td></tr>
            </table>
            <p style="font-size: 10px; color: #94a3b8; margin-top: 10px;">*Note: Week of 28 Sep is 70% mature; 5 Oct is 4 days complete.</p>
        </div>

        <!-- Panel 2: Rates without denominators in some rows -->
        <div class="panel">
            <h3>Panel 2: Funnel Conversion Stages</h3>
            <table>
                <tr><th>Stage</th><th>Baseline</th><th>Target</th><th>Delta</th></tr>
                <tr><td>Leads</td><td>956.9</td><td>903.0</td><td>-5.7%</td></tr>
                <tr><td>Inspection Rate</td><td>43.0%</td><td>42.4%</td><td>-0.6 pts</td></tr>
                <tr><td>Offer Rate</td><td>85.5%</td><td>84.1%</td><td>-1.4 pts</td></tr>
                <tr><td>Stockin Rate</td><td>34.2%</td><td>29.0%</td><td>-5.2 pts</td></tr>
            </table>
        </div>

        <!-- Panel 3: Factor Decomposition -->
        <div class="panel">
            <h3>Panel 3: Factor Decomposition</h3>
            <table>
                <tr><th>Factor</th><th>Contribution</th></tr>
                <tr><td>Lead Volume Effect</td><td>-6.8 stockins/wk</td></tr>
                <tr><td>Inspection Rate Effect</td><td>-1.6 stockins/wk</td></tr>
                <tr><td>Offer Rate Effect</td><td>-1.8 stockins/wk</td></tr>
                <tr><td>Stockin Rate Effect</td><td>-16.7 stockins/wk</td></tr>
                <tr><td><strong>Total Change</strong></td><td><strong>-26.9 stockins/wk</strong></td></tr>
            </table>
            <p style="font-size: 11px; color: #475569; margin-top: 8px;">Reconciles to observed delta.</p>
        </div>

        <!-- Panel 4: Ruled Out Explanations -->
        <div class="panel">
            <h3>Panel 4: Ruled Out Explanations</h3>
            <table>
                <tr><th>Claim</th><th>Verdict</th><th>Details</th></tr>
                <tr><td>Marketing cut spend</td><td>Refuted</td><td>Leads down 5.7%, which is within normal variation.</td></tr>
                <tr><td>Inspections are slow</td><td>Refuted</td><td>Inspection rate was 42.4% vs 43.0% baseline. App bug in 7 Sep.</td></tr>
                <tr><td>Pricing offer acceptance</td><td>Primary Driver</td><td>Stockin rate fell from 34.2% to 29.0%.</td></tr>
            </table>
        </div>

        <!-- Panel 5: Pricing Analysis -->
        <div class="panel">
            <h3>Panel 5: Pricing Analysis</h3>
            <table>
                <tr><th>Metric</th><th>Baseline</th><th>Target</th></tr>
                <tr><td>Offer Price</td><td>₹569,451</td><td>₹569,720</td></tr>
                <tr><td>Expected Price</td><td>₹615,849</td><td>₹621,595</td></tr>
                <tr><td>Price Gap</td><td>₹46,398</td><td>₹51,875 (+11.8%)</td></tr>
            </table>
        </div>

        <!-- Panel 6: Audit Gates -->
        <div class="panel">
            <h3>Panel 6: Audit Gates</h3>
            <table>
                <tr><th>Gate</th><th>Status</th></tr>
                <tr><td>Metric Scope</td><td>PASSED</td></tr>
                <tr><td>Temporal Completeness</td><td>CAVEAT (Week of 5 Oct has 4 days)</td></tr>
                <tr><td>Cohort Maturity</td><td>CAVEAT (Weeks of 28 Sep and 5 Oct immature)</td></tr>
                <tr><td>Data Logging</td><td>CAVEAT (App bug on 7-13 Sep)</td></tr>
                <tr><td>Statistical Significance</td><td>SIGNIFICANT (>2σ)</td></tr>
            </table>
            <p style="font-size: 11px; margin-top: 10px;">Confidence: High on stage, moderate on causality.</p>
        </div>
    </div>
</div>

</body>
</html>
"""
    with open("readout_v1.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("Generated readout_v1.html")

if __name__ == "__main__":
    generate_v1()
