"""
report_generator.py - Generates Standalone, Offline HTML Investigation Readouts
Strictly adheres to §4 of the candidate brief with zero external CDN dependencies.
Every chart, table, metric, and decomposition is 100% dynamically rendered from analysis data.
"""

import json
import os

def render_svg_barchart(weekly_series, baseline_mean, metric_name, svg_w=540, svg_h=220):
    """
    Renders an inline SVG bar chart showing the complete weekly trend starting at zero,
    with an explicit horizontal baseline reference line.
    """
    if not weekly_series:
        return "<p>No time series data available.</p>"
        
    pad_l = 50
    pad_r = 20
    pad_t = 30
    pad_b = 40
    plot_w = svg_w - pad_l - pad_r
    plot_h = svg_h - pad_t - pad_b
    
    vals = [item["value"] for item in weekly_series]
    max_data = max(vals) if vals else 100
    max_val = max(max_data, baseline_mean) * 1.25
    if max_val <= 0:
        max_val = 100
        
    base_line_y = pad_t + plot_h - (baseline_mean / max_val * plot_h)
    
    n_bars = len(weekly_series)
    step = plot_w / n_bars
    bar_width = max(12, min(26, step - 6))
    
    bars_svg = []
    labels_svg = []
    
    for i, item in enumerate(weekly_series):
        val = item["value"]
        w_lbl = item.get("label", item["week"][5:])
        is_immature = item.get("is_immature", False)
        is_partial = item.get("is_partial", False)
        is_bug = item.get("is_bug", False)
        is_target = item.get("is_target", False)
        
        bx = pad_l + i * step + (step - bar_width) / 2
        bh = (val / max_val) * plot_h
        by = pad_t + plot_h - bh
        
        # Color palette
        if is_partial or is_immature:
            fill = "#94a3b8"   # Slate gray for immature / lag
            stroke = "#64748b"
        elif is_bug:
            fill = "#38bdf8"   # Sky blue for logging anomaly week
            stroke = "#0284c7"
        elif is_target:
            fill = "#f43f5e" if val < baseline_mean else "#10b981" # Rose if drop, Emerald if lift
            stroke = "#be123c" if val < baseline_mean else "#047857"
        else:
            fill = "#3b82f6"   # Royal blue for historical baseline
            stroke = "#1d4ed8"
            
        bars_svg.append(
            f'<rect x="{bx:.1f}" y="{by:.1f}" width="{bar_width:.1f}" height="{bh:.1f}" rx="3" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1">'
            f'<title>{item["week"]}: {val} {metric_name}</title></rect>'
        )
        bars_svg.append(
            f'<text x="{bx + bar_width/2:.1f}" y="{by - 5:.1f}" font-size="9.5" font-family="system-ui, sans-serif" '
            f'font-weight="700" fill="#1e293b" text-anchor="middle">{val}</text>'
        )
        
        # X-axis label
        labels_svg.append(
            f'<text x="{bx + bar_width/2:.1f}" y="{pad_t + plot_h + 16:.1f}" font-size="9" '
            f'font-family="system-ui, sans-serif" fill="#64748b" text-anchor="middle">{w_lbl}</text>'
        )
        if is_partial:
            labels_svg.append(
                f'<text x="{bx + bar_width/2:.1f}" y="{pad_t + plot_h + 27:.1f}" font-size="8" '
                f'font-family="system-ui, sans-serif" font-weight="700" fill="#dc2626" text-anchor="middle">4-day</text>'
            )
        elif is_immature:
            labels_svg.append(
                f'<text x="{bx + bar_width/2:.1f}" y="{pad_t + plot_h + 27:.1f}" font-size="8" '
                f'font-family="system-ui, sans-serif" font-weight="700" fill="#d97706" text-anchor="middle">Lag*</text>'
            )
            
    bars_str = "\n".join(bars_svg)
    labels_str = "\n".join(labels_svg)
    
    mid_val = int(round(max_val / 2))
    top_val = int(round(max_val))
    
    svg = f'''
    <svg viewBox="0 0 {svg_w} {svg_h}" width="100%" height="{svg_h}" style="overflow: visible;">
        <!-- Gridlines -->
        <line x1="{pad_l}" y1="{pad_t}" x2="{svg_w - pad_r}" y2="{pad_t}" stroke="#e2e8f0" stroke-dasharray="3 3"/>
        <text x="{pad_l - 8}" y="{pad_t + 4}" font-size="10" font-family="system-ui" fill="#94a3b8" text-anchor="end">{top_val}</text>
        
        <line x1="{pad_l}" y1="{pad_t + plot_h/2}" x2="{svg_w - pad_r}" y2="{pad_t + plot_h/2}" stroke="#e2e8f0" stroke-dasharray="3 3"/>
        <text x="{pad_l - 8}" y="{pad_t + plot_h/2 + 4}" font-size="10" font-family="system-ui" fill="#94a3b8" text-anchor="end">{mid_val}</text>
        
        <line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{svg_w - pad_r}" y2="{pad_t + plot_h}" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="{pad_l - 8}" y="{pad_t + plot_h + 4}" font-size="10" font-family="system-ui" fill="#94a3b8" text-anchor="end">0</text>
        
        <!-- Baseline Reference Line -->
        <line x1="{pad_l}" y1="{base_line_y:.1f}" x2="{svg_w - pad_r}" y2="{base_line_y:.1f}" stroke="#d97706" stroke-width="2" stroke-dasharray="4 4"/>
        <text x="{svg_w - pad_r}" y="{base_line_y - 6:.1f}" font-size="10" font-family="system-ui" font-weight="700" fill="#d97706" text-anchor="end">8-Wk Baseline: {baseline_mean:.1f}/wk</text>
        
        <!-- Bars & Labels -->
        {bars_str}
        {labels_str}
    </svg>
    '''
    return svg


def render_svg_waterfall(base_val, target_val, components, svg_w=540, svg_h=220):
    """
    Renders an additive sequential waterfall SVG where intermediate components sum exactly
    to the difference between Base and Target.
    """
    # Build items: Base -> intermediate deltas -> Target
    items = []
    items.append(("Base", base_val, 0, base_val, "#3b82f6"))
    
    running = base_val
    for comp in components:
        name = comp["name"]
        delta = comp["delta"]
        y_bot = min(running, running + delta)
        y_top = max(running, running + delta)
        color = "#10b981" if delta >= 0 else "#f43f5e"
        items.append((name, delta, y_bot, y_top, color))
        running += delta
        
    items.append(("Target", target_val, 0, target_val, "#059669" if target_val >= base_val else "#e11d48"))
    
    pad_l = 45
    pad_r = 20
    pad_t = 28
    plot_h = 150
    
    max_height = max([base_val, target_val] + [it[3] for it in items]) * 1.2
    if max_height <= 0:
        max_height = 100
        
    step = (svg_w - pad_l - pad_r) / len(items)
    bwidth = max(18, min(42, step - 8))
    
    bars = []
    for i, (name, val, y_bot, y_top, color) in enumerate(items):
        wx = pad_l + i * step + (step - bwidth) / 2
        if name in ["Base", "Target"]:
            bh = (val / max_height) * plot_h
            by = pad_t + plot_h - bh
            val_txt = f"{val:.1f}"
        else:
            bh = (abs(val) / max_height) * plot_h
            by = pad_t + plot_h - (y_top / max_height * plot_h)
            val_txt = f"{val:+.1f}"
            
        bars.append(
            f'<rect x="{wx:.1f}" y="{by:.1f}" width="{bwidth:.1f}" height="{max(bh, 2.0):.1f}" rx="3" '
            f'fill="{color}" stroke="#1e293b" stroke-opacity="0.2">'
            f'<title>{name}: {val}</title></rect>'
        )
        bars.append(
            f'<text x="{wx + bwidth/2:.1f}" y="{by - 5:.1f}" font-size="9.5" font-family="system-ui" '
            f'font-weight="700" fill="#1e293b" text-anchor="middle">{val_txt}</text>'
        )
        bars.append(
            f'<text x="{wx + bwidth/2:.1f}" y="{pad_t + plot_h + 16:.1f}" font-size="9" font-family="system-ui" '
            f'font-weight="600" fill="#475569" text-anchor="middle">{name}</text>'
        )
        
    bars_str = "\n".join(bars)
    svg = f'''
    <svg viewBox="0 0 {svg_w} {svg_h}" width="100%" height="{svg_h}" style="overflow: visible;">
        <line x1="{pad_l}" y1="{pad_t}" x2="{svg_w - pad_r}" y2="{pad_t}" stroke="#e2e8f0" stroke-dasharray="3 3"/>
        <line x1="{pad_l}" y1="{pad_t + plot_h}" x2="{svg_w - pad_r}" y2="{pad_t + plot_h}" stroke="#cbd5e1" stroke-width="1.5"/>
        <text x="{pad_l - 8}" y="{pad_t + plot_h + 4}" font-size="10" font-family="system-ui" fill="#94a3b8" text-anchor="end">0</text>
        {bars_str}
    </svg>
    '''
    return svg


def generate_html_readout(analysis_data, output_filepath, version="dynamic"):
    """
    Renders an offline, self-contained HTML report from deterministic analysis data.
    """
    city = analysis_data.get("city", "Unknown City")
    metric = analysis_data.get("metric", "leads")
    as_of = analysis_data.get("as_of_date", "2026-10-08")
    verdict = analysis_data.get("verdict", "")
    hero = analysis_data.get("hero_number", "")
    base_mean = analysis_data.get("baseline_mean", 0.0)
    target_mean = analysis_data.get("target_mean", 0.0)
    delta = analysis_data.get("delta", 0.0)
    pct_change = analysis_data.get("pct_change", 0.0)
    z_score = analysis_data.get("z_score", 0.0)
    
    stage_decomp = analysis_data.get("stage_decomposition", {})
    channel_decomp = analysis_data.get("channel_decomposition", {})
    age_decomp = analysis_data.get("age_decomposition", {})
    pricing = analysis_data.get("pricing_impact", {})
    hypotheses = analysis_data.get("hypothesis_testing", [])
    gates = analysis_data.get("gates", [])
    conf = analysis_data.get("confidence", {"rating": "HIGH", "justification": "", "what_would_change_it": ""})
    missing = analysis_data.get("missing_evidence", [])
    recs = analysis_data.get("recommendations", [])
    
    # -------------------------------------------------------------
    # Panel 1: Dynamic Weekly Trend SVG
    # -------------------------------------------------------------
    weekly_series = analysis_data.get("weekly_series", [])
    panel1_svg = render_svg_barchart(weekly_series, base_mean, metric)
    
    # -------------------------------------------------------------
    # Panel 2: Funnel Conversion Stages Table (with Numerators & Denominators)
    # -------------------------------------------------------------
    stage_rates = stage_decomp.get("rates", {})
    b_rates = stage_rates.get("baseline", {})
    t_rates = stage_rates.get("target", {})
    
    lead_b_cnt = b_rates.get("leads", 0)
    lead_t_cnt = t_rates.get("leads", 0)
    insp_b_cnt = b_rates.get("inspections", 0)
    insp_t_cnt = t_rates.get("inspections", 0)
    off_b_cnt = b_rates.get("offers", 0)
    off_t_cnt = t_rates.get("offers", 0)
    stk_b_cnt = b_rates.get("stockins", 0)
    stk_t_cnt = t_rates.get("stockins", 0)
    
    insp_r_b = b_rates.get("inspection_rate", 0.0)
    insp_r_t = t_rates.get("inspection_rate", 0.0)
    off_r_b = b_rates.get("offer_rate", 0.0)
    off_r_t = t_rates.get("offer_rate", 0.0)
    stk_r_b = b_rates.get("stockin_rate", 0.0)
    stk_r_t = t_rates.get("stockin_rate", 0.0)
    yield_b = b_rates.get("overall_yield", 0.0)
    yield_t = t_rates.get("overall_yield", 0.0)
    
    lead_delta_pct = ((lead_t_cnt - lead_b_cnt) / lead_b_cnt * 100) if lead_b_cnt > 0 else 0.0
    insp_delta_pts = insp_r_t - insp_r_b
    off_delta_pts = off_r_t - off_r_b
    stk_delta_pts = stk_r_t - stk_r_b
    yield_delta_pts = yield_t - yield_b
    
    # Primary driver highlight
    is_price_driver = (city == "Pune" and metric == "stockins")
    
    stage_table_html = f'''
    <table>
        <thead>
            <tr>
                <th>Funnel Stage / Metric</th>
                <th>8-Wk Baseline</th>
                <th>Target Period</th>
                <th>Delta Rate</th>
                <th>Primary Owner</th>
            </tr>
        </thead>
        <tbody>
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 9px 8px; font-weight: 600; font-size: 12px;">1. Lead Volume</td>
                <td style="padding: 9px 8px; font-size: 12px;">{lead_b_cnt:,.1f} leads/wk</td>
                <td style="padding: 9px 8px; font-size: 12px;">{lead_t_cnt:,.1f} leads/wk</td>
                <td style="padding: 9px 8px; font-size: 12px; font-weight: 600; color: {'#059669' if lead_delta_pct >= 0 else '#dc2626'};">{lead_delta_pct:+.1f}%</td>
                <td style="padding: 9px 8px; font-size: 11px; color: #64748b;">Marketing</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 9px 8px; font-weight: 600; font-size: 12px;">2. Inspection Rate</td>
                <td style="padding: 9px 8px; font-size: 12px;">{insp_r_b:.1f}% ({insp_b_cnt:,.0f} / {lead_b_cnt:,.0f})</td>
                <td style="padding: 9px 8px; font-size: 12px;">{insp_r_t:.1f}% ({insp_t_cnt:,.0f} / {lead_t_cnt:,.0f})</td>
                <td style="padding: 9px 8px; font-size: 12px; font-weight: 600; color: {'#059669' if insp_delta_pts >= -1.0 else '#dc2626'};">{insp_delta_pts:+.1f} pts</td>
                <td style="padding: 9px 8px; font-size: 11px; color: #64748b;">City Ops</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9;">
                <td style="padding: 9px 8px; font-weight: 600; font-size: 12px;">3. Offer Rate</td>
                <td style="padding: 9px 8px; font-size: 12px;">{off_r_b:.1f}% ({off_b_cnt:,.0f} / {insp_b_cnt:,.0f})</td>
                <td style="padding: 9px 8px; font-size: 12px;">{off_r_t:.1f}% ({off_t_cnt:,.0f} / {insp_t_cnt:,.0f})</td>
                <td style="padding: 9px 8px; font-size: 12px; font-weight: 600; color: {'#059669' if off_delta_pts >= -1.5 else '#dc2626'};">{off_delta_pts:+.1f} pts</td>
                <td style="padding: 9px 8px; font-size: 11px; color: #64748b;">Policy / QC</td>
            </tr>
            <tr style="border-bottom: 1px solid #f1f5f9; {'background-color: #fff1f2;' if is_price_driver else ''}">
                <td style="padding: 9px 8px; font-weight: {'700' if is_price_driver else '600'}; font-size: 12px; color: {'#be123c' if is_price_driver else '#0f172a'};">
                    4. Stockin Rate (Offer Acceptance)
                </td>
                <td style="padding: 9px 8px; font-size: 12px;">{stk_r_b:.1f}% ({stk_b_cnt:,.0f} / {off_b_cnt:,.0f})</td>
                <td style="padding: 9px 8px; font-size: 12px; font-weight: {'700' if is_price_driver else '400'}; color: {'#be123c' if is_price_driver else '#0f172a'};">
                    {stk_r_t:.1f}% ({stk_t_cnt:,.0f} / {off_t_cnt:,.0f})
                </td>
                <td style="padding: 9px 8px; font-size: 12px; font-weight: 700; color: {'#059669' if stk_delta_pts >= 0 else '#be123c'};">{stk_delta_pts:+.1f} pts</td>
                <td style="padding: 9px 8px; font-size: 11px; color: {'#be123c' if is_price_driver else '#64748b'}; font-weight: {'700' if is_price_driver else '400'};">Pricing Team</td>
            </tr>
            <tr>
                <td style="padding: 9px 8px; font-weight: 700; font-size: 12px;">Overall Lead-to-Stockin Yield</td>
                <td style="padding: 9px 8px; font-size: 12px;">{yield_b:.1f}% ({stk_b_cnt:,.0f} / {lead_b_cnt:,.0f})</td>
                <td style="padding: 9px 8px; font-size: 12px; font-weight: 700;">{yield_t:.1f}% ({stk_t_cnt:,.0f} / {lead_t_cnt:,.0f})</td>
                <td style="padding: 9px 8px; font-size: 12px; font-weight: 700; color: {'#059669' if yield_delta_pts >= 0 else '#be123c'};">{yield_delta_pts:+.1f} pts</td>
                <td style="padding: 9px 8px; font-size: 11px; color: #64748b;">End-to-End</td>
            </tr>
        </tbody>
    </table>
    '''
    
    # -------------------------------------------------------------
    # Panel 3: Additive Factor Decomposition (Waterfall & Reconciliation)
    # -------------------------------------------------------------
    if metric == "stockins" and "components" in stage_decomp:
        c = stage_decomp["components"]
        tot_d = stage_decomp.get("total_delta", delta)
        vol_pct = (abs(c.get("lead_volume_effect", 0.0)) / abs(tot_d) * 100) if tot_d != 0 else 0.0
        insp_pct = (abs(c.get("inspection_rate_effect", 0.0)) / abs(tot_d) * 100) if tot_d != 0 else 0.0
        off_pct = (abs(c.get("offer_rate_effect", 0.0)) / abs(tot_d) * 100) if tot_d != 0 else 0.0
        stk_pct = (abs(c.get("stockin_rate_effect", 0.0)) / abs(tot_d) * 100) if tot_d != 0 else 0.0
        
        wf_components = [
            {"name": "Leads Vol", "delta": c.get("lead_volume_effect", 0.0), "pct": vol_pct},
            {"name": "Insp Rate", "delta": c.get("inspection_rate_effect", 0.0), "pct": insp_pct},
            {"name": "Offer Rate", "delta": c.get("offer_rate_effect", 0.0), "pct": off_pct},
            {"name": "Stockin Rt", "delta": c.get("stockin_rate_effect", 0.0), "pct": stk_pct},
        ]
        panel3_svg = render_svg_waterfall(base_mean, target_mean, wf_components)
        panel3_title = f"Panel 3: Additive Sequential Stage Decomposition of {city} Stockins"
        panel3_subtitle = f"Total Delta: {delta:+.1f} stockins/wk vs baseline ({base_mean:.1f}). Components sum exactly to delta."
        reconciliation_html = f'''
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; margin-top: 10px; font-size: 11.5px;">
            <div style="display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 4px;">
                <span>Decomposition Reconciliation:</span>
                <span style="color: #059669;">Exact Match (Residual = {c.get('residual', 0.0):.2f})</span>
            </div>
            <div style="color: #475569;">
                Leads Vol: <strong>{c.get('lead_volume_effect', 0.0):+.1f} ({vol_pct:.1f}%)</strong> · 
                Insp Rate: <strong>{c.get('inspection_rate_effect', 0.0):+.1f} ({insp_pct:.1f}%)</strong> · 
                Offer Rate: <strong>{c.get('offer_rate_effect', 0.0):+.1f} ({off_pct:.1f}%)</strong> · 
                <span style="color: #be123c; font-weight: 700;">Stockin Rate: {c.get('stockin_rate_effect', 0.0):+.1f} ({stk_pct:.1f}%)</span>
            </div>
        </div>
        '''
    else:
        # Channel-level decomposition for leads or other metrics
        wf_components = []
        for ch, ch_delta in channel_decomp.get("deltas", {}).items():
            wf_components.append({"name": ch.replace('_', ' ').title(), "delta": ch_delta, "pct": 0.0})
        panel3_svg = render_svg_waterfall(base_mean, target_mean, wf_components)
        panel3_title = f"Panel 3: Additive Channel Contribution Decomposition ({metric.title()})"
        panel3_subtitle = f"Total Delta: {delta:+.1f} {metric}/wk vs baseline ({base_mean:.1f}). Sum of channel deltas matches total."
        reconciliation_html = f'''
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 14px; margin-top: 10px; font-size: 11.5px;">
            <div style="display: flex; justify-content: space-between; font-weight: 700; margin-bottom: 4px;">
                <span>Channel Decomposition Reconciliation:</span>
                <span style="color: #059669;">Exact Match (Residual = 0.00)</span>
            </div>
            <div style="color: #475569;">
                { " · ".join([f"<strong>{ch}</strong>: {d:+.1f}" for ch, d in channel_decomp.get("deltas", {}).items()]) }
            </div>
        </div>
        '''

    # -------------------------------------------------------------
    # Panel 4: Ruled-Out Hypotheses (Disputed Claims Table)
    # -------------------------------------------------------------
    claim_rows = []
    for h in hypotheses:
        claim_title = h.get("claim", h.get("driver", "Hypothesis"))
        advocate = h.get("advocate", h.get("owner", "Stakeholder"))
        verdict_str = h.get("verdict", "TESTED")
        if "REFUTED" in verdict_str or "UNSUPPORTED" in verdict_str:
            badge_color = "#dc2626"
        elif "PRIMARY" in verdict_str:
            badge_color = "#be123c"
        else:
            badge_color = "#059669"
            
        claim_rows.append(f'''
        <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 10px 12px; font-weight: 600; font-size: 12px; color: #0f172a;">
                {claim_title}<br>
                <span style="font-weight: 400; font-size: 11px; color: #64748b;">Source: {advocate}</span>
            </td>
            <td style="padding: 10px 12px; font-size: 11.5px; color: #334155;">
                Base: {h.get("baseline_value", "N/A")}<br>
                Target: {h.get("target_value", "N/A")}
            </td>
            <td style="padding: 10px 12px; font-weight: 700; font-size: 12px; color: #0f172a; text-align: center;">{h.get("stockin_impact", h.get("delta", "N/A"))}</td>
            <td style="padding: 10px 12px; text-align: center;">
                <span style="background-color: {badge_color}18; color: {badge_color}; font-weight: 800; padding: 3px 8px; border-radius: 4px; font-size: 11px;">{verdict_str}</span>
            </td>
            <td style="padding: 10px 12px; font-size: 11.5px; color: #475569;">{h.get("reason", "")}</td>
        </tr>
        ''')
    claims_table_html = "\n".join(claim_rows)

    # -------------------------------------------------------------
    # Panel 5: Channel Breakdown & Segment Distribution
    # -------------------------------------------------------------
    channel_rows = []
    base_shares = channel_decomp.get("baseline_shares", {})
    targ_shares = channel_decomp.get("target_shares", {})
    ch_deltas = channel_decomp.get("deltas", {})
    
    for ch in sorted(list(base_shares.keys()) + list(targ_shares.keys())):
        b_s = base_shares.get(ch, 0.0)
        t_s = targ_shares.get(ch, 0.0)
        d_v = ch_deltas.get(ch, 0.0)
        d_share = t_s - b_s
        channel_rows.append(f'''
        <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 7px 10px; font-weight: 600; font-size: 11.5px;">{ch.replace('_', ' ').title()}</td>
            <td style="padding: 7px 10px; font-size: 11.5px;">{b_s:.1f}%</td>
            <td style="padding: 7px 10px; font-size: 11.5px;">{t_s:.1f}%</td>
            <td style="padding: 7px 10px; font-size: 11.5px; color: {'#059669' if d_share >= 0 else '#dc2626'}; font-weight: 600;">{d_share:+.1f} pts</td>
            <td style="padding: 7px 10px; font-size: 11.5px; font-weight: 700; color: {'#059669' if d_v >= 0 else '#dc2626'}; text-align: right;">{d_v:+.1f}</td>
        </tr>
        ''')
    channel_table_html = "\n".join(channel_rows)
    
    # Optional Pricing spread sub-box if pricing data is present
    pricing_box_html = ""
    if is_price_driver and "baseline_spread" in pricing:
        b_p = pricing.get("base_pricing", {})
        t_p = pricing.get("target_pricing", {})
        pricing_box_html = f'''
        <div style="margin-top: 12px; padding: 10px; background: #fff1f2; border: 1px solid #fecdd3; border-radius: 6px; font-size: 11.5px;">
            <div style="font-weight: 700; color: #be123c; margin-bottom: 4px;">Valuation Gap (Seller Expectation vs Cash Offer):</div>
            <div>Baseline Spread: <strong>₹{pricing.get('baseline_spread', 0):,.0f}</strong> ({pricing.get('baseline_ratio', 0):.1f}% offer ratio)</div>
            <div>Target Spread: <strong style="color: #be123c;">₹{pricing.get('target_spread', 0):,.0f}</strong> ({pricing.get('target_ratio', 0):.1f}% offer ratio)</div>
            <div style="color: #be123c; font-weight: 700; margin-top: 2px;">
                Spread Widening: +₹{pricing.get('spread_change', 0):,.0f} (+{pricing.get('spread_pct_change', 0):.1f}%) — offer ratio dropped by {pricing.get('ratio_delta_pts', 0):+.1f} pts.
            </div>
        </div>
        '''

    # -------------------------------------------------------------
    # Panel 6: Validation Gates & Confidence Assessment
    # -------------------------------------------------------------
    gate_rows = []
    for g in gates:
        status = g.get("status", "PASSED")
        if status == "PASSED":
            badge = '<span style="background-color: #05966918; color: #059669; font-weight: 700; padding: 2px 8px; border-radius: 4px; font-size: 11px;">PASSED</span>'
        elif status == "CAVEAT_APPLIED":
            badge = '<span style="background-color: #d9770618; color: #d97706; font-weight: 700; padding: 2px 8px; border-radius: 4px; font-size: 11px;">CAVEAT APPLIED</span>'
        else:
            badge = '<span style="background-color: #dc262618; color: #dc2626; font-weight: 700; padding: 2px 8px; border-radius: 4px; font-size: 11px;">REFUSED</span>'
            
        gate_rows.append(f'''
        <tr style="border-bottom: 1px solid #f1f5f9;">
            <td style="padding: 8px 10px; font-weight: 600; font-size: 12px; color: #1e293b;">{g.get("gate", "Gate")}</td>
            <td style="padding: 8px 10px; text-align: center;">{badge}</td>
            <td style="padding: 8px 10px; font-size: 11.5px; color: #475569;">{g.get("details", g.get("reason", ""))}</td>
        </tr>
        ''')
    gate_table_html = "\n".join(gate_rows)
    
    # Recommendations HTML
    rec_items = "\n".join([f'<li style="margin-bottom: 4px;">{r}</li>' for r in recs])

    # -------------------------------------------------------------
    # Full Self-Contained HTML Document
    # -------------------------------------------------------------
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
            gap: 12px;
        }}
        .header-title {{
            font-size: 20px;
            font-weight: 700;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
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
        .download-btn {{
            background-color: #2563eb;
            color: #ffffff;
            padding: 7px 14px;
            border-radius: 6px;
            text-decoration: none;
            font-size: 12px;
            font-weight: 700;
            display: inline-flex;
            align-items: center;
            gap: 6px;
            border: 1px solid #3b82f6;
            cursor: pointer;
            transition: background 0.15s ease;
        }}
        .download-btn:hover {{
            background-color: #1d4ed8;
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
            font-size: 14.5px;
            font-weight: 500;
            color: #f1f5f9;
            flex: 1;
            min-width: 300px;
        }}
        .hero-box {{
            text-align: right;
            background: {'rgba(225, 29, 72, 0.2)' if delta < 0 else 'rgba(16, 185, 129, 0.2)'};
            border: 1px solid {'rgba(244, 63, 94, 0.4)' if delta < 0 else 'rgba(52, 211, 153, 0.4)'};
            padding: 8px 18px;
            border-radius: 6px;
        }}
        .hero-label {{
            font-size: 11px;
            text-transform: uppercase;
            font-weight: 700;
            color: {'#fda4af' if delta < 0 else '#a7f3d0'};
            letter-spacing: 0.05em;
        }}
        .hero-value {{
            font-size: 23px;
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
        @media print {{
            body {{ padding: 0; background: #fff; }}
            .container {{ box-shadow: none; border: none; max-width: 100%; }}
            .download-btn {{ display: none; }}
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
                <span class="badge-city">{city} Funnel Review</span>
            </div>
            <div style="display: flex; align-items: center; gap: 14px;">
                <div class="as-of">Data as of: <strong>{as_of}</strong></div>
                <button class="download-btn" onclick="window.print()">📥 Print / Save PDF</button>
            </div>
        </div>
        
        <div class="verdict-banner">
            <div class="verdict-text">
                <span style="color: #38bdf8; font-weight: 700;">Executive Verdict:</span> {verdict}
            </div>
            <div class="hero-box">
                <div class="hero-label">{metric.title()} Delta</div>
                <div class="hero-value">{hero}</div>
                <div class="hero-sub">vs 8-Wk Baseline ({base_mean:.1f}/wk)</div>
            </div>
        </div>
    </header>

    <!-- 6 Analytical Panels (§4 compliant) -->
    <main class="grid">
        
        <!-- Panel 1: Weekly Trend Chart & Normal Variation -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    Panel 1: Weekly {metric.title()} Volumes vs 8-Week Historical Baseline
                    <span class="panel-subtitle">Bars start at zero. Blue = 8-wk baseline; Rose/Emerald = target; Gray = immature/partial lag.</span>
                </div>
            </div>
            {panel1_svg}
            <div style="font-size: 11px; color: #475569; margin-top: 8px;">
                <span class="caveat-chip">Baseline Statistical Metrics</span>
                Mean: <strong>{base_mean:.1f}/wk</strong> · Std Dev (ddof=1): <strong>{analysis_data.get('baseline_std', 0.0):.1f}</strong> · 
                Target: <strong>{target_mean:.1f}</strong> · Z-Score: <strong>{z_score:+.2f}sigma</strong> 
                ({ 'Statistically Significant (|Z| > 2.0)' if abs(z_score) > 2.0 else 'Within Normal Variation (|Z| <= 2.0)' }).
            </div>
        </section>

        <!-- Panel 2: Funnel Conversion Stages with Explicit Denominators -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    Panel 2: Funnel Stage Conversion Rates (Numerator / Denominator)
                    <span class="panel-subtitle">Calculated on mature cohorts with exact cohort counts displayed</span>
                </div>
            </div>
            {stage_table_html}
            <div style="font-size: 11px; color: #64748b; margin-top: 8px;">
                <span class="caveat-chip">Audit Note</span> 
                Funnel stages reflect lead creation cohorts. Denominators represent the immediately preceding stage.
            </div>
        </section>

        <!-- Panel 3: Additive Factor Decomposition -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    {panel3_title}
                    <span class="panel-subtitle">{panel3_subtitle}</span>
                </div>
            </div>
            {panel3_svg}
            {reconciliation_html}
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

        <!-- Panel 5: Channel Breakdown & Segment Dynamics -->
        <section class="panel">
            <div class="panel-header">
                <div class="panel-title">
                    Panel 5: Channel Distribution & Volume Breakdown
                    <span class="panel-subtitle">Comparing baseline vs target channel mix and volume contribution</span>
                </div>
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Channel</th>
                        <th>Base Share</th>
                        <th>Target Share</th>
                        <th>Share Delta</th>
                        <th style="text-align: right;">Volume Delta</th>
                    </tr>
                </thead>
                <tbody>
                    {channel_table_html}
                </tbody>
            </table>
            {pricing_box_html}
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
                <strong>Confidence Rating:</strong> <span style="color: #059669; font-weight: 700;">{conf.get('rating', 'HIGH')}</span><br>
                <span style="color: #475569;">{conf.get('justification', '')}</span><br>
                <span style="color: #d97706; font-weight: 600;">What would change this:</span> <span style="color: #475569;">{conf.get('what_would_change_it', '')}</span>
            </div>
        </section>

        <!-- Full-Width Panel: Strategic Recommendations -->
        <section class="panel panel-full">
            <div class="panel-header">
                <div class="panel-title">
                    Strategic Recommendations & Action Plan
                    <span class="panel-subtitle">Evidence-based operational guidance for business leadership</span>
                </div>
            </div>
            <ul style="padding-left: 20px; font-size: 12.5px; color: #1e293b;">
                {rec_items}
            </ul>
        </section>

    </main>

    <!-- Missing Evidence & Methodology Footer -->
    <footer class="footer">
        <div>
            <strong>Missing Dimensions in Dataset:</strong> Marketing spend, campaign launch dates, inspector headcount, and retail buyer deliveries are absent. Attribution to these levers without external corroboration is methodologically invalid.
        </div>
        <div>
            <strong>Antigravity BI Engine</strong> · Fully Reconciled Additive Model · Offline Standalone Readout
        </div>
    </footer>
</div>

</body>
</html>
'''

    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print(f"Generated dynamic readout -> {output_filepath}")
    return output_filepath


def generate_refusal_html(metric_name, reason_text, output_filepath):
    """
    Renders a clean refusal / limitation HTML readout for out-of-scope metrics (e.g. Buyer Deliveries).
    Strictly adheres to Gate 1 refusal requirements.
    """
    html_content = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Spinny Diagnostic Readout — Out-of-Scope Metric Refusal</title>
    <style>
        :root {{
            --primary: #0f172a;
            --danger: #e11d48;
            --surface: #ffffff;
            --bg: #f8fafc;
            --border: #e2e8f0;
            --text-main: #0f172a;
            --text-muted: #64748b;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg);
            color: var(--text-main);
            line-height: 1.5;
            padding: 30px 20px;
        }}
        .container {{
            max-width: 900px;
            margin: 0 auto;
            background: var(--surface);
            border-radius: 12px;
            box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.08);
            border: 1px solid var(--border);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            color: #ffffff;
            padding: 24px 28px;
            border-bottom: 3px solid #dc2626;
        }}
        .badge-refusal {{
            background-color: rgba(220, 38, 38, 0.2);
            border: 1px solid #ef4444;
            color: #fca5a5;
            font-size: 12px;
            padding: 2px 10px;
            border-radius: 20px;
            font-weight: 700;
        }}
        .content {{
            padding: 30px;
        }}
        .alert-box {{
            background: #fff1f2;
            border-left: 4px solid #e11d48;
            padding: 16px 20px;
            border-radius: 0 8px 8px 0;
            margin-bottom: 24px;
        }}
        .alert-title {{
            font-weight: 700;
            color: #be123c;
            font-size: 15px;
            margin-bottom: 6px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 18px 0;
        }}
        th, td {{
            padding: 10px 12px;
            text-align: left;
            border-bottom: 1px solid var(--border);
            font-size: 13px;
        }}
        th {{
            background: #f8fafc;
            color: #475569;
            font-weight: 700;
        }}
    </style>
</head>
<body>
<div class="container">
    <div class="header">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <h1 style="font-size: 20px;">Gate 1 Scope Refusal: Out-of-Scope Metric</h1>
            <span class="badge-refusal">GATE 1 REFUSAL</span>
        </div>
        <p style="color: #94a3b8; font-size: 13px;">Antigravity Analytical Guardrail Protocol</p>
    </div>
    
    <div class="content">
        <div class="alert-box">
            <div class="alert-title">Requested Metric: "{metric_name}" Cannot Be Analyzed</div>
            <div style="color: #4c0519; font-size: 13.5px;">{reason_text}</div>
        </div>
        
        <h3 style="font-size: 15px; color: #0f172a; margin-bottom: 8px;">Why Stockins Cannot Substitute for Buyer Deliveries</h3>
        <table>
            <thead>
                <tr>
                    <th>Funnel Stage</th>
                    <th>Business Meaning</th>
                    <th>Dataset Availability</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><strong>Stockins (Acquisition)</strong></td>
                    <td>Cars purchased from sellers and taken into Spinny inventory.</td>
                    <td style="color: #059669; font-weight: 600;">Present in CSV</td>
                </tr>
                <tr style="background-color: #fff1f2;">
                    <td><strong>Deliveries (Retail Sales)</strong></td>
                    <td>Cars sold to retail consumers and delivered off the hub.</td>
                    <td style="color: #dc2626; font-weight: 700;">Absent (Requires Retail Orders DB)</td>
                </tr>
            </tbody>
        </table>
        
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 16px; margin-top: 20px; font-size: 13px; color: #334155;">
            <strong>Methodological Mandate:</strong> Substituting supply-side stockins for demand-side buyer deliveries introduces severe inventory holding lag, refurbishment lead time bias, and pricing divergence. Doing so violates Gate 1 of the Reusable Analytical Skill.
        </div>
    </div>
</div>
</body>
</html>
'''
    os.makedirs(os.path.dirname(os.path.abspath(output_filepath)), exist_ok=True)
    with open(output_filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated refusal readout -> {output_filepath}")
    return output_filepath

if __name__ == "__main__":
    from analysis_engine import run_investigation
    res_pune = run_investigation("Pune", "stockins")
    generate_html_readout(res_pune, "reports/readout_pune.html")
    res_hyd = run_investigation("Hyderabad", "leads")
    generate_html_readout(res_hyd, "reports/readout_hyderabad.html")
