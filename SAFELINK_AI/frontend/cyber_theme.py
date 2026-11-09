"""Cyberpunk Theme & Transparent 3D Rotating Earth Background for SafeLink AI.
Matches the dark cyber dashboard aesthetic from USER.CTRL.

Palette Enforcement:
- Background: Deep Cyber Canvas #080D15 with high-tech grid
- Headings & Accents: Navy #142B4A & Off-white #F7F9FC
- Links & Informational Callouts: Blue #3978D6
- Privacy & Safe States: Green #16855B & Neon Mint #00F5A0
- Check Button & Danger States: Red #C83B4B
"""

from pathlib import Path

# Load repeating world map SVG
SVG_FILE = Path(__file__).parent / "world_map_svg.txt"
if SVG_FILE.exists():
    with open(SVG_FILE, "r", encoding="utf-8") as f:
        WORLD_MAP_SVG_URI = f.read().strip()
else:
    WORLD_MAP_SVG_URI = ""

CYBER_CSS = f"""
<style>
    /* =========================================================================
       1. Cyberpunk Dark Base & Canvas Styling (#080D15)
       ========================================================================= */
    .stApp {{
        background-color: #080D15 !important;
        background-image: 
            radial-gradient(circle at 50% 12%, rgba(20, 43, 74, 0.45) 0%, transparent 65%),
            linear-gradient(rgba(0, 245, 160, 0.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 245, 160, 0.025) 1px, transparent 1px) !important;
        background-size: 100% 100%, 42px 42px, 42px 42px !important;
        color: #F7F9FC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }}

    [data-testid="stSidebar"] {{
        background-color: #0B111B !important;
        border-right: 1px solid rgba(57, 120, 214, 0.18) !important;
    }}

    [data-testid="stSidebar"] * {{
        color: #E2E8F0 !important;
    }}

    /* Global Headings & Typography */
    h1, h2, h3, h4, h5, h6 {{
        color: #F7F9FC !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px !important;
    }}
    p, span, label, div {{
        color: #CBD5E1;
    }}
    strong {{
        color: #F7F9FC !important;
    }}
    code {{
        background-color: #111A29 !important;
        color: #00F5A0 !important;
        border: 1px solid rgba(0, 245, 160, 0.25) !important;
        padding: 2px 7px !important;
        border-radius: 4px !important;
        font-size: 0.9em !important;
    }}

    /* =========================================================================
       2. Transparent 3D Rotating Earth Background Animation
       ========================================================================= */
    .cyber-earth-bg {{
        position: fixed;
        top: 52%;
        right: 4%;
        transform: translateY(-50%);
        width: 520px;
        height: 520px;
        pointer-events: none;
        z-index: 0;
        opacity: 0.26;
        transition: opacity 0.5s ease;
    }}

    @media (max-width: 1200px) {{
        .cyber-earth-bg {{
            right: 50%;
            transform: translate(50%, -50%);
            opacity: 0.15;
            width: 420px;
            height: 420px;
        }}
    }}

    .earth-sphere {{
        position: absolute;
        top: 10px;
        left: 10px;
        width: 500px;
        height: 500px;
        border-radius: 50%;
        background-image: 
            radial-gradient(circle at 32% 32%, rgba(0, 245, 160, 0.28) 0%, rgba(57, 120, 214, 0.18) 35%, rgba(13, 21, 34, 0.82) 72%, rgba(8, 13, 21, 0.98) 100%),
            url("data:image/svg+xml;utf-8,{WORLD_MAP_SVG_URI}");
        background-size: auto, 1000px 500px;
        background-repeat: no-repeat, repeat-x;
        animation: spinEarthContinuous 30s linear infinite;
        box-shadow: 
            inset -35px -25px 55px rgba(0, 0, 0, 0.95),
            inset 18px 18px 40px rgba(0, 245, 160, 0.35),
            0 0 50px rgba(0, 245, 160, 0.18),
            0 0 100px rgba(57, 120, 214, 0.16);
        border: 1.5px solid rgba(0, 245, 160, 0.35);
        overflow: hidden;
    }}

    .earth-atmosphere {{
        position: absolute;
        top: -15px;
        left: -15px;
        width: 550px;
        height: 550px;
        border-radius: 50%;
        background: radial-gradient(circle, rgba(0, 245, 160, 0.12) 58%, rgba(57, 120, 214, 0.10) 72%, transparent 84%);
        filter: blur(12px);
        pointer-events: none;
        animation: pulseAtmosphere 5s ease-in-out infinite alternate;
    }}

    .earth-orbital-ring {{
        position: absolute;
        top: 50%;
        left: 50%;
        width: 610px;
        height: 220px;
        margin-top: -110px;
        margin-left: -305px;
        border: 1.5px dashed rgba(0, 245, 160, 0.38);
        border-radius: 50%;
        transform: rotate(-24deg);
        pointer-events: none;
        animation: spinOrbit 45s linear infinite;
    }}

    .earth-orbital-ring-2 {{
        position: absolute;
        top: 50%;
        left: 50%;
        width: 570px;
        height: 180px;
        margin-top: -90px;
        margin-left: -285px;
        border: 1px solid rgba(57, 120, 214, 0.32);
        border-radius: 50%;
        transform: rotate(34deg);
        pointer-events: none;
    }}

    .earth-satellite {{
        position: absolute;
        top: -5px;
        left: 48%;
        width: 10px;
        height: 10px;
        background: #00F5A0;
        border-radius: 50%;
        box-shadow: 0 0 14px #00F5A0, 0 0 25px #00F5A0;
        animation: blinkNode 1.6s infinite ease-in-out;
    }}

    @keyframes spinEarthContinuous {{
        0% {{
            background-position: 0 0, 0 0;
        }}
        100% {{
            background-position: 0 0, 1000px 0;
        }}
    }}

    @keyframes pulseAtmosphere {{
        0% {{
            opacity: 0.7;
            transform: scale(0.98);
        }}
        100% {{
            opacity: 1;
            transform: scale(1.02);
        }}
    }}

    @keyframes spinOrbit {{
        0% {{
            transform: rotate(-24deg) rotateZ(0deg);
        }}
        100% {{
            transform: rotate(-24deg) rotateZ(360deg);
        }}
    }}

    @keyframes blinkNode {{
        0%, 100% {{
            opacity: 0.4;
            transform: scale(0.85);
        }}
        50% {{
            opacity: 1;
            transform: scale(1.25);
        }}
    }}

    /* =========================================================================
       3. Cyber Header & System Status (USER.CTRL Style)
       ========================================================================= */
    .cyber-header-wrapper {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 22px;
        padding-bottom: 14px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        animation: fadeInDown 0.6s ease;
    }}

    .cyber-brand-title {{
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "SF Pro Display", monospace !important;
        font-size: 2.35rem !important;
        font-weight: 900 !important;
        letter-spacing: 2px !important;
        background: linear-gradient(90deg, #00F5A0 0%, #00D2FF 70%, #3978D6 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 0 28px rgba(0, 245, 160, 0.35);
        display: inline-flex;
        align-items: center;
        gap: 12px;
        margin: 0;
        animation: cyberBlinkShake 0.20s infinite ease-in-out !important;
        will-change: transform, opacity;
    }}

    /* Rapid Cyber Blink and Shake every 0.20 seconds */
    @keyframes cyberBlinkShake {{
        0% {{
            transform: translate(0, 0);
            opacity: 1;
            filter: drop-shadow(0 0 12px rgba(0, 245, 160, 0.75));
        }}
        20% {{
            transform: translate(-2.5px, 1.5px);
            opacity: 0.35;
            filter: drop-shadow(-2px 0 6px #C83B4B) drop-shadow(2px 0 6px #00F5A0);
        }}
        40% {{
            transform: translate(2.5px, -1.5px);
            opacity: 0.95;
            filter: drop-shadow(2px -1px 8px #00D2FF);
        }}
        60% {{
            transform: translate(-1.5px, -1px);
            opacity: 0.25;
            filter: drop-shadow(0 0 20px rgba(0, 245, 160, 0.9));
        }}
        80% {{
            transform: translate(1.5px, 1.5px);
            opacity: 0.85;
            filter: drop-shadow(1px 1px 8px #00F5A0);
        }}
        100% {{
            transform: translate(0, 0);
            opacity: 1;
            filter: drop-shadow(0 0 12px rgba(0, 245, 160, 0.75));
        }}
    }}

    /* Snake Motion along an Invisible Straight Line (Up to 6cm) - Straight line does NOT appear */
    .cyber-snake-track {{
        position: relative;
        overflow: visible;
        width: 100%;
        max-width: 720px;
        height: 38px;
        margin-top: 6px;
        pointer-events: none;
        border: none !important;
        background: transparent !important;
        outline: none !important;
        box-shadow: none !important;
        text-decoration: none !important;
    }}

    .cyber-snake-tagline {{
        display: inline-flex;
        align-items: center;
        white-space: nowrap;
        font-size: 0.92rem;
        font-weight: 700;
        color: #00F5A0 !important;
        letter-spacing: 1.5px;
        text-shadow: 0 0 12px rgba(0, 245, 160, 0.65), 0 0 24px rgba(0, 245, 160, 0.3);
        animation: snakeSlitherLine 4.5s ease-in-out infinite alternate !important;
        will-change: transform;
    }}

    .snake-head {{
        margin-right: 8px;
        font-size: 1.05rem;
        display: inline-block;
        animation: snakeHiss 1.2s infinite ease-in-out;
    }}

    @keyframes snakeHiss {{
        0%, 100% {{
            transform: scale(1) rotate(0deg);
        }}
        50% {{
            transform: scale(1.18) rotate(-4deg);
        }}
    }}

    /* Straight Line Trajectory: Up to exactly 6cm with natural sinusoidal snake undulation */
    @keyframes snakeSlitherLine {{
        0% {{
            transform: translateX(0cm) translateY(0px) rotate(0deg) scaleX(1);
        }}
        12.5% {{
            transform: translateX(0.75cm) translateY(-3.5px) rotate(-1.8deg) scaleX(1.02);
        }}
        25% {{
            transform: translateX(1.5cm) translateY(0px) rotate(0deg) scaleX(0.98);
        }}
        37.5% {{
            transform: translateX(2.25cm) translateY(3.5px) rotate(1.8deg) scaleX(1.02);
        }}
        50% {{
            transform: translateX(3.0cm) translateY(0px) rotate(0deg) scaleX(0.98);
        }}
        62.5% {{
            transform: translateX(3.75cm) translateY(-3.5px) rotate(-1.8deg) scaleX(1.02);
        }}
        75% {{
            transform: translateX(4.5cm) translateY(0px) rotate(0deg) scaleX(0.98);
        }}
        87.5% {{
            transform: translateX(5.25cm) translateY(3.5px) rotate(1.8deg) scaleX(1.02);
        }}
        100% {{
            transform: translateX(6cm) translateY(0px) rotate(0deg) scaleX(1);
        }}
    }}

    .system-status-pill {{
        background: #0E1624;
        border: 1px solid rgba(0, 245, 160, 0.3);
        padding: 8px 16px;
        border-radius: 24px;
        display: flex;
        align-items: center;
        gap: 9px;
        font-size: 0.86rem;
        font-weight: 600;
        color: #E2E8F0 !important;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.4);
    }}

    .status-dot-pulse {{
        width: 9px;
        height: 9px;
        background-color: #00F5A0;
        border-radius: 50%;
        box-shadow: 0 0 10px #00F5A0, 0 0 18px #00F5A0;
        animation: pulseGreenGlow 2s infinite ease-in-out;
    }}

    /* =========================================================================
       4. Top 4 Cyber Metric Cards (Directly matching uploaded image)
       ========================================================================= */
    .cyber-metric-row {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 16px;
        margin-bottom: 24px;
        animation: fadeInUp 0.7s ease;
    }}

    @media (max-width: 900px) {{
        .cyber-metric-row {{
            grid-template-columns: repeat(2, 1fr);
        }}
    }}

    .cyber-metric-card {{
        background: rgba(13, 21, 34, 0.82);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 18px 22px;
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
        backdrop-filter: blur(10px);
        transition: transform 0.25s ease, border-color 0.25s ease;
    }}

    .cyber-metric-card:hover {{
        transform: translateY(-3px);
        border-color: rgba(0, 245, 160, 0.4);
        box-shadow: 0 8px 24px rgba(0, 245, 160, 0.12);
    }}

    .cyber-metric-label {{
        font-size: 0.76rem;
        font-weight: 700;
        color: #7088A5 !important;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-bottom: 6px;
    }}

    .cyber-metric-value {{
        font-size: 1.85rem;
        font-weight: 800;
        color: #F7F9FC !important;
        letter-spacing: -0.5px;
        line-height: 1.1;
        margin-bottom: 4px;
    }}

    .cyber-metric-sub {{
        font-size: 0.78rem;
        color: #4A607A !important;
        font-weight: 500;
    }}

    .cyber-metric-value.cyan {{
        color: #00F5A0 !important;
        text-shadow: 0 0 16px rgba(0, 245, 160, 0.35);
    }}

    .cyber-metric-value.blue {{
        color: #3978D6 !important;
        text-shadow: 0 0 16px rgba(57, 120, 214, 0.35);
    }}

    /* =========================================================================
       5. Privacy Badge (Green #16855B)
       ========================================================================= */
    .privacy-badge {{
        background: rgba(22, 133, 91, 0.12) !important;
        border: 1.5px solid #16855B !important;
        color: #E2E8F0 !important;
        padding: 14px 20px !important;
        border-radius: 10px !important;
        font-size: 0.94rem !important;
        margin-bottom: 22px !important;
        box-shadow: 0 4px 16px rgba(22, 133, 91, 0.15) !important;
        animation: pulseGreenBox 4s infinite ease-in-out;
    }}

    .privacy-badge strong {{
        color: #00F5A0 !important;
    }}

    /* =========================================================================
       6. Check Button (Red #C83B4B) & Search Input Styling
       ========================================================================= */
    div[data-baseweb="input"] {{
        background-color: #0D1522 !important;
        border: 1.5px solid rgba(255, 255, 255, 0.14) !important;
        border-radius: 10px !important;
        color: #F7F9FC !important;
        transition: all 0.25s ease !important;
    }}

    div[data-baseweb="input"]:focus-within {{
        border-color: #00F5A0 !important;
        box-shadow: 0 0 0 3px rgba(0, 245, 160, 0.22) !important;
    }}

    div[data-baseweb="input"] input {{
        color: #F7F9FC !important;
        font-size: 1rem !important;
    }}

    div.stButton > button[kind="primary"],
    button[data-testid="stBaseButton-primary"],
    .stButton > button:first-child {{
        background: linear-gradient(135deg, #C83B4B 0%, #A52837 100%) !important;
        color: #FFFFFF !important;
        border: 1px solid #E5485B !important;
        border-radius: 9px !important;
        padding: 10px 24px !important;
        font-weight: 700 !important;
        font-size: 1rem !important;
        letter-spacing: 0.4px !important;
        box-shadow: 0 4px 18px rgba(200, 59, 75, 0.4) !important;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1) !important;
    }}

    button[data-testid="stBaseButton-primary"]:hover,
    .stButton > button:first-child:hover {{
        background: linear-gradient(135deg, #E5485B 0%, #C83B4B 100%) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 24px rgba(200, 59, 75, 0.6) !important;
    }}

    button[data-testid="stBaseButton-primary"]:active,
    .stButton > button:first-child:active {{
        transform: translateY(0) !important;
    }}

    /* Secondary Buttons */
    div.stButton > button[kind="secondary"],
    button[data-testid="stBaseButton-secondary"] {{
        background: #0D1522 !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        color: #CBD5E1 !important;
        border-radius: 9px !important;
        transition: all 0.2s ease !important;
    }}
    button[data-testid="stBaseButton-secondary"]:hover {{
        border-color: #3978D6 !important;
        color: #F7F9FC !important;
    }}

    /* =========================================================================
       7. Links & Informational Callouts (Blue #3978D6)
       ========================================================================= */
    a, a:visited {{
        color: #3978D6 !important;
        font-weight: 600 !important;
        text-decoration: none !important;
        transition: color 0.2s ease !important;
    }}
    a:hover {{
        color: #60A5FA !important;
        text-decoration: underline !important;
    }}

    .intent-box {{
        background: rgba(13, 21, 34, 0.9) !important;
        border-left: 5px solid #3978D6 !important;
        border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
        margin: 16px 0 !important;
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.35) !important;
        animation: fadeInUp 0.5s ease;
    }}

    .existence-box {{
        background: rgba(13, 21, 34, 0.9) !important;
        border-left: 5px solid #3978D6 !important;
        border-radius: 10px !important;
        padding: 16px 20px !important;
        margin: 14px 0 !important;
        border-top: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08) !important;
    }}

    /* =========================================================================
       8. Danger & Typosquatting States (Red #C83B4B)
       ========================================================================= */
    .typo-alert-box {{
        background: rgba(200, 59, 75, 0.12) !important;
        border: 2px solid #C83B4B !important;
        border-radius: 12px !important;
        padding: 20px 24px !important;
        margin: 18px 0 !important;
        box-shadow: 0 4px 24px rgba(200, 59, 75, 0.3) !important;
        animation: pulseDanger 2.5s infinite ease-in-out;
    }}

    .factor-box-risk {{
        background: rgba(200, 59, 75, 0.1) !important;
        border-left: 4px solid #C83B4B !important;
        border-radius: 6px !important;
        padding: 12px 16px !important;
        margin-bottom: 10px !important;
    }}

    .factor-box-safe {{
        background: rgba(22, 133, 91, 0.12) !important;
        border-left: 4px solid #16855B !important;
        border-radius: 6px !important;
        padding: 12px 16px !important;
        margin-bottom: 10px !important;
    }}

    /* Badges */
    .badge-pill-danger {{
        background-color: rgba(200, 59, 75, 0.2) !important;
        border: 1px solid #C83B4B !important;
        color: #FFA5AE !important;
        font-weight: 700 !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 0.88rem !important;
        display: inline-block !important;
        text-shadow: 0 0 10px rgba(200, 59, 75, 0.5) !important;
    }}

    .badge-pill-warning {{
        background-color: rgba(217, 119, 6, 0.2) !important;
        border: 1px solid #D97706 !important;
        color: #FCD34D !important;
        font-weight: 700 !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 0.88rem !important;
        display: inline-block !important;
    }}

    .badge-pill-success {{
        background-color: rgba(22, 133, 91, 0.22) !important;
        border: 1px solid #00F5A0 !important;
        color: #00F5A0 !important;
        font-weight: 700 !important;
        padding: 6px 14px !important;
        border-radius: 20px !important;
        font-size: 0.88rem !important;
        display: inline-block !important;
        text-shadow: 0 0 10px rgba(0, 245, 160, 0.5) !important;
    }}

    /* Tabs Styling */
    button[data-baseweb="tab"] {{
        color: #94A3B8 !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        padding: 10px 18px !important;
        border-radius: 6px 6px 0 0 !important;
        transition: all 0.2s ease !important;
    }}
    button[data-baseweb="tab"]:hover {{
        color: #F7F9FC !important;
        background-color: rgba(255, 255, 255, 0.04) !important;
    }}
    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #00F5A0 !important;
        border-bottom-color: #00F5A0 !important;
        background-color: rgba(0, 245, 160, 0.08) !important;
    }}

    /* Tables & Dataframes */
    [data-testid="stDataFrame"] {{
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        overflow: hidden !important;
    }}

    /* Keyframe Animations */
    @keyframes fadeInDown {{
        from {{
            opacity: 0;
            transform: translateY(-16px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes fadeInUp {{
        from {{
            opacity: 0;
            transform: translateY(16px);
        }}
        to {{
            opacity: 1;
            transform: translateY(0);
        }}
    }}

    @keyframes pulseGreenGlow {{
        0%, 100% {{
            box-shadow: 0 0 6px #00F5A0, 0 0 12px #00F5A0;
        }}
        50% {{
            box-shadow: 0 0 14px #00F5A0, 0 0 24px #00F5A0;
        }}
    }}

    @keyframes pulseGreenBox {{
        0%, 100% {{
            box-shadow: 0 4px 16px rgba(22, 133, 91, 0.15);
            border-color: #16855B;
        }}
        50% {{
            box-shadow: 0 6px 22px rgba(0, 245, 160, 0.25);
            border-color: #00F5A0;
        }}
    }}

    @keyframes pulseDanger {{
        0%, 100% {{
            box-shadow: 0 4px 18px rgba(200, 59, 75, 0.2);
            border-color: #C83B4B;
        }}
        50% {{
            box-shadow: 0 8px 30px rgba(200, 59, 75, 0.45);
            border-color: #E5485B;
        }}
    }}
</style>
"""


def get_cyber_earth_background_html() -> str:
    """Returns the HTML markup for the transparent 3D rotating earth background."""
    return """
    <div class="cyber-earth-bg">
        <div class="earth-atmosphere"></div>
        <div class="earth-sphere"></div>
        <div class="earth-orbital-ring">
            <div class="earth-satellite"></div>
        </div>
        <div class="earth-orbital-ring-2"></div>
    </div>
    """


def get_cyber_header_html() -> str:
    """Returns the top cyber navigation header matching USER.CTRL style with snake slither animation."""
    return """
    <div class="cyber-header-wrapper">
        <div>
            <div class="cyber-brand-title">
                <span>🛡️</span> SAFELINK.AI
            </div>
            <div class="cyber-snake-track">
                <div class="cyber-snake-tagline">
                    <span class="snake-head">🐍</span> DON'T CLICK BLINDLY. CHECK BEFORE YOU TRUST.
                </div>
            </div>
        </div>
        <div class="system-status-pill">
            <span class="status-dot-pulse"></span>
            <span>System Online</span>
        </div>
    </div>
    """


def get_cyber_metric_cards_html() -> str:
    """Returns the top 4 cyber status metric cards inspired by the uploaded image."""
    return """
    <div class="cyber-metric-row">
        <div class="cyber-metric-card">
            <div class="cyber-metric-label">TOTAL PROTECTED</div>
            <div class="cyber-metric-value">3,510+</div>
            <div class="cyber-metric-sub">DATABASE VERIFIED</div>
        </div>
        <div class="cyber-metric-card">
            <div class="cyber-metric-label">FRAUD SHIELD</div>
            <div class="cyber-metric-value cyan">ACTIVE</div>
            <div class="cyber-metric-sub">AI RANDOM FOREST</div>
        </div>
        <div class="cyber-metric-card">
            <div class="cyber-metric-label">DNS RADAR</div>
            <div class="cyber-metric-value blue">REAL-TIME</div>
            <div class="cyber-metric-sub">NXDOMAIN VERIFIER</div>
        </div>
        <div class="cyber-metric-card">
            <div class="cyber-metric-label">MODEL ACCURACY</div>
            <div class="cyber-metric-value cyan">100%</div>
            <div class="cyber-metric-sub">OFFLINE PRIVACY ENGINE</div>
        </div>
    </div>
    """

