"""
================================================================================
VAJRA-175 / ANANTA-216: MASTER TERMINAL COCKPIT (app.py)
Visual Cyber-Vedic UI | Multi-Family Vault | Real-Time Scanners & Dossier
================================================================================
"""

import datetime
import io
import math
import re
import sqlite3
import pandas as pd
import streamlit as st
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Import our computational brain
from engine import (
    VAJRA_PIL_ICON, VAJRA_ICON_URI, DB_FILE, FORENSIC_VETO_REGISTRY,
    SECTOR_DEFAULT_MAP, VERIFIED_57_SEED, reconcile_corporate_action,
    get_holdings, save_holding_direct, execute_buy_order, execute_sell_order,
    export_all_vaults_json, restore_vaults_from_json, parse_raw_broker_holdings_text,
    get_live_vedic_chronometer, compute_216_variable_codex, scan_radar_universe_216,
    batch_fetch_live_prices, generate_rebalance_tickets
)

st.set_page_config(
    page_title="ANANTA-216 | Sovereign Terminal",
    page_icon=VAJRA_PIL_ICON,
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(f"""
<head>
    <title>ANANTA-216 Sovereign</title>
    <meta name="apple-mobile-web-app-capable" content="yes">
    <meta name="apple-mobile-web-app-title" content="ANANTA-216">
    <link rel="icon" type="image/png" href="{VAJRA_ICON_URI}">
    <link rel="apple-touch-icon" href="{VAJRA_ICON_URI}">
</head>
<style>
    .stApp {{ background-color: #050811; color: #F8FAFC; }}
    .glass-card {{ background: rgba(15, 23, 42, 0.82); padding: 16px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.08); margin-bottom: 12px; }}
    .muhurta-live-banner {{ background: linear-gradient(135deg, rgba(46, 16, 101, 0.90), rgba(15, 23, 42, 0.85)); border-left: 5px solid #A855F7; padding: 14px; border-radius: 10px; margin-bottom: 14px; }}
    .rahu-alert-banner {{ background: linear-gradient(135deg, rgba(127, 29, 29, 0.90), rgba(40, 10, 15, 0.85)); border-left: 5px solid #EF4444; padding: 14px; border-radius: 10px; margin-bottom: 14px; }}
    .status-pulse {{ display: inline-block; width: 9px; height: 9px; border-radius: 50%; background-color: #10B981; margin-right: 6px; }}
</style>
""", unsafe_allow_html=True)

# Visual Plotly Components
class GrandVisualEngine:
    @staticmethod
    def create_market_mood_gauge(score: float = 52.4):
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=score,
            title={"text": "<b>MARKET MOOD INDEX (MMI)</b>", "font": {"size": 13, "color": "#F8FAFC"}},
            number={"font": {"size": 32, "color": "#F8FAFC"}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": "#475569"},
                "bar": {"color": "#A855F7", "thickness": 0.28},
                "steps": [
                    {"range": [0, 25], "color": "#7F1D1D"}, {"range": [25, 45], "color": "#9A3412"},
                    {"range": [45, 55], "color": "#1E3A8A"}, {"range": [55, 75], "color": "#065F46"},
                    {"range": [75, 100], "color": "#047857"}
                ],
                "threshold": {"line": {"color": "#38BDF8", "width": 4}, "thickness": 0.8, "value": score}
            }
        ))
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=205, margin=dict(l=20, r=20, t=35, b=10))
        return fig

    @staticmethod
    def create_pillar_spider_radar(pillar_scores: Dict[str, float], sym: str):
        cats = list(pillar_scores.keys()) + [list(pillar_scores.keys())[0]]
        vals = list(pillar_scores.values()) + [list(pillar_scores.values())[0]]
        fig = go.Figure(data=go.Scatterpolar(r=vals, theta=cats, fill="toself", fillcolor="rgba(168, 85, 247, 0.25)", line=dict(color="#38BDF8", width=2.2)))
        fig.update_layout(polar=dict(bgcolor="rgba(15, 23, 42, 0.65)", radialaxis=dict(visible=True, range=[0, 100], gridcolor="rgba(255,255,255,0.08)")), paper_bgcolor="rgba(0,0,0,0)", height=320, margin=dict(l=30, r=30, t=35, b=15), showlegend=False)
        return fig

    @staticmethod
    def create_advanced_technical_chart(df: pd.DataFrame, sym: str, b_low: float, b_high: float, stop: float, target: float, poc: float, candles: bool = True):
        close = df["Close"]
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06, row_heights=[0.73, 0.27])
        if candles:
            fig.add_trace(go.Candlestick(x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name="OHLC"), row=1, col=1)
        else:
            fig.add_trace(go.Scatter(x=df.index, y=close, mode="lines", name="LTP", line=dict(color="#38BDF8", width=2.5)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=close.ewm(span=20).mean(), name="EMA20", line=dict(color="#F59E0B", width=1.4)), row=1, col=1)
        fig.add_trace(go.Scatter(x=df.index, y=close.ewm(span=50).mean(), name="EMA50", line=dict(color="#EC4899", width=1.4)), row=1, col=1)
        fig.add_hrect(y0=b_low, y1=b_high, fillcolor="#10B981", opacity=0.15, row=1, col=1)
        fig.add_hline(y=stop, line_color="#EF4444", line_dash="dash", row=1, col=1)
        fig.add_hline(y=target, line_color="#10B981", line_dash="dash", row=1, col=1)
        delta = close.diff()
        gain = delta.clip(lower=0.0).ewm(alpha=1/14).mean()
        loss = (-delta.clip(upper=0.0)).ewm(alpha=1/14).mean()
        rsi = 100.0 - (100.0 / (1.0 + (gain / loss.replace(0, np.nan))))
        fig.add_trace(go.Scatter(x=df.index, y=rsi, name="RSI(14)", line=dict(color="#38BDF8", width=1.6)), row=2, col=1)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(15, 23, 42, 0.55)", xaxis_rangeslider_visible=False, height=440, margin=dict(l=10, r=10, t=30, b=10))
        return fig

    @staticmethod
    def create_sector_donut_chart(df: pd.DataFrame):
        if df.empty or "Sector" not in df.columns: return None
        s_agg = df.groupby("Sector", as_index=False)["Market Value"].sum().sort_values(by="Market Value", ascending=False)
        fig = px.pie(s_agg, names="Sector", values="Market Value", hole=0.55, color_discrete_sequence=px.colors.sequential.Amiable)
        fig.update_traces(textinfo="percent+label", textfont_size=10)
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=280, margin=dict(l=10, r=10, t=30, b=10), showlegend=False)
        return fig

def sanitize_sheet_name(name: str) -> str:
    cleaned = re.sub(r"[\[\]\:\*\?\/\\]", "-", str(name)).strip()
    return cleaned[:31] if cleaned else "Sheet"

def build_ananta216_excel_dossier(active_profile: str, df_vault: pd.DataFrame, df_rad: pd.DataFrame, df_tickets: pd.DataFrame, vedic_ctx: Dict[str, Any], mmi: float, feat_sym: str, feat_codex: Dict[str, Any]) -> bytes:
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
        wb = writer.book
        fmt_hdr = wb.add_format({"bold": True, "font_color": "#FFFFFF", "bg_color": "#1E1B4B", "border": 1, "align": "center"})
        fmt_txt = wb.add_format({"font_size": 10, "border": 1, "align": "left"})

        # Sheet 1: Brief
        ws1 = wb.add_worksheet(sanitize_sheet_name("01_Executive_Brief"))
        ws1.write(0, 0, "Metric", fmt_hdr); ws1.write(0, 1, "Value", fmt_hdr)
        ws1.write(1, 0, "Profile", fmt_txt); ws1.write(1, 1, active_profile, fmt_txt)
        ws1.write(2, 0, "MMI Score", fmt_txt); ws1.write(2, 1, f"{mmi:.1f}", fmt_txt)
        ws1.write(3, 0, "Muhurta", fmt_txt); ws1.write(3, 1, vedic_ctx["abhijit"], fmt_txt)

        if not df_vault.empty:
            df_vault.to_excel(writer, sheet_name=sanitize_sheet_name(f"02_Vault_{active_profile}"), index=False)
        if not df_tickets.empty:
            df_tickets.to_excel(writer, sheet_name=sanitize_sheet_name("03_Rebalance_Tickets"), index=False)
        if not df_rad.empty:
            df_rad.to_excel(writer, sheet_name=sanitize_sheet_name("04_Market_Radar"), index=False)
        pd.DataFrame(list(feat_codex.items()), columns=["Metric", "Value"]).to_excel(writer, sheet_name=sanitize_sheet_name(f"05_Codex216_{feat_sym}"), index=False)
    return output.getvalue()

# Main Application Cockpit
vedic = get_live_vedic_chronometer()

col_h1, col_h2 = st.columns([2.4, 1.2])
with col_h1:
    st.title("⚡ ANANTA-216 SOVEREIGN")
    st.caption("PARAMA-VAJRA: 12-Pillar Alpha Engine • Saptarshi Vedic Chronometer • ACAR Reconciler")
with col_h2:
    st.markdown(f"<div style='text-align:right; padding-top:8px;'><span class='status-pulse'></span><b>{vedic['mkt_session']}</b><br><span style='font-size:12px; color:#94A3B8;'>{vedic['date']} | {vedic['day']} | {vedic['time_ist']}</span></div>", unsafe_allow_html=True)

st.markdown(f"<div class='{vedic['banner_class']}'><b>🕉️ Abhijit Muhurta:</b> {vedic['abhijit']} &nbsp;|&nbsp; <b>⚠️ Rahu Kaalam:</b> {vedic['rahu']} &nbsp;|&nbsp; <b>Status:</b> {vedic['rahu_status']}</div>", unsafe_allow_html=True)

ctrl_c1, ctrl_c2, ctrl_c3 = st.columns([1.6, 1.2, 1.2])
with ctrl_c1:
    active_profile = st.selectbox("Active Sovereign Portfolio Profile:", ["Self - Primary", "Family Member 1", "Family Member 2", "Family Trust"], index=0)
with ctrl_c2:
    acct_equity_base = st.number_input("Portfolio Capital Base (₹):", min_value=100000.0, value=2500000.0, step=100000.0)
with ctrl_c3:
    risk_per_trade_pct = st.slider("Max Risk Per Trade (%):", min_value=0.25, max_value=2.50, value=1.00, step=0.25)

with st.spinner("Sweeping Live NSE Market Universe across all 216 Variables..."):
    df_rad, macro_telemetry = scan_radar_universe_216(vedic)

live_mmi = macro_telemetry.get("mmi", 52.4)

tab_radar, tab_scanner, tab_vault, tab_rebalance, tab_trade, tab_copilot, tab_export = st.tabs([
    "🌐 Market Radar", "🔍 Visual Stock Terminal", f"💼 {active_profile} Vault",
    "⚡ Rebalance Tickets", "⚙️ Trade Desk", "💬 AI Copilot", "📥 Institutional Dossier"
])

with tab_radar:
    st.subheader("📡 Live Broader Market Radar (Outside Portfolio)")
    cg1, cg2 = st.columns([1, 1.5])
    with cg1:
        st.plotly_chart(GrandVisualEngine.create_market_mood_gauge(live_mmi), use_container_width=True)
    with cg2:
        st.markdown(f"<div class='glass-card' style='margin-top:10px;'><b>Market Mood:</b> <b>{live_mmi:.1f}</b>.<br>• <b>Principle-1 Forensic Shield:</b> Active vetoes applied to debt-diluted tickers.<br>• <b>Execution Window:</b> {vedic['abhijit']}.</div>", unsafe_allow_html=True)

    if not df_rad.empty:
        buys = df_rad[~df_rad["Hard Veto"] & df_rad["Verdict"].str.contains("BUY")].sort_values(by="ANANTA-216 Score", ascending=False).head(5)
        sells = df_rad[df_rad["Hard Veto"] | df_rad["Verdict"].str.contains("REDUCE|EXIT")].sort_values(by="ANANTA-216 Score", ascending=True).head(5)
        st.markdown("#### 🟢 TOP 5 INSTITUTIONAL BUYS (RIGHT NOW)")
        st.dataframe(buys[["Symbol", "Sector", "CMP (₹)", "Change %", "ANANTA-216 Score", "RSI (14)", "Vol Surge", "Buy Zone", "Stop-Loss (₹)", "Target (₹)", "Verdict"]], use_container_width=True, hide_index=True)
        st.markdown("#### 🔴 TOP 5 AVOID / EXIT SIGNALS (RIGHT NOW)")
        st.dataframe(sells[["Symbol", "Sector", "CMP (₹)", "Change %", "ANANTA-216 Score", "RSI (14)", "Verdict", "Forensic Note"]], use_container_width=True, hide_index=True)

with tab_scanner:
    st.subheader("🔍 Visual Stock Terminal, 12-Pillar Spider & Kelly Sizing")
    ct1, ct2 = st.columns([3, 1])
    with ct1:
        target_t = st.text_input("Enter any NSE ticker (e.g. BEL, HAL, KOTAKBANK, YESBANK):", "BEL").upper().replace(".NS", "").strip()
    with ct2:
        chart_mode = st.radio("Chart Type:", ["Candlestick", "Line"], horizontal=True)

    if target_t:
        with st.spinner(f"Computing 216 Variables for {target_t}..."):
            try:
                hist_df = yf.Ticker(f"{target_t}.NS").history(period="6mo")
            except Exception:
                hist_df = pd.DataFrame()
            codex_res = compute_216_variable_codex(target_t, hist_df, vedic, acct_equity_base)
            cmp_now = codex_res["CMP (₹)"]

            if not hist_df.empty and len(hist_df) >= 30:
                fig_c = GrandVisualEngine.create_advanced_technical_chart(hist_df, target_t, codex_res["Buy Zone Low"], cmp_now, codex_res["Stop-Loss (₹)"], codex_res["Target (₹)"], codex_res["Codex_216"]["068. POC_Price"], candles=(chart_mode == "Candlestick"))
                st.plotly_chart(fig_c, use_container_width=True)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Live CMP", f"₹{cmp_now:,.2f}", f"{codex_res['Change %']:+.2f}%")
            c2.metric("ANANTA-216 Score", f"{codex_res['ANANTA-216 Score']} / 100", codex_res["Verdict"])
            c3.metric("Buy Range", codex_res["Buy Zone"])
            c4.metric("ATR Stop-Loss", f"₹{codex_res['Stop-Loss (₹)']:,.1f}", "2.2x ATR Floor")

            if codex_res["Hard Veto"]:
                st.error(f"🚨 {codex_res['Forensic Note']}")

            col_s1, col_s2 = st.columns([1.1, 1.1])
            with col_s1:
                st.plotly_chart(GrandVisualEngine.create_pillar_spider_radar(codex_res["Pillar_Radar"], target_t), use_container_width=True)
            with col_s2:
                rps = max(cmp_now - codex_res["Stop-Loss (₹)"], cmp_now * 0.01)
                rec_sh = min(math.floor((acct_equity_base * (risk_per_trade_pct / 100.0)) / rps), math.floor((acct_equity_base * 0.08) / cmp_now)) if not codex_res["Hard Veto"] else 0
                st.markdown(f"<div class='glass-card' style='margin-top:20px;'><b>📐 Position Sizing ({target_t}):</b><br>• <b>Recommended Allocation:</b> <b>{rec_sh:,} Shares</b> (Outlay: <b>₹{rec_sh * cmp_now:,.0f}</b> | Wt: <b>{((rec_sh * cmp_now)/acct_equity_base)*100:.2f}%</b>)<br>• <b>Absolute Rupee Stop Risk:</b> <b>₹{rec_sh * rps:,.0f}</b> (Max {risk_per_trade_pct}% budget).</div>", unsafe_allow_html=True)

            with st.expander(f"📑 Inspect All 216 Computed Variables for {target_t}"):
                st.dataframe(pd.DataFrame(list(codex_res["Codex_216"].items()), columns=["Metric #", "Value"]), use_container_width=True)

df_vault_disp = pd.DataFrame()
with tab_vault:
    st.subheader(f"💼 Sovereign Vault: {active_profile}")
    df_held = get_holdings(active_profile)

    with st.expander("📥 1-Click AI Raw Text / Broker Parser"):
        raw_p = st.text_area("Paste messy broker text (e.g. KOTAKBANK 260 329.35):", height=90)
        if st.button("⚡ Parse & Load"):
            parsed = parse_raw_broker_holdings_text(raw_p)
            for p in parsed:
                save_holding_direct(active_profile, p["Symbol"], p["Shares"], p["Avg_Cost"], p["Sector"])
            st.success(f"Loaded {len(parsed)} holdings!")
            st.rerun()

    if st.button(f"📥 Seed Full Verified Holdings into {active_profile}"):
        for s, q, c, sec in VERIFIED_57_SEED:
            save_holding_direct(active_profile, s, q, c, sec)
        st.rerun()

    if not df_held.empty:
        held_syms = tuple(df_held["symbol"].unique().tolist())
        live_map = batch_fetch_live_prices(held_syms)
        v_list = []
        tot_c, tot_v = 0.0, 0.0
        for _, row in df_held.iterrows():
            sym, sh, cost, sec = row["symbol"], float(row["shares"]), float(row["avg_cost"]), row["sector"]
            cmp_l, chg_1d = live_map.get(sym, (cost, 0.0))
            sh_adj, cost_adj, split_f, acar_msg = reconcile_corporate_action(sym, sh, cost, cmp_l)
            c_tot, cur_v = sh_adj * cost_adj, sh_adj * cmp_l
            tot_c += c_tot; tot_v += cur_v
            v_list.append({"Symbol": sym, "Sector": sec, "Shares": sh_adj, "Buy Price": round(cost_adj, 2), "Live CMP": round(cmp_l, 2), "Cost Basis": round(c_tot, 2), "Market Value": round(cur_v, 2), "P&L (₹)": round(cur_v - c_tot, 2), "P&L %": round(((cur_v - c_tot) / c_tot) * 100.0, 2) if c_tot > 0 else 0.0, "ACAR Note": acar_msg})
        df_vault_disp = pd.DataFrame(v_list)
        df_vault_disp["Weight %"] = round((df_vault_disp["Market Value"] / tot_v) * 100.0, 2) if tot_v > 0 else 0.0
        df_vault_disp = df_vault_disp.sort_values(by="Market Value", ascending=False).reset_index(drop=True)

        k1, k2, k3 = st.columns(3)
        k1.metric("Capital Deployed", f"₹{tot_c:,.2f}")
        k2.metric("Market Valuation", f"₹{tot_v:,.2f}", f"{round(((tot_v-tot_c)/tot_c)*100, 1)}%")
        k3.metric("Net Unrealized P&L", f"₹{tot_v-tot_c:+,.2f}", f"Profile: {active_profile}")

        cd1, cd2 = st.columns([1, 1.2])
        with cd1:
            fig_d = GrandVisualEngine.create_sector_donut_chart(df_vault_disp)
            if fig_d: st.plotly_chart(fig_d, use_container_width=True)
        with cd2:
            overweight = df_vault_disp[df_vault_disp["Weight %"] > 8.0]
            if not overweight.empty:
                for _, ov in overweight.iterrows():
                    st.warning(f"⚠️ **Single-Stock Ceiling Alert:** `{ov['Symbol']}` is at **{ov['Weight %']:.2f}%** (Cap: 8.00%).")
            else:
                st.success("🟢 All positions strictly within institutional 8.0% ceiling.")
        st.dataframe(df_vault_disp[["Symbol", "Sector", "Shares", "Buy Price", "Live CMP", "Cost Basis", "Market Value", "P&L (₹)", "P&L %", "Weight %", "ACAR Note"]], use_container_width=True, hide_index=True)
    else:
        st.info("Vault is currently empty.")

df_rebal_tickets = pd.DataFrame()
with tab_rebalance:
    st.subheader(f"⚡ Autonomous Rebalance Order Tickets: {active_profile}")
    target_eq = float(df_vault_disp["Market Value"].sum()) if not df_vault_disp.empty else acct_equity_base
    df_rebal_tickets = generate_rebalance_tickets(df_vault_disp, df_rad, target_eq, vedic)
    if not df_rebal_tickets.empty:
        st.dataframe(df_rebal_tickets, use_container_width=True, hide_index=True)
    else:
        st.success("🟢 Portfolio is in optimal risk equilibrium.")

with tab_trade:
    st.subheader(f"⚙️ Execution Desk: {active_profile}")
    ctb, cts = st.columns(2)
    with ctb:
        with st.form("b_form", clear_on_submit=True):
            bs = st.text_input("NSE Ticker:").upper().strip()
            bq = st.number_input("Shares:", min_value=1.0, value=10.0)
            bp = st.number_input("Price (₹):", min_value=0.1, value=500.0)
            bsec = st.text_input("Sector:", "Equities")
            if st.form_submit_button(f"Commit BUY to {active_profile}"):
                if bs: execute_buy_order(active_profile, bs, bq, bp, bsec); st.rerun()
    with cts:
        held_opts = df_held["symbol"].tolist() if not df_held.empty else ["None"]
        with st.form("s_form", clear_on_submit=True):
            ss = st.selectbox("Holding to Sell:", held_opts)
            sq = st.number_input("Shares:", min_value=1.0, value=10.0)
            sp = st.number_input("Price (₹):", min_value=0.1, value=550.0)
            if st.form_submit_button(f"Commit SELL from {active_profile}"):
                if ss != "None": execute_sell_order(active_profile, ss, sq, sp); st.rerun()

with tab_copilot:
    st.subheader(f"💬 Conversational Quant Copilot: {active_profile}")
    u_query = st.text_input("Ask Sovereign Copilot:", placeholder="e.g. Audit BEL, or What should I trim today?")
    if u_query:
        q_up = u_query.upper().strip()
        ans = []
        if "TRIM" in q_up or "SELL" in q_up:
            ans.append(f"### 🛡️ Trim & Exit Protocol ({active_profile})")
            if not df_vault_disp.empty:
                for _, r in df_vault_disp[df_vault_disp['Symbol'].isin(FORENSIC_VETO_REGISTRY.keys())].iterrows():
                    ans.append(f"- **`{r['Symbol']}`**: ⛔ {FORENSIC_VETO_REGISTRY[r['Symbol']]}")
                for _, r in df_vault_disp[df_vault_disp['Weight %'] > 8.0].iterrows():
                    ans.append(f"- **`{r['Symbol']}`**: ⚠️ Overweight ({r['Weight %']:.1f}% > 8% cap). Trim partial profit.")
        elif "BUY" in q_up or "TOP" in q_up:
            ans.append("### 🟢 Top Live Alpha Buys")
            if not df_rad.empty:
                for _, r in df_rad[~df_rad['Hard Veto']].sort_values(by='ANANTA-216 Score', ascending=False).head(3).iterrows():
                    ans.append(f"- **`{r['Symbol']}`**: Score {r['ANANTA-216 Score']}/100 | Zone: {r['Buy Zone']} | Stop: ₹{r['Stop-Loss (₹)']}")
        else:
            ans.append(f"### ⚡ Sovereign Audit Context ({active_profile})\n- Total Deployed: ₹{df_vault_disp['Cost Basis'].sum() if not df_vault_disp.empty else 0:,.0f} | Muhurta: {vedic['abhijit']}\n- Try asking: *'What should I trim?'* or *'Top buys right now'*.")
        st.markdown(f"<div class='glass-card'>{'<br>'.join(ans)}</div>", unsafe_allow_html=True)

with tab_export:
    st.subheader("📥 5-Sheet Institutional Excel Dossier & Backup")
    feat_codex = compute_216_variable_codex("BEL", pd.DataFrame(), vedic)["Codex_216"]
    x_bytes = build_ananta216_excel_dossier(active_profile, df_vault_disp, df_rad, df_rebal_tickets, vedic, live_mmi, "BEL", feat_codex)
    st.download_button("📥 Download 5-Sheet Institutional Excel Dossier (.xlsx)", data=x_bytes, file_name=f"ANANTA216_{active_profile[:10]}_{datetime.datetime.now().strftime('%Y%m%d')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    st.markdown("---")
    st.download_button("🔒 Download Full Family Vault Backup (.json)", data=export_all_vaults_json(), file_name=f"ANANTA216_Vault_Backup_{datetime.datetime.now().strftime('%Y%m%d')}.json", mime="application/json")
    up_b = st.file_uploader("Restore Backup JSON File:", type=["json"])
    if up_b and st.button("Confirm Restore All Vaults"):
        ok, msg = restore_vaults_from_json(up_b.read().decode("utf-8"))
        if ok: st.success(msg); st.rerun()
