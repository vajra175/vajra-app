"""
================================================================================
VEDICQUANT PARAMA-VAJRA (ANANTA-216): SUPREME FRONTEND TERMINAL & UI (app.py)
================================================================================
Bloomberg-Class Cyber-Vedic UI | Mobile PWA Home-Screen Icon & Manifest
Plotly GrandVisualEngine (Candlesticks, 12-Pillar Spider, Treemap, Monte Carlo)
8-Tab Interactive Command Center | AI Quant Copilot | 6-Sheet Excel Export
================================================================================
"""

import datetime
import re
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import yfinance as yf

from engine import (
    VAJRA_PIL_ICON,
    VAJRA_ICON_URI,
    build_vajra_app_icon,
    DB_FILE,
    CORPORATE_SPLIT_REGISTRY,
    FORENSIC_VETO_REGISTRY,
    SECTOR_DEFAULT_MAP,
    NSE_RADAR_UNIVERSE,
    reconcile_corporate_action,
    init_db,
    get_holdings,
    get_all_profiles_holdings,
    get_trade_ledger,
    save_holding_direct,
    execute_buy_order,
    execute_sell_order,
    export_all_vaults_json,
    restore_vaults_from_json,
    parse_raw_broker_holdings_text,
    get_ist_now,
    get_live_vedic_chronometer,
    compute_216_variable_codex,
    scan_radar_universe_216,
    batch_fetch_live_prices,
    generate_autonomous_rebalance_tickets,
    generate_deterministic_copilot_response,
    query_optional_llm_api,
    sanitize_sheet_name,
    build_ananta216_excel_dossier,
)

# ------------------------------------------------------------------------------
# 1. CUSTOM BRANDED ICON, PWA MANIFEST & CYBER-VEDIC TERMINAL UI
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="ANANTA-216 | Parama-Vajra Sovereign Terminal",
    page_icon=VAJRA_PIL_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    f"""
<head>
    <title>ANANTA-216 Sovereign</title>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    <meta name="apple-mobile-web-app-title" content="ANANTA-216">
    <meta name="mobile-web-app-capable" content="yes">
    <meta name="application-name" content="ANANTA-216">
    <meta name="theme-color" content="#050811">
    <link rel="icon" type="image/png" href="{VAJRA_ICON_URI}">
    <link rel="apple-touch-icon" href="{VAJRA_ICON_URI}">
</head>
<style>
    .stApp {{
        background-color: #050811;
        background-image:
            radial-gradient(circle at 10% 10%, rgba(124, 58, 237, 0.13) 0%, transparent 38%),
            radial-gradient(circle at 90% 15%, rgba(14, 165, 233, 0.10) 0%, transparent 38%),
            radial-gradient(circle at 50% 90%, rgba(16, 185, 129, 0.08) 0%, transparent 45%);
        color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }}
    .command-ribbon {{
        background: linear-gradient(90deg, rgba(15, 23, 42, 0.95) 0%, rgba(30, 27, 75, 0.90) 50%, rgba(15, 23, 42, 0.95) 100%);
        border: 1px solid rgba(148, 163, 184, 0.18);
        border-radius: 10px;
        padding: 10px 16px;
        margin-bottom: 12px;
        display: flex;
        flex-wrap: wrap;
        justify-content: space-between;
        align-items: center;
        gap: 10px;
        font-size: 12.5px;
    }}
    .ribbon-pill {{
        background: rgba(2, 6, 23, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 5px 11px;
        border-radius: 8px;
        display: inline-block;
    }}
    .glass-card {{
        background: rgba(15, 23, 42, 0.82);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        padding: 16px 20px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.09);
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.45);
        margin-bottom: 14px;
    }}
    .muhurta-live-banner {{
        background: linear-gradient(135deg, rgba(46, 16, 101, 0.90), rgba(15, 23, 42, 0.88));
        border: 1px solid rgba(168, 85, 247, 0.42);
        color: #F5F3FF;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 5px solid #A855F7;
        margin-bottom: 14px;
        box-shadow: 0 4px 24px rgba(168, 85, 247, 0.18);
    }}
    .rahu-alert-banner {{
        background: linear-gradient(135deg, rgba(127, 29, 29, 0.90), rgba(30, 10, 15, 0.88));
        border: 1px solid rgba(248, 113, 113, 0.50);
        color: #FEF2F2;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 5px solid #EF4444;
        margin-bottom: 14px;
    }}
    .badge-buy {{
        background: rgba(6, 95, 70, 0.90);
        color: #6EE7B7;
        border: 1px solid #10B981;
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
    }}
    .badge-veto {{
        background: rgba(136, 19, 55, 0.90);
        color: #FECDD3;
        border: 1px solid #F43F5E;
        padding: 4px 12px;
        border-radius: 999px;
        font-weight: 700;
        font-size: 12px;
        display: inline-block;
    }}
    .status-pulse {{
        display: inline-block;
        width: 9px;
        height: 9px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 10px #10B981;
        margin-right: 6px;
    }}
    div[data-testid="stMetric"] {{
        background: linear-gradient(145deg, rgba(15, 23, 42, 0.85), rgba(30, 41, 59, 0.55));
        border: 1px solid rgba(148, 163, 184, 0.14);
        padding: 12px 15px;
        border-radius: 11px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.25);
    }}
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    header[data-testid="stHeader"] {{background: transparent;}}
</style>
""",
    unsafe_allow_html=True,
)


# ------------------------------------------------------------------------------
# 9. PLOTLY SUPREME VISUAL ENGINE (CANDLES, RADAR SPIDER, TREEMAP, MONTE CARLO)
# ------------------------------------------------------------------------------
class GrandVisualEngine:

    @staticmethod
    def create_market_mood_gauge(score: float = 52.4) -> go.Figure:
        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "<b>MARKET MOOD INDEX (MMI)</b>", "font": {"size": 13, "color": "#F8FAFC"}},
                number={"font": {"size": 32, "color": "#F8FAFC"}},
                gauge={
                    "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#475569"},
                    "bar": {"color": "#A855F7", "thickness": 0.28},
                    "bgcolor": "rgba(0,0,0,0)",
                    "steps": [
                        {"range": [0, 25], "color": "#7F1D1D"},
                        {"range": [25, 45], "color": "#9A3412"},
                        {"range": [45, 55], "color": "#1E3A8A"},
                        {"range": [55, 75], "color": "#065F46"},
                        {"range": [75, 100], "color": "#047857"},
                    ],
                    "threshold": {"line": {"color": "#38BDF8", "width": 4}, "thickness": 0.82, "value": score},
                },
            )
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=205,
            margin=dict(l=20, r=20, t=35, b=10),
        )
        return fig

    @staticmethod
    def create_pillar_spider_radar(pillar_scores: Dict[str, float], sym: str) -> go.Figure:
        categories = list(pillar_scores.keys())
        values = list(pillar_scores.values())
        categories_closed = categories + [categories[0]]
        values_closed = values + [values[0]]

        fig = go.Figure(
            data=go.Scatterpolar(
                r=values_closed,
                theta=categories_closed,
                fill="toself",
                fillcolor="rgba(168, 85, 247, 0.25)",
                line=dict(color="#38BDF8", width=2.2),
                marker=dict(size=6, color="#10B981"),
                name=sym,
            )
        )
        fig.update_layout(
            title=dict(text=f"<b>{sym} 12-PILLAR MULTI-FACTOR RADAR</b>", font=dict(size=12, color="#F8FAFC")),
            polar=dict(
                bgcolor="rgba(15, 23, 42, 0.65)",
                radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=9, color="#94A3B8")),
                angularaxis=dict(gridcolor="rgba(255,255,255,0.08)", tickfont=dict(size=10, color="#E2E8F0")),
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=35, r=35, t=42, b=20),
            showlegend=False,
        )
        return fig

    @staticmethod
    def create_advanced_technical_chart(
        df_hist: pd.DataFrame,
        sym: str,
        buy_zone_low: float,
        buy_zone_high: float,
        stop_loss: float,
        target: float,
        poc_price: float,
        use_candles: bool = True,
    ) -> go.Figure:
        df = df_hist.dropna(subset=["Close", "High", "Low", "Open"]).copy()
        close = df["Close"]
        ema20 = close.ewm(span=20, adjust=False).mean()
        ema50 = close.ewm(span=50, adjust=False).mean()
        ema200 = close.ewm(span=200, adjust=False).mean()

        delta = close.diff()
        gain = delta.clip(lower=0.0).ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
        loss = (-delta.clip(upper=0.0)).ewm(alpha=1 / 14, min_periods=14, adjust=False).mean()
        rs = gain / loss.replace(0, np.nan)
        rsi_series = 100.0 - (100.0 / (1.0 + rs))

        fig = make_subplots(
            rows=2,
            cols=1,
            shared_xaxes=True,
            vertical_spacing=0.06,
            row_heights=[0.73, 0.27],
            subplot_titles=(
                f"<b>{sym} ANANTA-216 ACTION ZONES, 20D POC & EMA STRUCTURE</b>",
                "<b>WILDER'S RSI (14) MOMENTUM OSCILLATOR</b>",
            ),
        )

        if use_candles:
            fig.add_trace(
                go.Candlestick(
                    x=df.index,
                    open=df["Open"],
                    high=df["High"],
                    low=df["Low"],
                    close=df["Close"],
                    name="OHLC",
                    increasing_line_color="#10B981",
                    decreasing_line_color="#EF4444",
                ),
                row=1,
                col=1,
            )
        else:
            fig.add_trace(
                go.Scatter(x=df.index, y=df["Close"], mode="lines", name="LTP", line=dict(color="#38BDF8", width=2.5)),
                row=1,
                col=1,
            )

        fig.add_trace(
            go.Scatter(x=df.index, y=ema20, mode="lines", name="EMA 20", line=dict(color="#F59E0B", width=1.5, dash="dot")),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(x=df.index, y=ema50, mode="lines", name="EMA 50", line=dict(color="#EC4899", width=1.5, dash="dash")),
            row=1,
            col=1,
        )
        fig.add_trace(
            go.Scatter(x=df.index, y=ema200, mode="lines", name="EMA 200", line=dict(color="#A855F7", width=1.6)),
            row=1,
            col=1,
        )

        fig.add_hrect(
            y0=buy_zone_low,
            y1=buy_zone_high,
            fillcolor="#10B981",
            opacity=0.16,
            line_width=0,
            annotation_text="BUY / ACCUMULATION ZONE",
            annotation_position="top left",
            annotation_font_color="#34D399",
            row=1,
            col=1,
        )
        fig.add_hline(
            y=poc_price,
            line_width=1.4,
            line_dash="dot",
            line_color="#38BDF8",
            annotation_text=f"20D POC (₹{poc_price:,.1f})",
            annotation_position="bottom left",
            annotation_font_color="#38BDF8",
            row=1,
            col=1,
        )
        fig.add_hline(
            y=stop_loss,
            line_width=1.8,
            line_dash="dash",
            line_color="#EF4444",
            annotation_text=f"2.2x ATR STOP (₹{stop_loss:,.1f})",
            annotation_position="bottom right",
            annotation_font_color="#F87171",
            row=1,
            col=1,
        )
        fig.add_hline(
            y=target,
            line_width=1.8,
            line_dash="dash",
            line_color="#10B981",
            annotation_text=f"TARGET (₹{target:,.1f})",
            annotation_position="top right",
            annotation_font_color="#34D399",
            row=1,
            col=1,
        )

        fig.add_trace(
            go.Scatter(x=df.index, y=rsi_series, mode="lines", name="RSI (14)", line=dict(color="#38BDF8", width=1.8)),
            row=2,
            col=1,
        )
        fig.add_hline(y=70, line_dash="dot", line_color="#EF4444", line_width=1, row=2, col=1)
        fig.add_hline(y=50, line_dash="dot", line_color="#64748B", line_width=1, row=2, col=1)
        fig.add_hline(y=30, line_dash="dot", line_color="#10B981", line_width=1, row=2, col=1)

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.55)",
            xaxis_rangeslider_visible=False,
            height=460,
            margin=dict(l=12, r=12, t=38, b=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.03,
                xanchor="right",
                x=1,
                font=dict(size=10, color="#CBD5E1"),
            ),
        )
        fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8")
        fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8", row=1, col=1)
        fig.update_yaxes(range=[15, 85], showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8", row=2, col=1)
        return fig

    @staticmethod
    def create_sector_donut_chart(df_holdings: pd.DataFrame) -> Optional[go.Figure]:
        if df_holdings.empty or "Sector" not in df_holdings.columns:
            return None
        sector_agg = df_holdings.groupby("Sector", as_index=False)["Market Value"].sum().sort_values(by="Market Value", ascending=False)
        palette = ["#8B5CF6", "#38BDF8", "#10B981", "#F59E0B", "#EC4899", "#6366F1", "#14B8A6", "#F43F5E", "#84CC16", "#06B6D4"]
        fig = px.pie(sector_agg, names="Sector", values="Market Value", hole=0.58, color_discrete_sequence=palette)
        fig.update_traces(textinfo="percent+label", textfont_size=10, marker=dict(line=dict(color="#050811", width=2)))
        fig.update_layout(
            title="<b>SECTOR ALLOCATION (STRICT 20.0% CAP)</b>",
            title_font=dict(size=12, color="#F8FAFC"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=290,
            margin=dict(l=10, r=10, t=35, b=10),
            showlegend=False,
        )
        return fig

    @staticmethod
    def create_portfolio_treemap(df_holdings: pd.DataFrame) -> Optional[go.Figure]:
        if df_holdings.empty:
            return None
        df_tree = df_holdings.copy()
        df_tree["Market Value"] = df_tree["Market Value"].clip(lower=1.0)
        fig = px.treemap(
            df_tree,
            path=[px.Constant("Sovereign Vault"), "Sector", "Symbol"],
            values="Market Value",
            color="P&L %",
            color_continuous_scale=["#991B1B", "#1E293B", "#059669", "#10B981"],
            color_continuous_midpoint=0.0,
        )
        fig.update_layout(
            title="<b>PORTFOLIO CAPITAL HEATMAP (SIZE = MARKET VALUE | COLOR = P&L %)</b>",
            title_font=dict(size=12, color="#F8FAFC"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=340,
            margin=dict(l=8, r=8, t=35, b=8),
        )
        return fig

    @staticmethod
    def create_monte_carlo_fan_chart(start_equity: float, drift_cagr: float = 0.185, ann_vol: float = 0.165) -> Tuple[go.Figure, Dict[str, float]]:
        """Simulates 1,000 Jump-Diffusion Monte Carlo portfolio paths over 252 trading days (1 Year)."""
        rng = np.random.default_rng(216)
        n_paths = 1000
        n_days = 252
        dt = 1.0 / n_days
        daily_shocks = rng.normal((drift_cagr - 0.5 * ann_vol ** 2) * dt, ann_vol * math.sqrt(dt), size=(n_paths, n_days))
        # Add rare Poisson jump shocks (Taleb Black Swan Stress)
        jumps = (rng.random(size=(n_paths, n_days)) < 0.003) * rng.normal(-0.035, 0.025, size=(n_paths, n_days))
        log_paths = np.cumsum(daily_shocks + jumps, axis=1)
        eq_paths = start_equity * np.exp(log_paths)

        p5 = np.percentile(eq_paths, 5, axis=0)
        p25 = np.percentile(eq_paths, 25, axis=0)
        p50 = np.percentile(eq_paths, 50, axis=0)
        p75 = np.percentile(eq_paths, 75, axis=0)
        p95 = np.percentile(eq_paths, 95, axis=0)
        days_x = list(range(1, n_days + 1))

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=days_x, y=p95, mode="lines", name="95th Percentile (Bull Convexity)", line=dict(color="#10B981", width=1.5, dash="dot")))
        fig.add_trace(go.Scatter(x=days_x, y=p75, mode="lines", name="75th Percentile", line=dict(color="#34D399", width=1), fill="tonexty", fillcolor="rgba(16, 185, 129, 0.08)"))
        fig.add_trace(go.Scatter(x=days_x, y=p50, mode="lines", name="Median Sovereign Trajectory", line=dict(color="#38BDF8", width=2.6)))
        fig.add_trace(go.Scatter(x=days_x, y=p25, mode="lines", name="25th Percentile", line=dict(color="#F59E0B", width=1), fill="tonexty", fillcolor="rgba(56, 189, 248, 0.08)"))
        fig.add_trace(go.Scatter(x=days_x, y=p5, mode="lines", name="5th Percentile (95% VaR Floor)", line=dict(color="#EF4444", width=1.6, dash="dash")))

        fig.update_layout(
            title="<b>1,000-PATH MONTE CARLO JUMP-DIFFUSION CONE (1-YEAR FORWARD EQUITY PROJECTION)</b>",
            title_font=dict(size=12, color="#F8FAFC"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.55)",
            xaxis_title="Forward Trading Days (252D = 1 Year)",
            yaxis_title="Projected Portfolio Value (₹)",
            height=330,
            margin=dict(l=12, r=12, t=38, b=12),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(size=10, color="#CBD5E1"),
            ),
        )
        fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8")
        fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8")

        terminal_vals = eq_paths[:, -1]
        var_95_loss = max(start_equity - float(p5[-1]), 0.0)
        tail_losses = start_equity - terminal_vals[terminal_vals <= p5[-1]]
        cvar_95_loss = float(np.mean(tail_losses)) if len(tail_losses) > 0 else var_95_loss * 1.25

        stats = {
            "median_1y": float(p50[-1]),
            "bull_95_1y": float(p95[-1]),
            "floor_5_1y": float(p5[-1]),
            "var_95_inr": var_95_inr if (var_95_inr := round(var_95_loss, 0)) >= 0 else 0.0,
            "cvar_95_inr": round(max(cvar_95_loss, 0.0), 0),
        }
        return fig, stats



# ------------------------------------------------------------------------------
# 12. MASTER APPLICATION HEADER, COMMAND RIBBON & NAVIGATION
# ------------------------------------------------------------------------------
vedic = get_live_vedic_chronometer()

col_h1, col_h2 = st.columns([2.3, 1.2])
with col_h1:
    st.title("⚡ VEDICQUANT PARAMA-VAJRA (ANANTA-216)")
    st.caption("12-Pillar 216-Variable Sovereign Alpha Engine • Autonomous Rebalancer • Saptarshi Vedic Chronometer")
with col_h2:
    st.markdown(
        f"""
        <div style="text-align:right; padding-top:10px;">
            <span class="status-pulse"></span><b>{vedic['mkt_session']}</b><br>
            <span style="font-size:12px; color:#94A3B8;">{vedic['date']} | {vedic['day']} | {vedic['time_ist']}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Global Macro & Vedic Telemetry Command Ribbon
st.markdown(
    f"""
    <div class="command-ribbon">
        <span class="ribbon-pill"><b>🇮🇳 RBI Repo:</b> 6.25% (Neutral)</span>
        <span class="ribbon-pill"><b>📈 10Y G-Sec:</b> 6.78% (+36 bps Spread)</span>
        <span class="ribbon-pill"><b>🛢️ Brent Crude:</b> $74.80/bbl</span>
        <span class="ribbon-pill"><b>💵 DXY Index:</b> 103.40</span>
        <span class="ribbon-pill"><b>☀️ Nirayana Sun/Moon:</b> {vedic['sidereal_sun']}° / {vedic['sidereal_moon']}°</span>
        <span class="ribbon-pill"><b>🧭 Prashna Lagna:</b> {vedic['prashna_lagna']}</span>
        <span class="ribbon-pill"><b>⚡ Kala Shuddhi:</b> {vedic['kala_shuddhi_score']}/100</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="{vedic['banner_class']}">
        <b>🕉️ Live Abhijit Muhurta:</b> {vedic['abhijit']} &nbsp;|&nbsp;
        <b>⚠️ Rahu Kaalam:</b> {vedic['rahu']} &nbsp;|&nbsp;
        <b>Yamaganda:</b> {vedic['yamaganda']} &nbsp;|&nbsp;
        <b>Choghadiya:</b> {vedic['choghadiya']}<br>
        <b>Execution Gate:</b> {vedic['rahu_status']}
    </div>
    """,
    unsafe_allow_html=True,
)

ctrl1, ctrl2, ctrl3 = st.columns([1.6, 1.2, 1.2])
profile_list = ["Self - Primary", "Family Member 1", "Family Member 2", "Family Trust"]
with ctrl1:
    active_profile = st.selectbox("Active Multi-Family Office Vault Profile:", profile_list, index=0)
with ctrl2:
    acct_equity_base = st.number_input(
        "Reference Portfolio Equity (₹):",
        min_value=100000.0,
        value=2500000.0,
        step=100000.0,
        help="Used for Fractional Kelly Position Sizing, 1% Risk-Per-Trade, and Autonomous Rebalancing Order Tickets.",
    )
with ctrl3:
    risk_per_trade_pct = st.slider("Max Risk Per Trade (% of Equity):", 0.25, 2.50, 1.00, 0.25)

with st.spinner("Executing Vectorized 216-Variable NSE Radar Sweep..."):
    df_rad, macro_telemetry = scan_radar_universe_216(vedic)

live_mmi = macro_telemetry.get("mmi", 52.4)

# Pre-build Active Vault Valuation with ACAR Corporate Action Split Immunity
df_held_raw = get_holdings(active_profile)
df_vault_disp = pd.DataFrame()
acar_alerts: List[str] = []

if not df_held_raw.empty:
    held_syms = tuple(df_held_raw["symbol"].unique().tolist())
    live_price_map = batch_fetch_live_prices(held_syms)
    vault_rows = []
    tot_cost = 0.0
    tot_val = 0.0

    for _, row in df_held_raw.iterrows():
        sym = row["symbol"]
        raw_sh = float(row["shares"])
        raw_cost = float(row["avg_cost"])
        sec = row["sector"]

        cmp_live, chg_1d = live_price_map.get(sym, (raw_cost, 0.0))
        adj_sh, adj_cost, was_reconciled, acar_note = reconcile_corporate_action(sym, raw_sh, raw_cost, cmp_live)
        if was_reconciled:
            acar_alerts.append(f"`{sym}`: {acar_note}")
            save_holding_direct(active_profile, sym, adj_sh, adj_cost, sec)

        c_basis = adj_sh * adj_cost
        m_val = adj_sh * cmp_live
        tot_cost += c_basis
        tot_val += m_val

        vault_rows.append(
            {
                "Symbol": sym,
                "Sector": sec,
                "Shares": adj_sh,
                "Buy Price": round(adj_cost, 2),
                "Live CMP": round(cmp_live, 2),
                "1D Change %": chg_1d,
                "Cost Basis": round(c_basis, 2),
                "Market Value": round(m_val, 2),
                "P&L (₹)": round(m_val - c_basis, 2),
                "P&L %": round(((m_val - c_basis) / c_basis) * 100.0, 2) if c_basis > 0 else 0.0,
                "ACAR Note": acar_note,
            }
        )

    df_vault_disp = pd.DataFrame(vault_rows)
    df_vault_disp["Weight %"] = round((df_vault_disp["Market Value"] / tot_val) * 100.0, 2) if tot_val > 0 else 0.0
    df_vault_disp = df_vault_disp.sort_values(by="Market Value", ascending=False).reset_index(drop=True)

tab_radar, tab_scanner, tab_codex, tab_vault, tab_rebalance, tab_copilot, tab_trade, tab_export = st.tabs(
    [
        "🌐 Market Radar",
        "🔍 Visual Terminal & Radar",
        "🧬 216-Variable Codex",
        f"💼 {active_profile} Vault & NLP",
        "🎯 Rebalancer & Stress Lab",
        "💬 AI Quant Copilot",
        "⚙️ Trade Desk",
        "📥 Cloud Backup & 6-Sheet Dossier",
    ]
)

# ==============================================================================
# TAB 1: AUTONOMOUS BROADER MARKET RADAR (OUTSIDE PORTFOLIO)
# ==============================================================================
with tab_radar:
    st.subheader("📡 Autonomous Broader Market Radar (39 Liquid NSE Sector Bellwethers)")
    col_g1, col_g2 = st.columns([1, 1.6])
    with col_g1:
        st.plotly_chart(GrandVisualEngine.create_market_mood_gauge(live_mmi), use_container_width=True)
    with col_g2:
        pct_above_50 = round((df_rad["CMP (₹)"] > df_rad["EMA 50"]).mean() * 100.0, 1) if not df_rad.empty else 50.0
        mean_rsi = round(df_rad["RSI (14)"].mean(), 1) if not df_rad.empty else 50.0
        strong_buys_cnt = int((df_rad["Verdict"] == "🟢 STRONG BUY").sum()) if not df_rad.empty else 0
        st.markdown(
            f"""
            <div class="glass-card" style="margin-top:8px;">
                <b>Principle-1 Gatekeeper & Macro Breadth Telemetry:</b><br>
                • <b>Market Mood Index (MMI):</b> <b>{live_mmi:.1f} / 100</b> | <b>NSE Leaders &gt; 50D EMA:</b> <b>{pct_above_50}%</b> | <b>Mean RSI:</b> <b>{mean_rsi}</b> | <b>Active Breakouts:</b> <b>{strong_buys_cnt}</b><br>
                • <b>Fundamental Gatekeeper Rule:</b> Any stock with Beneish M-Score &gt; -1.78, Sloan Accruals &gt; 10%, Promoter Pledge &gt; 20%, or Negative Owner Earnings is capped at <b>⛔ REDUCE / EXIT (0.0% Kelly Weight)</b>.<br>
                • <b>Dalio Macro Season:</b> Reflation / Sovereign Capex Expansion | <b>Taleb Barbell Base:</b> 85% Safe Vault / 15% Convex Alpha.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if not df_rad.empty:
        top5_buys = df_rad[~df_rad["Hard Veto"]].sort_values(by="ANANTA-216 Score", ascending=False).head(5)
        top5_vetoes = df_rad.sort_values(by="ANANTA-216 Score", ascending=True).head(5)

        st.markdown("#### 🟢 TOP 5 INSTITUTIONAL BUYS IN THE MARKET (RIGHT NOW)")
        st.dataframe(
            top5_buys[
                [
                    "Symbol", "Sector", "CMP (₹)", "Change %", "ANANTA-216 Score", "ROIC %",
                    "Piotroski F", "Buy Zone", "Stop-Loss (₹)", "Target (₹)", "R:R", "Kelly Weight %", "Verdict",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### 🔴 TOP 5 FORENSIC AVOID / EXIT SIGNALS (PRINCIPLE-1 GATEKEEPER VETOES)")
        st.dataframe(
            top5_vetoes[
                [
                    "Symbol", "Sector", "CMP (₹)", "Change %", "ANANTA-216 Score",
                    "Beneish M", "Sloan Accrual %", "Verdict", "Forensic Note",
                ]
            ],
            use_container_width=True,
            hide_index=True,
        )

        with st.expander("📊 Expand Full 39-Stock NSE Radar Screening Universe"):
            st.dataframe(
                df_rad.drop(columns=["Codex_216", "Pillar_Radar", "Buy Zone Low", "Hard Veto"]).sort_values(
                    by="ANANTA-216 Score", ascending=False
                ),
                use_container_width=True,
                hide_index=True,
            )

# ==============================================================================
# TAB 2: REAL-TIME VISUAL STOCK TERMINAL & 12-PILLAR SPIDER RADAR
# ==============================================================================
with tab_scanner:
    st.subheader("🔍 Real-Time Visual Stock Terminal, 12-Pillar Radar & Volatility-Parity Sizing")
    sc1, sc2, sc3 = st.columns([2.2, 1.2, 1.0])
    with sc1:
        target_t = (
            st.text_input("Enter any NSE Ticker (e.g. BEL, HAL, KOTAKBANK, POLYCAB, TRENT, YESBANK):", "BEL")
            .upper()
            .replace(".NS", "")
            .strip()
        )
    with sc2:
        chart_period = st.selectbox("Historical Horizon:", ["3mo", "6mo", "1y", "2y"], index=1)
    with sc3:
        chart_mode = st.radio("Price Display:", ["Candlestick", "Line"], horizontal=True)

    featured_codex_res = None
    if target_t:
        with st.spinner(f"Computing 216-Variable Codex & Auction Profile for {target_t}..."):
            yf_sym = f"{target_t.replace('DATA_PATTERNS', 'DATAPATTNS')}.NS"
            try:
                df_chart = yf.Ticker(yf_sym).history(period=chart_period)
            except Exception:
                df_chart = pd.DataFrame()

            featured_codex_res = compute_216_variable_codex(target_t, df_chart, vedic, acct_equity_base)
            c216 = featured_codex_res["Codex_216"]

            ch_col, rad_col = st.columns([1.85, 1.0])
            with ch_col:
                if not df_chart.empty and len(df_chart) >= 20:
                    fig_t = GrandVisualEngine.create_advanced_technical_chart(
                        df_chart,
                        target_t,
                        featured_codex_res["Buy Zone Low"],
                        featured_codex_res["CMP (₹)"],
                        featured_codex_res["Stop-Loss (₹)"],
                        featured_codex_res["Target (₹)"],
                        c216["068. POC_Price"],
                        use_candles=(chart_mode == "Candlestick"),
                    )
                    st.plotly_chart(fig_t, use_container_width=True)
            with rad_col:
                fig_spider = GrandVisualEngine.create_pillar_spider_radar(featured_codex_res["Pillar_Radar"], target_t)
                st.plotly_chart(fig_spider, use_container_width=True)

            m1, m2, m3, m4, m5 = st.columns(5)
            m1.metric("Live CMP (Split-Adj)", f"₹{featured_codex_res['CMP (₹)']:,.2f}", f"{featured_codex_res['Change %']:+.2f}%")
            m2.metric("ANANTA-216 Score", f"{featured_codex_res['ANANTA-216 Score']} / 100", featured_codex_res["Verdict"])
            m3.metric("Accumulation Zone", featured_codex_res["Buy Zone"], f"POC: ₹{c216['068. POC_Price']:,.1f}")
            m4.metric("Profit Target", f"₹{featured_codex_res['Target (₹)']:,.1f}", f"R:R {featured_codex_res['R:R']}")
            m5.metric("2.2x ATR Stop", f"₹{featured_codex_res['Stop-Loss (₹)']:,.1f}", f"{c216['107. Stop_Loss_Pct']:.2f}%")

            if featured_codex_res["Hard Veto"]:
                rec_shares = 0
                rec_outlay = 0.0
            else:
                risk_inr = acct_equity_base * (risk_per_trade_pct / 100.0)
                per_sh_risk = max(
                    featured_codex_res["CMP (₹)"] - featured_codex_res["Stop-Loss (₹)"],
                    featured_codex_res["CMP (₹)"] * 0.01,
                )
                shares_by_risk = math.floor(risk_inr / per_sh_risk)
                shares_by_cap = math.floor((acct_equity_base * 0.08) / max(featured_codex_res["CMP (₹)"], 1.0))
                rec_shares = min(shares_by_risk, shares_by_cap)
                rec_outlay = rec_shares * featured_codex_res["CMP (₹)"]

            st.markdown(
                f"""
                <div class="glass-card">
                    <b>📐 Principle-1 Gatekeeper & Fractional Kelly Sizing Summary ({target_t})</b><br>
                    • <b>Gatekeeper Forensic Verdict:</b> {featured_codex_res['Forensic Note']} | <b>Beneish M:</b> {featured_codex_res['Beneish M']} | <b>Sloan Accrual:</b> {featured_codex_res['Sloan Accrual %']}%<br>
                    • <b>Vedic Saptarshi Alignment:</b> Janma Rashi: <b>{c216['119. Corporate_Janma_Rashi']}</b> ({c216['120. Nakshatra_Pada']}) | Transit SAV: <b>{c216['128. SAV_Bindus_Transit']} Bindus</b> | Mahadasha: <b>{c216['133. Mahadasha_Lord']}</b><br>
                    • <b>Frontier Chaos & Flow:</b> Hurst Exponent: <b>{c216['183. Hurst_Exponent_Long_Memory']}</b> | FFT Spectral Entropy: <b>{c216['190. Spectral_Entropy_Phase_Collapse']}</b> | VPIN Toxicity: <b>{c216['185. VPIN_Order_Flow_Toxicity']}</b><br>
                    • <b>Authorized Position Size:</b> <b>{rec_shares:,} Shares</b> (Capital Outlay: <b>₹{rec_outlay:,.0f}</b> | Fractional Kelly Optimal Weight: <b>{featured_codex_res['Kelly Weight %']}%</b>)
                </div>
                """,
                unsafe_allow_html=True,
            )

# ==============================================================================
# TAB 3: THE 12-PILLAR 216-VARIABLE DETERMINISTIC CODEX EXPLORER (ANY TICKER)
# ==============================================================================
with tab_codex:
    st.subheader("🧬 Master 12-Pillar 216-Variable Codex Inspector")
    codex_t_col1, codex_t_col2 = st.columns([1.8, 2.2])
    with codex_t_col1:
        codex_sym_input = (
            st.text_input("Inspect 216 Variables for Ticker:", value=target_t if target_t else "BEL")
            .upper()
            .replace(".NS", "")
            .strip()
        )
    with codex_t_col2:
        var_search = st.text_input("Search Variable by Name or Number (e.g. 'Beneish', 'Kelly', '128', 'Hurst'):", "").strip()

    if codex_sym_input != target_t or featured_codex_res is None:
        yf_c_sym = f"{codex_sym_input.replace('DATA_PATTERNS', 'DATAPATTNS')}.NS"
        try:
            c_hist = yf.Ticker(yf_c_sym).history(period="6mo")
        except Exception:
            c_hist = pd.DataFrame()
        active_codex_obj = compute_216_variable_codex(codex_sym_input, c_hist, vedic, acct_equity_base)
    else:
        active_codex_obj = featured_codex_res

    codex_dict = active_codex_obj["Codex_216"]

    if var_search:
        filtered_items = [(k, str(v)) for k, v in codex_dict.items() if var_search.upper() in k.upper()]
        st.dataframe(
            pd.DataFrame(filtered_items, columns=["Variable Code & Name", f"Computed Value ({codex_sym_input})"]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        pillar_ranges = [
            ("Pillar 1: Buffett-Munger Capital Forensics & Owner Cash (001 - 026)", 1, 26),
            ("Pillar 2: Damani Working Capital, Moats & Porter Forces (027 - 044)", 27, 44),
            ("Pillar 3: Promoter DNA & Governance Forensics (045 - 060)", 45, 60),
            ("Pillar 4: Institutional Tape & Microstructure Flow (061 - 082)", 61, 82),
            ("Pillar 5: Macro Transmission & Sovereign Mandates (083 - 104)", 83, 104),
            ("Pillar 6: Quantitative Risk Budgeting, Sizing & Stress Testing (105 - 115)", 105, 115),
            ("Pillar 7: Saptarshi Deep Vedic Astrological Engine (116 - 140)", 116, 140),
            ("Pillar 8: The Operational Frontier Edge (141 - 150)", 141, 150),
            ("Pillars 9 & 10: All-Weather Antifragility & Mundane Synthesis (151 - 175)", 151, 175),
            ("Pillars 11 & 12: Frontier God-Particle Intelligence (176 - 216)", 176, 216),
        ]
        all_items = list(codex_dict.items())
        for p_title, start_i, end_i in pillar_ranges:
            with st.expander(f"🔹 {p_title}", expanded=(start_i == 1 or start_i == 176)):
                slice_items = [(k, str(v)) for k, v in all_items[start_i - 1 : end_i]]
                st.dataframe(
                    pd.DataFrame(slice_items, columns=["Variable Code & Name", f"Computed Value ({codex_sym_input})"]),
                    use_container_width=True,
                    hide_index=True,
                )

# ==============================================================================
# TAB 4: MULTI-FAMILY VAULT, TREEMAP, ACAR SPLIT RECONCILER & AI NLP PARSER
# ==============================================================================
with tab_vault:
    st.subheader(f"💼 Sovereign Portfolio Vault: {active_profile}")

    with st.expander("🤖 AI Raw Portfolio Text Ingestion (Paste Broker Holdings / WhatsApp / Excel Text)", expanded=df_vault_disp.empty):
        st.caption(
            "Paste messy lines containing Symbol, Quantity, and Buy Price (e.g. `KOTAKBANK 260 2150`, `BEL.NS 300 @ 210.65`, `HAL, 30, 3420`). "
            "ACAR automatically reconciles stock splits (like Kotak Bank's 1:5 split) upon ingestion."
        )
        sample_paste = "KOTAKBANK 260 2150.00\nBEL.NS 300 210.65\nHAL 30 3420.00\nPOLYCAB 25 4937.74\nTRENT 18 4150.00"
        raw_paste_input = st.text_area("Paste Raw Broker Holdings / Text:", value=sample_paste, height=115)
        if st.button(f"⚡ Parse & Bulk-Upsert into {active_profile} Vault"):
            parsed_list = parse_raw_broker_holdings_text(raw_paste_input)
            if parsed_list:
                for item in parsed_list:
                    save_holding_direct(active_profile, item["Symbol"], item["Shares"], item["Avg_Cost"], item["Sector"])
                st.success(f"Successfully parsed and bulk-upserted {len(parsed_list)} positions into {active_profile}!")
                st.rerun()
            else:
                st.error("No valid `SYMBOL QTY PRICE` lines detected. Check your text format.")

    sb1, sb2, sb3 = st.columns(3)
    with sb1:
        if st.button(f"📥 Seed Verified 57-Stock Institutional Universe into {active_profile}"):
            for s, q, c, sec in VERIFIED_57_SEED_HOLDINGS:
                save_holding_direct(active_profile, s, q, c, sec)
            st.rerun()
    with sb2:
        if st.button(f"⚡ Seed Core 8 Starter Pack into {active_profile}"):
            for s, q, c, sec in VERIFIED_57_SEED_HOLDINGS[:8]:
                save_holding_direct(active_profile, s, q, c, sec)
            st.rerun()
    with sb3:
        if st.button(f"🗑️ Clear All Holdings in {active_profile}"):
            with sqlite3.connect(DB_FILE) as conn:
                conn.execute("DELETE FROM family_holdings WHERE profile = ?", (active_profile,))
                conn.commit()
            st.rerun()

    if acar_alerts:
        for alert_msg in acar_alerts:
            st.info(f"🛡️ **ACAR Corporate Action Split Immunity Triggered:** {alert_msg}")

    if df_vault_disp.empty:
        st.info(f"No holdings currently registered for **{active_profile}**. Use the NLP Parser or 57-Stock Seed button above.")
    else:
        tot_c = float(df_vault_disp["Cost Basis"].sum())
        tot_v = float(df_vault_disp["Market Value"].sum())
        tot_gain = tot_v - tot_c
        tot_pct = round((tot_gain / tot_c) * 100.0, 2) if tot_c > 0 else 0.0
        day_pnl = sum(float(r["Market Value"]) * (float(r["1D Change %"]) / 100.0) for _, r in df_vault_disp.iterrows())

        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Reconciled Cost Basis", f"₹{tot_c:,.2f}", f"{len(df_vault_disp)} Positions")
        k2.metric("Mark-to-Market NAV", f"₹{tot_v:,.2f}", f"{tot_pct:+.2f}% Total Return")
        k3.metric("Net Unrealized P&L", f"₹{tot_gain:+,.2f}", f"1D Est: ₹{day_pnl:+,.0f}")
        k4.metric("Max Single-Stock Wt", f"{df_vault_disp['Weight %'].max():.2f}%", "Hard Cap: 8.00%")

        c_pie, c_tree = st.columns([1.0, 1.35])
        with c_pie:
            fig_d = GrandVisualEngine.create_sector_donut_chart(df_vault_disp)
            if fig_d:
                st.plotly_chart(fig_d, use_container_width=True)
        with c_tree:
            fig_tm = GrandVisualEngine.create_portfolio_treemap(df_vault_disp)
            if fig_tm:
                st.plotly_chart(fig_tm, use_container_width=True)

        st.markdown("#### 🛡️ Principle-1 Gatekeeper & Concentration Audit")
        ov_stocks = df_vault_disp[df_vault_disp["Weight %"] > 8.0]
        sec_wts = df_vault_disp.groupby("Sector")["Weight %"].sum()
        ov_secs = sec_wts[sec_wts > 20.0]
        veto_held = df_vault_disp[df_vault_disp["Symbol"].isin(FORENSIC_VETO_REGISTRY.keys())]

        if ov_stocks.empty and ov_secs.empty and veto_held.empty:
            st.success("🟢 100% Compliant: All positions <8.0% single-stock cap, <20.0% sector cap, and zero forensic vetoes.")
        else:
            for _, ov in ov_stocks.iterrows():
                st.warning(f"⚠️ **Single-Stock Cap Breach:** `{ov['Symbol']}` is at **{ov['Weight %']:.2f}%** (Ceiling: 8.0%).")
            for sn, sw in ov_secs.items():
                st.warning(f"⚠️ **Sector Cap Breach:** `{sn}` is at **{sw:.2f}%** (Ceiling: 20.0%).")
            for _, vh in veto_held.iterrows():
                st.error(
                    f"⛔ **Forensic Gatekeeper Veto Held:** `{vh['Symbol']}` ({vh['Weight %']:.2f}% wt) — "
                    f"{FORENSIC_VETO_REGISTRY[vh['Symbol']]['reason']}"
                )

        st.dataframe(df_vault_disp, use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 5: AUTONOMOUS REBALANCER, ORDER TICKET GENERATOR & MONTE CARLO STRESS LAB
# ==============================================================================
with tab_rebalance:
    st.subheader("🎯 Autonomous Portfolio Rebalancer, Order Ticket Generator & Tail-Risk Stress Lab")
    st.caption(
        "Transforms 216-variable intelligence into concrete money-making execution tickets: "
        "purges Principle-1 forensic vetoes, trims >8% overweight positions, and deploys capital into top Fractional Kelly alpha leaders."
    )

    ref_eq = float(df_vault_disp["Market Value"].sum()) if not df_vault_disp.empty else acct_equity_base
    df_tickets = generate_autonomous_rebalance_tickets(df_vault_disp, df_rad, ref_eq, vedic)

    st.markdown("#### 📋 Executable Institutional Order Tickets (Today's Action Queue)")
    if df_tickets.empty:
        st.success("Portfolio is in equilibrium. No immediate rebalance tickets required.")
    else:
        st.dataframe(df_tickets, use_container_width=True, hide_index=True)
        if not df_vault_disp.empty:
            if st.button(f"⚡ Auto-Execute All Urgent Veto Exits & Risk Trims in {active_profile} Vault"):
                exec_cnt = 0
                for _, tk_row in df_tickets.iterrows():
                    if "SELL" in tk_row["Action"]:
                        ok, _ = execute_sell_order(
                            active_profile,
                            tk_row["Symbol"],
                            float(tk_row["Order Shares"]),
                            float(tk_row["Limit / Exec Price (₹)"]),
                        )
                        if ok:
                            exec_cnt += 1
                st.success(f"Executed {exec_cnt} risk-reduction sell/trim orders in {active_profile}!")
                st.rerun()

    st.markdown("#### 🎲 1,000-Path Jump-Diffusion Monte Carlo Tail-Risk & VaR Lab")
    fig_mc, mc_stats = GrandVisualEngine.create_monte_carlo_fan_chart(ref_eq)
    mc1, mc2, mc3, mc4 = st.columns(4)
    mc1.metric("1Y Median Projected NAV", f"₹{mc_stats['median_1y']:,.0f}", "+18.5% Drift")
    mc2.metric("1Y 95th Percentile (Bull)", f"₹{mc_stats['bull_95_1y']:,.0f}", "Convex Payoff")
    mc3.metric("95% Annual Value-at-Risk (VaR)", f"₹{mc_stats['var_95_inr']:,.0f}", "5th Percentile Loss")
    mc4.metric("95% Conditional VaR (CVaR)", f"₹{mc_stats['cvar_95_inr']:,.0f}", "Expected Tail Shortfall")
    st.plotly_chart(fig_mc, use_container_width=True)

# ==============================================================================
# TAB 6: EMBEDDED CONVERSATIONAL AI QUANT COPILOT (MULTI-TICKER + PORTFOLIO AWARE)
# ==============================================================================
with tab_copilot:
    st.subheader(f"💬 Embedded Conversational AI Quant Copilot: {active_profile}")
    st.caption(
        "Select any ticker or click a quick-prompt button for an instant 216-variable synthesis. "
        "Works 100% offline deterministically or optionally connects to Gemini / Groq."
    )

    ak1, ak2, ak3 = st.columns([1.3, 1.3, 1.4])
    with ak1:
        copilot_ticker_pick = st.selectbox(
            "Select Any Ticker for 1-Tap 216-Variable Audit:",
            [s.replace(".NS", "") for s in NSE_RADAR_UNIVERSE],
            index=0,
        )
    with ak2:
        llm_provider = st.selectbox(
            "Copilot Engine Mode:",
            ["Offline Deterministic 216-Codex Engine (Zero Key Needed)", "Google Gemini (gemini-1.5-flash)", "Groq (Llama-3.3-70B)"],
        )
    with ak3:
        user_api_key = st.text_input("Optional Gemini / Groq API Key:", type="password")

    if "copilot_messages" not in st.session_state:
        st.session_state.copilot_messages = [
            {
                "role": "assistant",
                "content": generate_deterministic_copilot_response(
                    "SUMMARY", active_profile, df_vault_disp, df_rad, vedic, live_mmi
                ),
            }
        ]

    qp1, qp2, qp3, qp4 = st.columns(4)
    triggered_prompt = None
    if qp1.button(f"⚡ Audit Selected: {copilot_ticker_pick}"):
        triggered_prompt = f"Audit {copilot_ticker_pick} across all 216 variables and give exact buy, stop, and target levels."
    if qp2.button("🛡️ What should I trim/exit today?"):
        triggered_prompt = "What should I trim or exit in my portfolio today?"
    if qp3.button("🟢 Top 5 Institutional Buys"):
        triggered_prompt = "What are the top 5 institutional buys in the market right now?"
    if qp4.button("🏦 Audit KOTAKBANK (ACAR Split)"):
        triggered_prompt = "Audit KOTAKBANK and verify split-adjusted buy zone and stop levels."

    chat_input_val = st.chat_input("Ask anything (e.g., 'Audit HAL', 'Audit TRENT', 'What should I trim today?', 'Top 5 buys')...")
    active_query = triggered_prompt or chat_input_val

    if active_query:
        st.session_state.copilot_messages.append({"role": "user", "content": active_query})
        det_reply = generate_deterministic_copilot_response(
            active_query, active_profile, df_vault_disp, df_rad, vedic, live_mmi
        )
        final_reply = det_reply
        if user_api_key and "Offline" not in llm_provider:
            sys_ctx = (
                "You are VEDICQUANT PARAMA-VAJRA (ANANTA-216), Chief Quantitative Architect and Vedic Astrologer. "
                f"Use this deterministic 216-variable analysis to answer concisely:\n{det_reply}"
            )
            llm_out = query_optional_llm_api(user_api_key, llm_provider, sys_ctx, active_query)
            if llm_out:
                final_reply = llm_out
        st.session_state.copilot_messages.append({"role": "assistant", "content": final_reply})

    for msg in st.session_state.copilot_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ==============================================================================
# TAB 7: INSTITUTIONAL TRADE DESK (BUY / SELL / REALIZED P&L LEDGER)
# ==============================================================================
with tab_trade:
    st.subheader(f"⚙️ Institutional Trade Execution Desk: {active_profile}")
    t_col1, t_col2 = st.columns(2)

    with t_col1:
        st.markdown("#### 🟢 Execute Buy / Accumulation Order")
        with st.form("buy_order_form", clear_on_submit=True):
            b_sym = st.text_input("NSE Ticker Symbol (e.g. BEL, HAL, KOTAKBANK):").upper().strip()
            b_qty = st.number_input("Quantity (Shares):", min_value=1.0, value=10.0, step=1.0)
            b_prc = st.number_input("Execution Price (₹):", min_value=0.05, value=400.0, step=0.5)
            b_sec = st.selectbox(
                "Sector Classification:",
                [
                    "Equities", "Defence & Aerospace", "Private Banking", "PSU Banking", "Capital Markets",
                    "Cables & Wires", "Industrial Automation", "Infrastructure & EPC", "Electronics Mfg (EMS)",
                    "PSU Energy & Mining", "Power Utilities", "IT Services", "Digital ER&D", "Auto OEMs",
                    "Luxury & Retail", "Specialty Chemicals", "Pharmaceuticals",
                ],
            )
            if st.form_submit_button(f"🟢 Commit BUY Order to {active_profile}"):
                ok, msg = execute_buy_order(active_profile, b_sym, b_qty, b_prc, b_sec)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    with t_col2:
        st.markdown("#### 🔴 Execute Sell / Partial Trim / Exit Order")
        held_list = df_held_raw["symbol"].tolist() if not df_held_raw.empty else []
        with st.form("sell_order_form", clear_on_submit=True):
            s_sym = st.selectbox("Select Holding to Sell:", held_list) if held_list else st.text_input("Symbol:").upper().strip()
            s_qty = st.number_input("Sell Quantity (Shares):", min_value=1.0, value=10.0, step=1.0)
            s_prc = st.number_input("Sale Price (₹):", min_value=0.05, value=450.0, step=0.5)
            if st.form_submit_button(f"🔴 Commit SELL Order from {active_profile}"):
                ok, msg = execute_sell_order(active_profile, s_sym, s_qty, s_prc)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

    st.markdown("#### 📜 Immutable Trade Audit Ledger")
    df_led_disp = get_trade_ledger(active_profile)
    if df_led_disp.empty:
        st.info(f"No trades logged for **{active_profile}** yet.")
    else:
        st.metric("Cumulative Realized P&L (Booked)", f"₹{float(df_led_disp['realized_pnl'].sum()):+,.2f}")
        st.dataframe(df_led_disp, use_container_width=True, hide_index=True)

# ==============================================================================
# TAB 8: CLOUD-IMMUNE JSON VAULT BACKUP & 6-SHEET EXCEL DOSSIER
# ==============================================================================
with tab_export:
    st.subheader("📥 6-Sheet Institutional Excel Dossier & Cloud-Immune JSON Backup")
    st.markdown(
        """
        <div class="glass-card">
            <b>🏛️ Institutional 6-Sheet Workbook Architecture (XlsxWriter):</b><br>
            • <b>Sheet 1 (01_Executive_Vedic_Brief):</b> Portfolio NAV, Unrealized P&L, MMI, &amp; Saptarshi Vedic Parameters.<br>
            • <b>Sheet 2 (02_Vault_Profile):</b> Mark-to-market position audit with ACAR split reconciliation &amp; 8% risk ceiling flags.<br>
            • <b>Sheet 3 (03_Sector_Risk_Audit):</b> Sector-level capital allocation vs. 20.0% institutional concentration cap.<br>
            • <b>Sheet 4 (04_Live_Market_Radar):</b> Complete 39-stock NSE universe ranked by ANANTA-216 Score.<br>
            • <b>Sheet 5 (05_Codex216_Ticker):</b> Full 216-variable line-by-line deterministic ledger for your selected ticker.<br>
            • <b>Sheet 6 (06_Trade_Audit_Ledger):</b> Complete historical trade execution log with realized P&amp;L accounting.
        </div>
        """,
        unsafe_allow_html=True,
    )

    dossier_sym = st.selectbox(
        "Select Featured Stock for Sheet 5 (Full 216-Variable Codex Sheet):",
        [s.replace(".NS", "") for s in NSE_RADAR_UNIVERSE],
        index=0,
    )
    yf_d_sym = f"{dossier_sym.replace('DATA_PATTERNS', 'DATAPATTNS')}.NS"
    try:
        dossier_hist = yf.Ticker(yf_d_sym).history(period="6mo")
    except Exception:
        dossier_hist = pd.DataFrame()
    dossier_codex_dict = compute_216_variable_codex(dossier_sym, dossier_hist, vedic, acct_equity_base)["Codex_216"]

    excel_dossier_bytes = build_ananta216_excel_dossier(
        active_profile=active_profile,
        df_vault_disp=df_vault_disp,
        df_radar=df_rad,
        df_ledger=get_trade_ledger(active_profile),
        vedic_info=vedic,
        mmi_score=live_mmi,
        featured_sym=dossier_sym,
        featured_codex=dossier_codex_dict,
    )

    safe_prof_slug = re.sub(r"[^A-Za-z0-9]+", "_", active_profile).strip("_")
    xlsx_filename = f"PARAMA_VAJRA_ANANTA216_{safe_prof_slug}_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx"

    st.download_button(
        label=f"📥 Download 6-Sheet Institutional Excel Dossier ({xlsx_filename})",
        data=excel_dossier_bytes,
        file_name=xlsx_filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True,
    )

    st.markdown("#### 🔒 Cloud-Immune Multi-Family Vault Backup & Restore (Zero Data Loss)")
    bk1, bk2 = st.columns(2)
    with bk1:
        json_backup_str = export_all_vaults_json()
        st.download_button(
            label="📲 Download All Family Vaults Backup (.json)",
            data=json_backup_str.encode("utf-8"),
            file_name=f"PARAMA_VAJRA_All_Family_Vaults_{datetime.datetime.now().strftime('%Y%m%d')}.json",
            mime="application/json",
            use_container_width=True,
        )
    with bk2:
        uploaded_json = st.file_uploader("Upload `.json` Vault Backup File to Restore:", type=["json"])
        if uploaded_json is not None:
            if st.button("⚡ Confirm Restore All Family Vaults"):
                raw_json_bytes = uploaded_json.read().decode("utf-8")
                ok, msg = restore_vaults_from_json(raw_json_bytes)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
