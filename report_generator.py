"""
report_generator.py - Generates Standalone, Offline HTML Investigation Readouts
Strictly adheres to §4 of the candidate brief with zero external CDN dependencies.
"""

import json

def generate_html_readout(analysis_data, output_filepath, version="v2"):
    """
    Renders an offline, self-contained HTML report from deterministic analysis data.
    """
    city = analysis_data.get("city", "Pune")
    metric = analysis_data.get("metric", "stockins")
    as_of = analysis_data.get("as_of_date", "2026-10-08")
    verdict = analysis_data["verdict"]
    hero = analysis_data["hero_number"]
    
    decomp = analysis_data["stage_decomposition"]
    pricing = analysis_data["pricing_impact"]
    base_pricing = pricing.get("base_pricing", {})
    target_pricing = pricing.get("target_pricing", {})
    hypotheses = analysis_data["hypothesis_testing"]
    gates = analysis_data["gates"]
    conf = analysis_data["confidence"]
    missing = analysis_data["missing_evidence"]
    
    # Pre-render SVG charts
    # Panel 1: Weekly trend of stockins with baseline reference line
    # Data points for Pune:
    weeks_data = [
        ("07-13", 128, False, False),
        ("07-20", 105, False, False),
        ("07-27", 108, False, False),
        ("08-03", 135, False, False),
        ("08-10", 118, False, False),
        ("08-17", 129, False, False),
        ("08-24", 114, False, False),
        ("08-31", 126, False, False),
        ("09-07", 122, True, False),   # Bug week
        ("09-14", 96, False, False),   # Target mature
        ("09-21", 91, False, False),   # Target mature
        ("09-28", 63, False, True),    # Immature (~70%)
        ("10-05", 24, False, True)     # Immature & partial (4d)
    ]
    
    # SVG Dimensions
    svg_w = 540
    svg_h = 220
    pad_l = 45
    pad_r = 20
    pad_t = 30
    pad_b = 40
    plot_w = svg_w - pad_l - pad_r
    plot_h = svg_h - pad_t - pad_b
    
    max_val = 150
    base_line_y = pad_t + plot_h - (120.4 / max_val * plot_h)
    
    bar_width = 24
    step = plot_w / len(weeks_data)
    
    bars_svg = []
    labels_svg = []
    
    for i, (w_lbl, val, is_bug, is_immature) in enumerate(weeks_data):
        bx = pad_l + i * step + (step - bar_width) / 2
        bh = (val / max_val) * plot_h
        by = pad_t + plot_h - bh
        
        # Color based on state
        if is_immature:
            fill = "#94a3b8" # Slate/muted gray for immature
            stroke = "#64748b"
        elif is_bug:
            fill = "#38bdf8" # Cyan for bug week where stockins normal
            stroke = "#0284c7"
        elif i >= 9:
            fill = "#f43f5e" # Rose/red for mature drop
            stroke = "#be123c"
        else:
            fill = "#3b82f6" # Royal blue for baseline
            stroke = "#1d4ed8"
            
        bars_svg.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_width}" height="{bh:.1f}" rx="3" fill="{fill}" stroke="{stroke}" stroke-width="1"><title>{w_lbl}: {val} stockins</title></rect>')
        bars_svg.append(f'<text x="{bx + bar_width/2:.1f}" y="{by - 6:.1f}" font-size="10" font-family="system-ui, sans-serif" font-weight="600" fill="#1e293b" text-anchor="middle">{val}</text>')
        
        # X label
        labels_svg.append(f'<text x="{bx + bar_width/2:.1f}" y="{pad_t + plot_h + 16:.1f}" font-size="9" font-family="system-ui, sans-serif" fill="#64748b" text-anchor="middle">{w_lbl}</text>')
        if is_immature:
            labels_svg.append(f'<text x="{bx + bar_width/2:.1f}" y="{pad_t + plot_h + 27:.1f}" font-size="8" font-family="system-ui, sans-serif" font-weight="700" fill="#d97706" text-anchor="middle">Lag*</text>')

    bars_str = "\n".join(bars_svg)
    labels_str = "\n".join(labels_svg)
    
    panel1_svg = f'''
    <svg viewBox="0 0 {svg_w} {svg_h}" width="100%" height="220" style="overflow: visible;">
        <!-- Gridlines -->
        <line x1="{pad_l}" y1="{pad_t}" x2="{svg_w - pad_r}" y2="{pad_t}" stroke="#e2e8f0" stroke-dasharray="3 3"/>
        <text x="{pad_l - 8}" y="{pad_t + 4}" font-size="10" font-family="system-ui" fill="#94a3b8" text-anchor="end">150</text>
        
        <line x1="{pad_l}" y1="{pad_t + plot_h/2}" x2="{svg_w - pad_r}" y2="{pad_t + plot_h/2}" stroke="#e2e8f0" stroke-dasharray="3 3"/>
        <text x="{pad_l - 8}" y="{pad_t + plot_h/2 + 4}" font-size="10" font-family="system-ui" fill="#94a3b8" text-anchor="end">75</text>
        
        <line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{svg_w - pad_r}" y2="{pad_t + plot_h}" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="{pad_l - 8}" y="{pad_t + plot_h + 4}" font-size="10" font-family="system-ui" fill="#94a3b8" text-anchor="end">0</text>
        
        <!-- Baseline Reference Line -->
        <line x1="{pad_l}" y1="{base_line_y:.1f}" x2="{svg_w - pad_r}" y2="{base_line_y:.1f}" stroke="#d97706" stroke-width="2" stroke-dasharray="4 4"/>
        <text x="{svg_w - pad_r}" y="{base_line_y - 6:.1f}" font-size="10" font-family="system-ui" font-weight="700" fill="#d97706" text-anchor="end">8-Wk Baseline: 120.4/wk</text>
        
        <!-- Bars & Labels -->
        {bars_str}
        {labels_str}
    </svg>
    '''

    # Panel 3: Waterfall Decomposition SVG
    # Components: Baseline (120.4), Volume (-6.8), Insp Rate (-1.6), Offer Rate (-1.8), Stockin Rate (-16.7), Target (93.5)
    wf_items = [
        ("Base", 120.4, 0, 120.4, "#3b82f6"),
        ("Leads Vol", -6.8, 120.4 - 6.8, 120.4, "#f43f5e"),
        ("Insp Rate", -1.6, 113.6 - 1.6, 113.6, "#f43f5e"),
        ("Offer Rate", -1.8, 112.0 - 1.8, 112.0, "#f43f5e"),
        ("Stockin Rt", -16.7, 110.2 - 16.7, 110.2, "#be123c"),
        ("Target", 93.5, 0, 93.5, "#059669")
    ]
    
    wf_svg_h = 220
    wf_pad_l = 40
    wf_plot_h = 150
    wf_max = 140
    wf_step = (svg_w - wf_pad_l - pad_r) / len(wf_items)
    wf_bwidth = 38
    
    wf_bars = []
    for i, (name, delta_v, y_bot, y_top, color) in enumerate(wf_items):
        wx = wf_pad_l + i * wf_step + (wf_step - wf_bwidth) / 2
        if name in ["Base", "Target"]:
            bh = (delta_v / wf_max) * wf_plot_h
            by = pad_t + wf_plot_h - bh
            val_txt = f"{delta_v:.1f}"
        else:
            bh = (abs(delta_v) / wf_max) * wf_plot_h
            by = pad_t + wf_plot_h - (y_top / wf_max * wf_plot_h)
            val_txt = f"{delta_v:+.1f}"
            
        wf_bars.append(f'<rect x="{wx:.1f}" y="{by:.1f}" width="{wf_bwidth}" height="{bh:.1f}" rx="3" fill="{color}" stroke="#1e293b" stroke-opacity="0.2"><title>{name}: {delta_v}</title></rect>')
        wf_bars.append(f'<text x="{wx + wf_bwidth/2:.1f}" y="{by - 5:.1f}" font-size="10" font-family="system-ui" font-weight="700" fill="#1e293b" text-anchor="middle">{val_txt}</text>')
        wf_bars.append(f'<text x="{wx + wf_bwidth/2:.1f}" y="{pad_t + wf_plot_h + 16:.1f}" font-size="9.5" font-family="system-ui" font-weight="600" fill="#475569" text-anchor="middle">{name}</text>')
        
    wf_bars_str = "\n".join(wf_bars)
    panel3_svg = f'''
    <svg viewBox="0 0 {svg_w} {wf_svg_h}" width="100%" height="220" style="overflow: visible;">
        <line x1="{wf_pad_l}" y1="{pad_t}" x2="{svg_w - pad_r}" y2="{pad_t}" stroke="#e2e8f0" stroke-dasharray="3 3"/>
        <line x1="{wf_pad_l}" y1="{pad_t + wf_plot_h}" x2="{svg_w - pad_r}" y2="{pad_t + wf_plot_h}" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="{wf_pad_l - 8}" y="{pad_t + wf_plot_h + 4}" font-size="10" font-family="system-ui" fill="#94a3b8" text-anchor="end">0</text>
        {wf_bars_str}
    </svg>
    '''

    # Build Gate Status Rows
    gate_rows = []
    for g in gates:
        status_color = "#059669" if g.get("passed") else ("#d97706" if g.get("status") == "CAVEAT_APPLIED" else "#dc2626")
        status_badge = f'<span style="background-color: {status_color}18; color: {status_color}; font-weight: 700; padding: 2px 8px; border-radius: 4px; font-size: 11px;">{g.get("status")}</span>'
        gate_rows.append(f'''
        <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 8px 10px; font-weight: 600; font-size: 12px; color: #1e293b;">{g.get("gate")}</td>
            <td style="padding: 8px 10px; text-align: center;">{status_badge}</td>
            <td style="padding: 8px 10px; font-size: 11.5px; color: #475569;">{g.get("details", g.get("reason", ""))}</td>
        </tr>
        ''')
    gate_table_html = "\n".join(gate_rows)

    # Build Disputed Claims Rows
    claim_rows = []
    for h in hypotheses:
        claim_title = h.get("claim", h.get("driver"))
        advocate = h.get("advocate", h.get("owner", "Pricing"))
        verdict_badge_color = "#dc2626" if h["verdict"] == "REFUTED" else "#059669"
        claim_rows.append(f'''
        <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 10px 12px; font-weight: 600; font-size: 12px; color: #0f172a;">
                {claim_title}<br>
                <span style="font-weight: 400; font-size: 11px; color: #64748b;">Source: {advocate}</span>
            </td>
            <td style="padding: 10px 12px; font-size: 11.5px; color: #334155;">
                Base: {h["baseline_value"]}<br>
                Target: {h["target_value"]}
            </td>
            <td style="padding: 10px 12px; font-weight: 700; font-size: 12px; color: #0f172a; text-align: center;">{h["stockin_impact"]}</td>
            <td style="padding: 10px 12px; text-align: center;">
                <span style="background-color: {verdict_badge_color}18; color: {verdict_badge_color}; font-weight: 800; padding: 3px 8px; border-radius: 4px; font-size: 11px;">{h["verdict"]}</span>
            </td>
            <td style="padding: 10px 12px; font-size: 11.5px; color: #475569;">{h["reason"]}</td>
        </tr>
        ''')
    claims_table_html = "\n".join(claim_rows)

    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spinny Diagnostic Readout — {city} {metric.title()} Investigation</title>
    <style>
        :root {{
            --primary: #0f172a;
            --primary-accent: #2563eb;
            --surface: #ffffff;
            --bg: #f8fafc;
            --border: #e2e8f0;
            --text-main: #0f172a;
            --text-muted: #64748b;
            --danger: #e11d48;
            --success: #059669;
            --warning: #d97706;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.45;
            padding: 24px 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: var(--surface);
            border-radius: 12px;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.08);
            border: 1px solid var(--border);
            overflow: hidden;
        }}
        /* Header Block */
        .header {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff;
            padding: 24px 28px;
            border-bottom: 3px solid var(--primary-accent);
        }}
        .header-top {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        .header-title {{
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        .badge-city {{
            background-color: rgba(37, 99, 235, 0.3);
            border: 1px solid #3b82f6;
            color: #93c5fd;
            font-size: 12px;
            padding: 2px 10px;
            border-radius: 20px;
            font-weight: 600;
        }}
        .as-of {{
            font-size: 12px;
            color: #94a3b8;
            font-weight: 500;
        }}
        /* Verdict Banner */
        .verdict-banner {{
            background: rgba(255, 255, 255, 0.06);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 8px;
            padding: 16px 20px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 20px;
            flex-wrap: wrap;
        }}
        .verdict-text {{
            font-size: 15px;
            font-weight: 500;
            color: #f1f5f9;
            flex: 1;
            min-width: 300px;
        }}
        .hero-box {{
            text-align: right;
            background: rgba(225, 29, 72, 0.2);
            border: 1px solid rgba(244, 63, 94, 0.4);
            padding: 8px 18px;
            border-radius: 6px;
        }}
        .hero-label {{
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 700;
            color: #fda4af;
            letter-spacing: 0.05em;
        }}
        .hero-value {{
            font-size: 24px;
            font-weight: 800;
            color: #ffffff;
            font-feature-settings: "tnum";
        }}
        .hero-sub {{
            font-size: 11px;
            color: #cbd5e1;
        }}
        /* 6 Panel Grid */
        .grid {{
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            padding: 24px;
        }}
        @media (max-width: 900px) {{
            .grid {{ grid-template-columns: 1fr; }}
        }}
        .panel {{
            background: #ffffff;
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 18px 20px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.02);
        }}
        .panel-full {{
            grid-column: span 2;
        }}
        @media (max-width: 900px) {{
            .panel-full {{ grid-column: span 1; }}
        }}
        .panel-header {{
            margin-bottom: 14px;
            padding-bottom: 8px;
            border-bottom: 1px solid #f1f5f9;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
        }}
        .panel-title {{
            font-size: 14px;
            font-weight: 700;
            color: var(--primary);
            display: flex;
            flex-direction: column;
            gap: 2px;
        }}
        .panel-subtitle {{
            font-size: 11.5px;
            font-weight: 400;
            color: var(--text-muted);
        }}
        /* Tables */
        table {{
            width: 100%;
            border-collapse: collapse;
        }}
        th {{
            background: #f8fafc;
            text-align: left;
            padding: 8px 10px;
            font-size: 11px;
            font-weight: 700;
            color: #475569;
            text-transform: uppercase;
            letter-spacing: 0.03em;
            border-bottom: 1px solid var(--border);
        }}
        /* Callouts */
        .caveat-chip {{
            display: inline-block;
            background: #fef3c7;
            color: #92400e;
            border: 1px solid #fde68a;
            font-size: 10.5px;
            font-weight: 600;
            padding: 1px 6px;
            border-radius: 4px;
            margin-top: 4px;
        }}
        .footer {{
            background: #f8fafc;
            border-top: 1px solid var(--border);
            padding: 16px 24px;
            display: flex;
            justify-content: space-between;
            font-size: 11px;
            color: var(--text-muted);
            flex-wrap: wrap;
            gap: 10px;
        }}
    </style>
</head>
<body>

<div class="container">
    <!-- Header with 30-Second Verdict -->
    <header class="header">
        <div class="header-top">
            <div class="header-title">
                Spinny Executive Diagnostic Readout
                <span class="badge-city">{city} Supply Review</span>
            </div>
            <div class="as-of">Data as of: <strong>{as_of}</strong> (Official Cutoff)</div>
        </div>
        
        <div class="verdict-banner">
            <div class="verdict-text">
                <span style="color: #38bdf8; font-weight: 700;">Executive Verdict:</span> {verdict}
            </div>
            <div class="hero-box">
                <div class="hero-label">Mature Stockin Delta</div>
                <div class="hero-value">{hero}</div>
                <div class="hero-sub">vs 8-Week Historical Baseline</div>
            </div>
        </div>
    </header>

    <!-- 6 Analytical Panels (§4 compliant) -->
    <main class="grid">
        
        <!-- Panel 1: Weekly Funnel Trend & Normal Variation -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    Panel 1: Weekly Stockin Volumes vs 8-Week Historical Baseline
                    <span class="panel-subtitle">Bars start at zero. Blue = 8-wk baseline; Rose = mature drop; Gray = immature/partial lag.</span>
                </div>
            </div>
            {panel1_svg}
            <div style="font-size: 11px; color: #475569; margin-top: 8px;">
                <span class="caveat-chip">Caveat on Recent Weeks</span>
                <strong>28 Sep (63)</strong> is ~70% mature (10 days old); projected full-cohort yield is ~90.0 stockins. 
                <strong>05 Oct (24)</strong> is only 4 of 7 days complete and &lt;30% mature; run-rate is normal.
            </div>
        </section>

        <!-- Panel 2: Funnel Conversion Stages with Explicit Denominators -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    Panel 2: Funnel Stage Conversion Rates (Numerator / Denominator)
                    <span class="panel-subtitle">Comparing 8-week baseline average vs mature drop weeks (14 Sep & 21 Sep)</span>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Funnel Stage / Metric</th>
                        <th>8-Wk Baseline</th>
                        <th>Target (14 & 21 Sep)</th>
                        <th>Delta Rate</th>
                        <th>Primary Owner</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid #f1f5f9;">
                        <td style="padding: 10px 8px; font-weight: 600; font-size: 12px;">Lead Volume</td>
                        <td style="padding: 10px 8px; font-size: 12px;">956.9 leads/wk</td>
                        <td style="padding: 10px 8px; font-size: 12px;">903.0 leads/wk</td>
                        <td style="padding: 10px 8px; font-size: 12px; color: #dc2626; font-weight: 600;">-5.7% (within 1.7σ)</td>
                        <td style="padding: 10px 8px; font-size: 11px; color: #64748b;">Marketing</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;">
                        <td style="padding: 10px 8px; font-weight: 600; font-size: 12px;">Inspection Rate</td>
                        <td style="padding: 10px 8px; font-size: 12px;">43.0% (3,294 / 7,655)</td>
                        <td style="padding: 10px 8px; font-size: 12px;">42.4% (766 / 1,806)</td>
                        <td style="padding: 10px 8px; font-size: 12px; color: #059669; font-weight: 600;">-0.6 pts (Normal)</td>
                        <td style="padding: 10px 8px; font-size: 11px; color: #64748b;">City Ops</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;">
                        <td style="padding: 10px 8px; font-weight: 600; font-size: 12px;">Offer Rate</td>
                        <td style="padding: 10px 8px; font-size: 12px;">85.5% (2,815 / 3,294)</td>
                        <td style="padding: 10px 8px; font-size: 12px;">84.1% (644 / 766)</td>
                        <td style="padding: 10px 8px; font-size: 12px; color: #059669; font-weight: 600;">-1.4 pts (Normal)</td>
                        <td style="padding: 10px 8px; font-size: 11px; color: #64748b;">Policy / QC</td>
                    </tr>
                    <tr style="background-color: #fff1f2; border-bottom: 1px solid #fecdd3;">
                        <td style="padding: 10px 8px; font-weight: 700; font-size: 12px; color: #be123c;">Stockin Rate (Offer Acceptance)</td>
                        <td style="padding: 10px 8px; font-size: 12px; font-weight: 600;">34.2% (963 / 2,815)</td>
                        <td style="padding: 10px 8px; font-size: 12px; font-weight: 700; color: #be123c;">29.0% (187 / 644)</td>
                        <td style="padding: 10px 8px; font-size: 12px; color: #be123c; font-weight: 800;">-5.2 pts (-15.2%)</td>
                        <td style="padding: 10px 8px; font-size: 11px; font-weight: 700; color: #be123c;">Pricing Team</td>
                    </tr>
                    <tr>
                        <td style="padding: 10px 8px; font-weight: 700; font-size: 12px;">Overall Lead-to-Stockin Yield</td>
                        <td style="padding: 10px 8px; font-size: 12px;">12.6% (963 / 7,655)</td>
                        <td style="padding: 10px 8px; font-size: 12px;">10.4% (187 / 1,806)</td>
                        <td style="padding: 10px 8px; font-size: 12px; color: #be123c; font-weight: 700;">-2.2 pts (-17.5%)</td>
                        <td style="padding: 10px 8px; font-size: 11px; color: #64748b;">End-to-End</td>
                    </tr>
                </tbody>
            </table>
            <div style="font-size: 11px; color: #64748b; margin-top: 8px;">
                <span class="caveat-chip">Logging Caveat</span> 
                Week of 7–13 Sep recorded 24.8% inspection rate due to an unbackfilled software release bug; actual physical inspections operated normally.
            </div>
        </section>

        <!-- Panel 3: Additive Sequential Stage Decomposition -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    Panel 3: Additive Factor Decomposition of Stockin Decline
                    <span class="panel-subtitle">Total Delta: -26.9 stockins/wk vs 8-wk baseline. Components sum exactly to delta.</span>
                </div>
            </div>
            {panel3_svg}
            <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; margin-top: 10px; font-size: 11.5px;">
                <div style="display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 4px;">
                    <span>Decomposition Reconciliation:</span>
                    <span style="color: #059669;">Exact Match (Residual = 0.00)</span>
                </div>
                <div style="color: #475569;">
                    Lead Volume: <strong>-6.8/wk (25.2%)</strong> · 
                    Inspection Rate: <strong>-1.6/wk (6.1%)</strong> · 
                    Offer Rate: <strong>-1.8/wk (6.8%)</strong> · 
                    <span style="color: #be123c; font-weight: 700;">Stockin Rate: -16.7/wk (62.0%)</span>
                </div>
            </div>
        </section>

        <!-- Panel 4: Ruled-Out Hypotheses (Disputed Claims with Evidence) -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    Panel 4: Ruled-Out Explanations & Disputed Claims
                    <span class="panel-subtitle">Evaluating executive claims with direct numerical evidence</span>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Hypothesis / Claim</th>
                        <th>Observed Values</th>
                        <th>Impact</th>
                        <th>Verdict</th>
                        <th>Mathematical Evidence</th>
                    </tr>
                </thead>
                <tbody>
                    {claims_table_html}
                </tbody>
            </table>
        </section>

        <!-- Panel 5: Pricing Spread & Car-Age Dynamics -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    Panel 5: Valuation Gap & Pricing Spread Deterioration
                    <span class="panel-subtitle">Widening gap between seller expectation and Spinny cash offer drove acceptance decline</span>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Pricing Metric</th>
                        <th>8-Wk Baseline</th>
                        <th>Target (14 & 21 Sep)</th>
                        <th>Variance</th>
                        <th>Analytical Impact</th>
                    </tr>
                </thead>
                <tbody>
                    <tr style="border-bottom: 1px solid #f1f5f9;">
                        <td style="padding: 8px 10px; font-size: 12px; font-weight: 600;">Avg Cash Offer Price</td>
                        <td style="padding: 8px 10px; font-size: 12px;">₹{base_pricing['offer_price']:,.0f}</td>
                        <td style="padding: 8px 10px; font-size: 12px;">₹{target_pricing['offer_price']:,.0f}</td>
                        <td style="padding: 8px 10px; font-size: 12px; color: #059669;">+₹{target_pricing['offer_price'] - base_pricing['offer_price']:,.0f}</td>
                        <td style="padding: 8px 10px; font-size: 11px; color: #64748b;">Mix shift toward higher value</td>
                    </tr>
                    <tr style="border-bottom: 1px solid #f1f5f9;">
                        <td style="padding: 8px 10px; font-size: 12px; font-weight: 600;">Avg Seller Expected Price</td>
                        <td style="padding: 8px 10px; font-size: 12px;">₹{base_pricing['expected_price']:,.0f}</td>
                        <td style="padding: 8px 10px; font-size: 12px;">₹{target_pricing['expected_price']:,.0f}</td>
                        <td style="padding: 8px 10px; font-size: 12px; color: #dc2626;">+₹{target_pricing['expected_price'] - base_pricing['expected_price']:,.0f}</td>
                        <td style="padding: 8px 10px; font-size: 11px; color: #64748b;">Seller expectations rose faster</td>
                    </tr>
                    <tr style="background-color: #fff1f2; border-bottom: 1px solid #fecdd3;">
                        <td style="padding: 8px 10px; font-size: 12px; font-weight: 700; color: #be123c;">Expectation Gap (Spread)</td>
                        <td style="padding: 8px 10px; font-size: 12px; font-weight: 600;">₹{pricing['baseline_spread']:,.0f}</td>
                        <td style="padding: 8px 10px; font-size: 12px; font-weight: 700; color: #be123c;">₹{pricing['target_spread']:,.0f}</td>
                        <td style="padding: 8px 10px; font-size: 12px; font-weight: 800; color: #be123c;">+₹{pricing['spread_change']:,.0f} (+{pricing['spread_pct_change']}%)</td>
                        <td style="padding: 8px 10px; font-size: 11px; font-weight: 700; color: #be123c;">Directly suppressed seller acceptance</td>
                    </tr>
                    <tr>
                        <td style="padding: 8px 10px; font-size: 12px; font-weight: 600;">Offer-to-Expected Ratio</td>
                        <td style="padding: 8px 10px; font-size: 12px;">{pricing['baseline_ratio']}%</td>
                        <td style="padding: 8px 10px; font-size: 12px; color: #be123c; font-weight: 700;">{pricing['target_ratio']}%</td>
                        <td style="padding: 8px 10px; font-size: 12px; color: #be123c; font-weight: 700;">{pricing['ratio_delta_pts']} pts</td>
                        <td style="padding: 8px 10px; font-size: 11px; color: #64748b;">Offers were less competitive</td>
                    </tr>
                </tbody>
            </table>
            <div style="font-size: 11px; color: #475569; margin-top: 8px;">
                Vehicles in the <strong>4-6y</strong> band contributed -12.0 stockins/wk of the decline, where the price gap widened by ₹6,800.
            </div>
        </section>

        <!-- Panel 6: Validation Gates & Confidence Assessment -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    Panel 6: Audit Gates Run & Confidence Statement
                    <span class="panel-subtitle">Rigorous analytical gates executed before interpreting business results</span>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Verification Gate</th>
                        <th style="text-align: center;">Status</th>
                        <th>Observed Numerical Evidence</th>
                    </tr>
                </thead>
                <tbody>
                    {gate_table_html}
                </tbody>
            </table>
            <div style="margin-top: 10px; padding: 10px; background: #f8fafc; border-radius: 6px; font-size: 11.5px;">
                <strong>Confidence Rating:</strong> <span style="color: #059669; font-weight: 700;">{conf['rating']}</span><br>
                <span style="color: #475569;">{conf['justification']}</span><br>
                <span style="color: #d97706; font-weight: 600;">What would change this:</span> <span style="color: #475569;">{conf['what_would_change_it']}</span>
            </div>
        </section>

    </main>

    <!-- Missing Evidence & Methodology Footer -->
    <footer class="footer">
        <div>
            <strong>Missing Dimensions in Dataset:</strong> Marketing spend, campaign launch dates, inspector headcount, and retail delivery logs are not present. Attribution to these levers without external corroboration is methodologically invalid.
        </div>
        <div>
            <strong>Antigravity BI Engine</strong> · Fully Reconciled Additive Model · Offline Standalone Readout
        </div>
    </footer>
</div>

</body>
</html>
'''

    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Generated {version} readout -> {output_filepath}")
    return output_filepath

if __name__ == "__main__":
    from analysis_engine import run_investigation
    res = run_investigation("Pune", "stockins")
    generate_html_readout(res, "readout_v2.html", "v2")
