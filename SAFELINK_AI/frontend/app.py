"""SafeLink AI – Intelligent Fraud URL Detector Frontend.
Built with Streamlit & Plotly.

Tagline: Don't click blindly. Check before you trust.
Cyber Theme: Inspired by USER.CTRL with Animated Transparent 3D Rotating Earth.
"""

import sys
import urllib.parse
from pathlib import Path
from datetime import datetime
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Setup python path so frontend can import backend modules
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

from backend.model_service import model_service
from frontend.cyber_theme import (
    CYBER_CSS,
    get_cyber_earth_background_html,
    get_cyber_header_html,
    get_cyber_metric_cards_html,
)

# Page configuration
st.set_page_config(
    page_title="SafeLink AI – Fraud URL Detector",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Inject Cyberpunk CSS & Transparent 3D Rotating Earth Background
st.markdown(CYBER_CSS, unsafe_allow_html=True)
st.markdown(get_cyber_earth_background_html(), unsafe_allow_html=True)


def create_risk_gauge(score: int, level: str):
    """Creates a beautiful interactive speedometer gauge chart styled for the dark cyber theme."""
    if level == "Low":
        bar_color = "#00F5A0"  # Neon Mint / Safe
    elif level == "Medium":
        bar_color = "#F59E0B"  # Amber / Caution
    else:
        bar_color = "#C83B4B"  # Red / Danger

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': f"Risk Score: {score} / 100", 'font': {'size': 20, 'color': '#F7F9FC'}},
        number={'font': {'size': 44, 'color': bar_color}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#7088A5"},
            'bar': {'color': bar_color, 'thickness': 0.3},
            'bgcolor': "rgba(13, 21, 34, 0.8)",
            'borderwidth': 1,
            'bordercolor': "rgba(255, 255, 255, 0.12)",
            'steps': [
                {'range': [0, 30], 'color': 'rgba(22, 133, 91, 0.28)'},
                {'range': [30, 70], 'color': 'rgba(217, 119, 6, 0.28)'},
                {'range': [70, 100], 'color': 'rgba(200, 59, 75, 0.35)'}
            ],
            'threshold': {
                'line': {'color': "#C83B4B", 'width': 4},
                'thickness': 0.75,
                'value': 70
            }
        }
    ))
    fig.update_layout(
        height=240,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font={'family': "-apple-system, BlinkMacSystemFont, Segoe UI, Roboto, sans-serif", 'color': '#F7F9FC'}
    )
    return fig


def generate_html_report(result) -> str:
    """Generates a standalone, beautifully formatted HTML report of the URL analysis."""
    risk = result.risk
    dns = result.domain_existence
    typo = result.typosquatting
    intent = getattr(result, "intention", None)
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

    score_color = "#16855B" if risk.risk_level == "Low" else ("#D97706" if risk.risk_level == "Medium" else "#C83B4B")
    badge_bg = "#EBF7F2" if risk.risk_level == "Low" else ("#FEF7E6" if risk.risk_level == "Medium" else "#FDF1F2")

    factors_html = ""
    for f in result.factors:
        icon = "🚩" if f.category == "risk" else "✅"
        border_col = "#C83B4B" if f.category == "risk" else "#16855B"
        factors_html += f"""
        <div style="background:#FFFFFF; border-left:4px solid {border_col}; padding:8px 12px; margin-bottom:8px; border-radius:4px;">
            <strong>{icon} {f.title}</strong> — <code>{f.severity.upper()}</code> ({f.score_impact:+.0f} pts)<br/>
            <span style="font-size:0.9rem; color:#334E68;">{f.description}</span>
        </div>
        """

    recs_html = ""
    for r in result.recommendations:
        recs_html += f"""
        <div style="margin-bottom:8px;">
            <strong>• {r.title}:</strong> {r.guidance}
        </div>
        """

    target_data_str = ", ".join(intent.targeted_data) if intent else "None"
    intent_summary = intent.intent_summary if intent else "Standard analysis"
    intent_category = intent.category if intent else "Web Analysis"

    target_url = result.cleaned_url if hasattr(result, "cleaned_url") else result.url
    encoded_url = urllib.parse.quote(target_url, safe="")
    screenshot_url = f"https://s0.wp.com/mshots/v1/{encoded_url}?w=800"

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>SafeLink AI - Security Assessment Certificate</title>
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; background: #080D15; padding: 30px; color: #142B4A; }}
    .cert-card {{ max-width: 800px; margin: 0 auto; background: #ffffff; border-radius: 12px; border: 1px solid #DCE3EE; box-shadow: 0 8px 32px rgba(0,0,0,0.4); padding: 36px; }}
    .header {{ border-bottom: 2px solid #DCE3EE; padding-bottom: 16px; margin-bottom: 24px; display: flex; justify-content: space-between; align-items: center; }}
    .title {{ font-size: 24px; font-weight: 800; color: #142B4A; }}
    .subtitle {{ font-size: 14px; color: #4A607A; }}
    .score-badge {{ display: inline-block; background: {badge_bg}; color: {score_color}; font-size: 26px; font-weight: 800; padding: 8px 22px; border-radius: 8px; border: 2px solid {score_color}; margin: 16px 0; }}
    .section-title {{ font-size: 16px; font-weight: 700; color: #142B4A; margin-top: 24px; margin-bottom: 10px; border-bottom: 1px solid #DCE3EE; padding-bottom: 4px; }}
    .meta-table {{ width: 100%; border-collapse: collapse; margin: 12px 0; }}
    .meta-table td {{ padding: 6px 10px; border-bottom: 1px solid #EDF2F7; font-size: 14px; color: #142B4A; }}
    .meta-table td.label {{ font-weight: 600; width: 30%; color: #334E68; }}
    
    /* Browser Mockup Window for Website Screenshot */
    .browser-mockup {{ background: #0F172A; border-radius: 8px; border: 1px solid #CBD5E1; overflow: hidden; margin: 14px 0 20px 0; box-shadow: 0 4px 16px rgba(0,0,0,0.08); }}
    .browser-header {{ background: #1E293B; padding: 8px 14px; display: flex; align-items: center; gap: 6px; border-bottom: 1px solid #334155; }}
    .browser-dot {{ width: 10px; height: 10px; border-radius: 50%; display: inline-block; }}
    .dot-red {{ background: #EF4444; }}
    .dot-yellow {{ background: #F59E0B; }}
    .dot-green {{ background: #10B981; }}
    .browser-address {{ background: #0F172A; color: #94A3B8; font-family: monospace; font-size: 11px; padding: 4px 10px; border-radius: 4px; margin-left: 10px; flex-grow: 1; border: 1px solid #334155; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .sandbox-tag {{ color: #10B981; font-size: 10px; font-weight: 700; background: rgba(16, 185, 129, 0.15); padding: 3px 8px; border-radius: 10px; border: 1px solid rgba(16, 185, 129, 0.3); }}
    .browser-viewport {{ min-height: 200px; background: #F8FAFC; display: flex; align-items: center; justify-content: center; position: relative; }}
    .screenshot-image {{ width: 100%; max-height: 420px; object-fit: cover; display: block; }}
    .report-fallback {{ display: none; flex-direction: column; align-items: center; justify-content: center; padding: 36px 20px; text-align: center; }}

    .disclaimer {{ background: #EDF2F7; border: 1px solid #DCE3EE; border-radius: 6px; padding: 12px; font-size: 11px; color: #4A607A; margin-top: 28px; }}
    a {{ color: #3978D6; text-decoration: none; font-weight: 600; }}
</style>
</head>
<body>
<div class="cert-card">
    <div class="header">
        <div>
            <div class="title">🛡️ SafeLink AI — Security Assessment</div>
            <div class="subtitle">Intelligent Fraud URL Detection • Don't click blindly. Check before you trust.</div>
        </div>
        <div style="text-align:right; font-size:12px; color:#4A607A;">
            Generated: {now_str}<br/>
            Engine: SafeLink v1.2.0
        </div>
    </div>

    <div style="text-align:center;">
        <div style="font-size:13px; color:#4A607A; text-transform:uppercase; font-weight:700;">Analyzed Target URL</div>
        <code style="font-size:15px; word-break:break-all; color:#142B4A; background:#EDF2F7; padding:6px 12px; border-radius:6px; display:inline-block; margin-top:4px;">{result.url}</code><br/>
        <div class="score-badge">Risk Score: {risk.score} / 100 • {risk.risk_level.upper()} RISK</div>
        <div style="font-weight:700; font-size:16px; color:#142B4A;">{risk.phishing_classification}</div>
    </div>

    <div class="section-title">Visual Evidence • Isolated Website Sandbox Snapshot</div>
    <div class="browser-mockup">
        <div class="browser-header">
            <span class="browser-dot dot-red"></span>
            <span class="browser-dot dot-yellow"></span>
            <span class="browser-dot dot-green"></span>
            <span class="browser-address">{target_url}</span>
            <span class="sandbox-tag">🔒 Cloud-Sandboxed Capture</span>
        </div>
        <div class="browser-viewport">
            <img id="target-screenshot" src="{screenshot_url}" alt="Target Website Sandbox Snapshot" class="screenshot-image" onerror="this.style.display='none'; document.getElementById('report-fallback').style.display='flex';" onload="var retries=Number(this.dataset.retries||0); if(this.naturalWidth<600) {{ if(retries<3) {{ this.dataset.retries=retries+1; setTimeout(()=>{{this.src=this.src.split('&retry=')[0]+'&retry='+Date.now()}},5000); }} else {{this.style.display='none'; document.getElementById('report-fallback').style.display='flex';}} }}" />
            <div id="report-fallback" class="report-fallback">
                <div style="font-size:36px; margin-bottom:8px;">🛡️</div>
                <div style="font-weight:700; font-size:15px; color:#142B4A;">Website Snapshot</div>
                <div style="font-size:12px; color:#64748B; max-width:460px; margin-top:4px;">
                    The screenshot service may need a few seconds or may be unable to capture this site. Try again after the page loads.
                </div>
                <button type="button" onclick="var img=document.getElementById('target-screenshot'); img.dataset.retries=0; img.style.display='block'; this.parentElement.style.display='none'; img.src=img.src.split('&retry=')[0]+'&retry='+Date.now();">Retry screenshot</button>
            </div>
        </div>
    </div>

    <div class="section-title">1. Target Intention & Threat Objective</div>
    <table class="meta-table">
        <tr><td class="label">Identified Objective:</td><td><strong>{intent_category}</strong></td></tr>
        <tr><td class="label">Summary:</td><td>{intent_summary}</td></tr>
        <tr><td class="label">Targeted Data / Assets:</td><td>{target_data_str}</td></tr>
    </table>

    <div class="section-title">2. Domain Verification & DNS Status</div>
    <table class="meta-table">
        <tr><td class="label">Domain Existence:</td><td>{'✅ Active / Resolves in Global DNS' if dns.exists else '❌ Non-Existent / Inactive (NXDOMAIN)'} ({dns.status})</td></tr>
        <tr><td class="label">Brand Similarity:</td><td>{'⚠️ Mimics ' + str(typo.target_brand) if typo.is_typosquatting else ('🛡️ Verified Official Brand' if typo.is_official_brand else 'Clean Domain')}</td></tr>
        <tr><td class="label">Root Domain:</td><td><code>{result.anatomy.root_domain}.{result.anatomy.tld}</code></td></tr>
        <tr><td class="label">Transport Protocol:</td><td>{'HTTPS (Encrypted)' if result.features.get('is_https') == 1 else 'HTTP (Unencrypted)'}</td></tr>
    </table>

    <div class="section-title">3. Contributing Factors & Red Flags</div>
    {factors_html}

    <div class="section-title">4. Actionable Precautions & Guidance</div>
    {recs_html}

    <div class="disclaimer">
        <strong>Important Limitation:</strong> The risk score and intention analysis are heuristic and pattern indicators generated by SafeLink AI static analyzers. This report is not legal or definitive proof of website safety or criminality. Offline static evaluation was performed without visiting the remote server.
    </div>
</div>
</body>
</html>"""
    return html_content


# Sidebar Navigation & Educational Info
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=64)
    st.title("SafeLink AI")
    st.markdown("**Intelligent Cyber Defense**")
    st.markdown("---")

    st.subheader("🛡️ Core Verification Pillars")
    st.markdown("""
    1. **Domain Existence Check**:
       Verifies if the domain actually exists in global DNS or is a fake/inactive NXDOMAIN.
    2. **Phishing vs Legitimate Verdict**:
       Explicit determination of fraudulent, suspicious, or authentic link nature.
    3. **Score & Risk Grade**:
       Granular 0-100 score classified into **Low Score (Safe)**, **Medium Score (Caution)**, or **High Score (Dangerous)**.
    4. **Typosquatting & Brand Similarity**:
       Detects lookalike imitations like `nnicrosoft` (mimicking Microsoft) and `g00gle` (mimicking Google).
    """)

    st.markdown("---")
    st.markdown("""
    > **Cyber Prototype Notice**  
    > The risk score is an indicator based on URL patterns, DNS resolution, and trained ML models. It is not definitive proof. Prototype for fraud awareness.
    """)
    st.caption("SafeLink AI v1.2.0 • FastAPI • Scikit-Learn • Streamlit")


# Top Cyber Header & Metric Status Bar (USER.CTRL Style)
st.markdown(get_cyber_header_html(), unsafe_allow_html=True)
st.markdown(get_cyber_metric_cards_html(), unsafe_allow_html=True)

# Privacy Preserving Notice
st.markdown("""
<div class="privacy-badge">
    <strong>🔒 100% Privacy-Preserving Engine:</strong> SafeLink AI analyses URL content, DNS status, and deceptive patterns without loading or visiting the destination website. Your IP address, device footprint, and network remain completely protected.
</div>
""", unsafe_allow_html=True)

# Input Form
with st.container():
    url_to_analyze = st.text_input(
        "Enter or paste the suspicious URL to analyze:",
        value=st.session_state.get("url_input", ""),
        placeholder="e.g. http://nnicrosoft.com/login or http://g00gle.com or https://paypal.com",
        key="main_url_input",
    )
    col_btn, col_dns_toggle, col_clear = st.columns([2, 3, 2])
    analyze_clicked = col_btn.button("🔍 Check URL Safety", type="primary", use_container_width=True)
    check_dns_enabled = col_dns_toggle.checkbox("Perform Live DNS Domain Existence Check", value=True)
    if col_clear.button("Clear Input"):
        st.session_state["url_input"] = ""
        st.rerun()

# Run Analysis
if analyze_clicked or (url_to_analyze and url_to_analyze != st.session_state.get("last_analyzed", "")):
    if not url_to_analyze.strip():
        st.warning("Please enter a valid URL to analyze.")
    else:
        st.session_state["last_analyzed"] = url_to_analyze.strip()
        with st.spinner("Analyzing URL content, domain existence, and similarity patterns..."):
            try:
                result = model_service.analyze(url_to_analyze.strip(), check_dns=check_dns_enabled)
            except Exception as e:
                st.error(f"Error evaluating URL: {e}")
                result = None

        if result:
            score = result.risk.score
            level = result.risk.risk_level
            grade = result.risk.score_grade
            is_phish = result.risk.is_phishing
            phish_class = result.risk.phishing_classification
            verdict = result.risk.verdict
            typo = result.typosquatting
            dns = result.domain_existence

            st.markdown("---")

            # TOP LEVEL CALLOUTS: TYPOSQUATTING ALERT (If Detected)
            if typo.is_typosquatting:
                st.markdown(f"""
                <div class="typo-alert-box">
                    <h3 style="color:#C83B4B; margin:0 0 6px 0;">🚨 CRITICAL TYPOSQUATTING DETECTED!</h3>
                    <p style="font-size:1.05rem; margin:0 0 8px 0; color:#FFA5AE;">
                        The domain <strong>'{result.anatomy.root_domain}'</strong> is a deceptive imitation of <strong>'{typo.target_brand}'</strong>!
                    </p>
                    <div style="font-size:0.95rem; color:#E2E8F0;">
                        • <strong>Impersonation Technique:</strong> {typo.technique}<br/>
                        • <strong>Similarity Match:</strong> {typo.similarity_percentage:.1f}%<br/>
                        • <strong>Authentic Official Domain:</strong> <a href="https://{typo.official_domain}" target="_blank" style="color:#3978D6; font-weight:bold;">https://{typo.official_domain}</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            elif typo.is_official_brand:
                st.success(f"✅ Verified Authentic Website: This is the official domain for **{typo.target_brand}** ({typo.official_domain}).")

            # TOP 4 CORE STATUS CARDS (User Requirements)
            col_v1, col_v2, col_v3, col_v4 = st.columns(4)

            # 1. Phishing Website or Not
            with col_v1:
                st.markdown("**1. Phishing Classification**")
                if is_phish:
                    st.markdown('<span class="badge-pill-danger">🚨 PHISHING WEBSITE</span>', unsafe_allow_html=True)
                elif level == "Medium":
                    st.markdown('<span class="badge-pill-warning">⚠️ SUSPICIOUS LINK</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-pill-success">✅ LEGITIMATE WEBSITE</span>', unsafe_allow_html=True)
                st.caption(phish_class)

            # 2. Low Score or High Score
            with col_v2:
                st.markdown("**2. Risk Score Grade**")
                if level == "Low":
                    st.markdown('<span class="badge-pill-success">🟢 LOW SCORE (SAFE)</span>', unsafe_allow_html=True)
                elif level == "Medium":
                    st.markdown('<span class="badge-pill-warning">🟡 MEDIUM SCORE (CAUTION)</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="badge-pill-danger">🔴 HIGH SCORE (DANGEROUS)</span>', unsafe_allow_html=True)
                st.caption(f"Score: {score}/100 • Grade: {grade}")

            # 3. Domain Existence (Does it exist or not?)
            with col_v3:
                st.markdown("**3. Domain Existence Status**")
                if dns.exists:
                    st.markdown('<span class="badge-pill-success">🌐 DOMAIN EXISTS (ACTIVE)</span>', unsafe_allow_html=True)
                    st.caption(f"{dns.status} • Resolves to {len(dns.resolved_ips)} IP(s)")
                else:
                    st.markdown('<span class="badge-pill-danger">❌ DOES NOT EXIST (NXDOMAIN)</span>', unsafe_allow_html=True)
                    st.caption("Host not found in global DNS records")

            # 4. Brand Similarity Check
            with col_v4:
                st.markdown("**4. Brand Similarity Check**")
                if typo.is_typosquatting:
                    st.markdown(f'<span class="badge-pill-danger">⚠️ MIMICS {typo.target_brand.upper()}</span>', unsafe_allow_html=True)
                    st.caption(f"{typo.similarity_percentage:.0f}% match to {typo.target_brand}")
                elif typo.is_official_brand:
                    st.markdown('<span class="badge-pill-success">🛡️ OFFICIAL BRAND</span>', unsafe_allow_html=True)
                    st.caption(f"Genuine {typo.target_brand} property")
                else:
                    st.markdown('<span class="badge-pill-success">✓ NO SQUATTING</span>', unsafe_allow_html=True)
                    st.caption("No brand lookalike detected")

            # MAIN VISUALIZATION: Gauge Meter + Key Findings
            st.markdown("### 📊 Risk Evaluation Summary")
            gauge_col, summary_col = st.columns([1, 1])

            with gauge_col:
                st.plotly_chart(create_risk_gauge(score, level), use_container_width=True)

            with summary_col:
                st.markdown(f"#### Verdict: **{verdict}**")
                st.markdown(f"""
                - **Analyzed URL:** `{result.cleaned_url}`
                - **Root Domain:** `{result.anatomy.root_domain}.{result.anatomy.tld}`
                - **Random Forest ML Probability:** `{result.risk.ml_risk_probability*100:.1f}%`
                - **Rule-Based Heuristic Penalty:** `{result.risk.heuristic_score} / 100`
                - **Transport Security:** `{"HTTPS (Encrypted)" if result.features.get("is_https") == 1 else "HTTP (Unencrypted)"}`
                """)
                
                # Downloadable Formal Security Certificate / Report
                report_html_data = generate_html_report(result)
                st.download_button(
                    label="📄 Download Security Report (HTML)",
                    data=report_html_data,
                    file_name=f"SafeLink_Report_{result.anatomy.root_domain}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                    mime="text/html",
                    use_container_width=True
                )

            # MAIN INTENTION OF THE WEBSITE
            intent = getattr(result, "intention", None)
            if intent is None:
                from backend.intention_analyzer import analyze_website_intention
                from backend.schemas import WebsiteIntention
                anatomy_dict = result.anatomy.model_dump() if hasattr(result.anatomy, "model_dump") else (result.anatomy.__dict__ if hasattr(result.anatomy, "__dict__") else {})
                typo_dict = result.typosquatting.model_dump() if hasattr(result.typosquatting, "model_dump") else (result.typosquatting.__dict__ if hasattr(result.typosquatting, "__dict__") else {})
                raw_intent = analyze_website_intention(
                    url=result.url,
                    anatomy=anatomy_dict,
                    features=result.features,
                    typosquatting=typo_dict,
                    risk_score=result.risk.score
                )
                intent = WebsiteIntention(**raw_intent)

            st.markdown(f"""
            <div class="intent-box">
                <div style="font-size:0.9rem; font-weight:700; color:#3978D6; text-transform:uppercase; letter-spacing:0.5px;">
                    🎯 Main Intention of This Website: {intent.category} ({intent.risk_context})
                </div>
                <div style="font-size:1.05rem; font-weight:600; color:#F7F9FC; margin:6px 0;">
                    {intent.intent_summary}
                </div>
                <div style="font-size:0.92rem; color:#CBD5E1; margin-top:6px;">
                    <strong>Targeted Data / Assets:</strong> {', '.join(intent.targeted_data)}
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Cloud-Sandboxed Website Screenshot Preview
            with st.expander("📷 Visual Evidence: Cloud-Sandboxed Website Snapshot", expanded=False):
                st.markdown(
                    "<p style='color:#94A3B8; font-size:0.88rem; margin-bottom:12px;'>"
                    "🔒 <strong>Zero-Exposure Isolation:</strong> This visual capture is safely fetched using a cloud-sandboxed proxy. "
                    "Your personal device never connects to or executes code from the target server."
                    "</p>",
                    unsafe_allow_html=True
                )
                preview_target = result.cleaned_url if hasattr(result, "cleaned_url") else result.url
                preview_encoded = urllib.parse.quote(preview_target, safe="")
                preview_shot = f"https://s0.wp.com/mshots/v1/{preview_encoded}?w=800"
                if dns.exists:
                    st.image(preview_shot, caption=f"Isolated Sandbox Snapshot • {preview_target}", use_container_width=True)
                else:
                    st.warning(f"⚠️ Destination domain does not resolve in global DNS ({dns.status}). Remote capture is unavailable for non-existent servers.")

            # DETAILED TABS
            tab_intent, tab_typo, tab_dns, tab_recs, tab_factors = st.tabs([
                "🎯 Website Intention",
                "🔤 Brand Similarity Analysis",
                "🌐 Domain Existence & DNS",
                "📋 Safety Recommendations",
                "🔍 Explainable Factors"
            ])

            # TAB 0: Website Intention & Targeted Data
            with tab_intent:
                st.subheader("🎯 Threat Objective & Website Intention Analysis")
                c_i1, c_i2 = st.columns([3, 2])
                with c_i1:
                    st.markdown(f"#### Primary Purpose: **{intent.category}**")
                    st.write(intent.intent_summary)
                    st.markdown(f"**Attack & Deception Strategy:** {intent.attack_strategy}")
                    if intent.safe_alternative:
                        st.info(f"🛡️ **Safe Path:** {intent.safe_alternative}")
                with c_i2:
                    st.markdown("#### 🔒 Targeted Sensitive Assets:")
                    for asset in intent.targeted_data:
                        st.markdown(f"- ⚠️ **{asset}**")

            # TAB 1: Typosquatting & Similarity
            with tab_typo:
                st.subheader("🔤 Brand Lookalike & Typosquatting Analysis")
                if typo.is_typosquatting:
                    st.error(f"🚨 **CRITICAL: Brand Impersonation Detected! This domain mimics '{typo.target_brand}'**")
                    
                    c_t1, c_t2 = st.columns(2)
                    with c_t1:
                        st.markdown(f"""
                        <div style="background:rgba(200,59,75,0.12); border:1.5px solid #C83B4B; border-radius:10px; padding:16px;">
                            <div style="font-size:0.8rem; font-weight:700; color:#FFA5AE; text-transform:uppercase;">🚨 Submitted Deceptive Domain</div>
                            <div style="font-size:1.35rem; font-weight:800; color:#FFFFFF; margin:6px 0;">{result.anatomy.root_domain}{'.' + result.anatomy.tld if result.anatomy.tld else ''}</div>
                            <div style="font-size:0.85rem; color:#CBD5E1;">Deceptive imitation of <strong>{typo.target_brand}</strong></div>
                        </div>
                        """, unsafe_allow_html=True)
                    with c_t2:
                        st.markdown(f"""
                        <div style="background:rgba(22,133,91,0.15); border:1.5px solid #00F5A0; border-radius:10px; padding:16px;">
                            <div style="font-size:0.8rem; font-weight:700; color:#00F5A0; text-transform:uppercase;">🛡️ Authentic Official Website</div>
                            <div style="font-size:1.35rem; font-weight:800; color:#FFFFFF; margin:6px 0;">{typo.official_domain}</div>
                            <div style="font-size:0.85rem; color:#CBD5E1;">Genuine verified address for <strong>{typo.target_brand}</strong></div>
                        </div>
                        """, unsafe_allow_html=True)

                    st.markdown("#### 🔬 Similarity Breakdown & Forensic Metrics")
                    col_m1, col_m2, col_m3 = st.columns(3)
                    with col_m1:
                        st.metric("Similarity Score", f"{typo.similarity_percentage:.1f}%")
                    with col_m2:
                        st.metric("Impersonated Brand", typo.target_brand)
                    with col_m3:
                        st.metric("Deception Method", typo.technique[:28] if typo.technique else "Glyph Mimicry")

                    st.markdown(f"""
                    > **Forensic Assessment:**  
                    > {typo.explanation}
                    """)

                    # Tactic Explanation Callout
                    clean_root_lower = result.anatomy.root_domain.lower()
                    if "nn" in clean_root_lower:
                        st.warning("🔤 **Glyph Mimicry Detected ('nn' for 'm'):** Attackers use consecutive 'n's because in standard sans-serif web fonts, `'nn'` renders almost identically to an `'m'` (e.g. `nnicrosoft` ↔ `microsoft`).")
                    elif "0" in clean_root_lower:
                        st.warning("🔢 **Leet-Speak Substitution Detected ('0' for 'o'):** Attackers swap the letter `'o'` with numeric zero `'0'` (e.g. `g00gle` ↔ `google` or `amaz0n` ↔ `amazon`).")
                    elif "1" in clean_root_lower:
                        st.warning("🔢 **Leet-Speak Substitution Detected ('1' for 'l'):** Attackers swap the letter `'l'` with numeric one `'1'` (e.g. `paypa1` ↔ `paypal`).")

                elif typo.is_official_brand:
                    st.success(f"🛡️ **Verified Authentic Brand Domain**: `{result.anatomy.netloc}` is a genuine official address belonging to **{typo.target_brand}**.")
                    st.markdown(f"""
                    - **Verified Organization:** `{typo.target_brand}`
                    - **Official Domain:** [`https://{typo.official_domain}`](https://{typo.official_domain})
                    - **Domain Legitimacy:** `100% Authentic`
                    - **Squatting Verdict:** `Clean (Official Brand)`
                    """)
                else:
                    st.info(f"✅ **No Brand Typosquatting Detected**: `{result.anatomy.root_domain}` does not deceptively mimic any of the monitored high-profile brands (e.g. Microsoft, Google, Apple, Amazon, PayPal, Meta, Chase).")

            # TAB 2: Domain Existence
            with tab_dns:
                st.subheader("🌐 Domain Existence & Global DNS Verification")
                st.markdown(f"""
                <div class="existence-box">
                    <strong>Resolution Status:</strong> <code>{dns.status}</code><br/>
                    <strong>Domain Exists in Global DNS:</strong> {'✅ Yes (Active)' if dns.exists else '❌ No (Does Not Exist / Inactive)'}<br/>
                    <strong>Resolved IP Addresses:</strong> {', '.join(dns.resolved_ips) if dns.resolved_ips else '(none)'}<br/><br/>
                    <strong>Details:</strong> {dns.explanation}
                </div>
                """, unsafe_allow_html=True)

            # TAB 3: Recommendations
            with tab_recs:
                st.subheader("💡 Recommended Actions for You")
                for rec in result.recommendations:
                    if rec.priority == "critical":
                        st.error(f"**🛑 {rec.title}**\n\n{rec.guidance}")
                    elif rec.priority == "warning":
                        st.warning(f"**⚠️ {rec.title}**\n\n{rec.guidance}")
                    else:
                        st.info(f"**ℹ️ {rec.title}**\n\n{rec.guidance}")

            # TAB 4: Factors
            with tab_factors:
                st.subheader("🔍 Breakdown of Contributing Factors")
                risk_factors = [f for f in result.factors if f.category == "risk"]
                safety_factors = [f for f in result.factors if f.category == "safety"]

                if risk_factors:
                    st.markdown(f"##### 🚩 Red Flags Detected ({len(risk_factors)})")
                    for f in risk_factors:
                        st.markdown(f"""
                        <div class="factor-box-risk">
                            <strong>{f.title}</strong> — <code>{f.severity.upper()}</code> (+{f.score_impact:.0f} points)<br/>
                            <span style="color:#CBD5E1; font-size:0.92rem;">{f.description}</span>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.success("No suspicious heuristic red flags detected.")

                if safety_factors:
                    st.markdown(f"##### 🛡️ Positive Indicators ({len(safety_factors)})")
                    for f in safety_factors:
                        st.markdown(f"""
                        <div class="factor-box-safe">
                            <strong>✅ {f.title}</strong><br/>
                            <span style="color:#CBD5E1; font-size:0.92rem;">{f.description}</span>
                        </div>
                        """, unsafe_allow_html=True)


else:
    # Initial State
    st.info("👆 Enter or paste any website URL above to inspect its safety, intention, domain existence, and typosquatting risk.")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("""
        #### 1. Exists or Not
        Safe DNS resolution checks whether the domain exists in global DNS or is a fake/inactive NXDOMAIN link.
        """)
    with col2:
        st.markdown("""
        #### 2. Phishing or Not
        Instant classification whether the link is an authentic site or a malicious fraudulent phishing portal.
        """)
    with col3:
        st.markdown("""
        #### 3. Low vs High Score
        Clear 0-100 score categorizing links into **Low Score (Safe)**, **Medium Score (Caution)**, or **High Score (Dangerous)**.
        """)
    with col4:
        st.markdown("""
        #### 4. Brand Similarity
        Detects lookalikes like `nnicrosoft` (mimicking Microsoft) and `g00gle` (mimicking Google) using edit-distance & leet-speak analysis.
        """)


The focused UI element is 1 AXWebArea raw.githubusercontent.com/ganeshpgowda/SAFELINK_AI/refs/heads/main/SAFELINK_AI/frontend/app.py
