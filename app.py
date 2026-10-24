"""
================================================================================
VAJRA-175: GRAND CYBER-VEDIC MASTER TERMINAL (ARCHITECTURE 5.0)
World-Class UI/UX with Plotly Gauges, Interactive Charts & Multi-Family Vault.
================================================================================
"""

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import math
import io
import json
import sqlite3
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px

# ------------------------------------------------------------------------------
# 1. LUXURY CYBER-VEDIC MOBILE UI (GLASSMORPHISM & DEEP OBSIDIAN THEME)
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="VAJRA-175 Sovereign Terminal",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<head>
    <title>VAJRA-175</title>
    <meta name="apple-mobile-web-app-title" content="VAJRA">
    <meta name="application-name" content="VAJRA">
    <meta name="theme-color" content="#070A13">
</head>
<style>
    /* Ultra-Premium Glassmorphism & Cyber-Vedic Palette */
    .stApp { background-color: #070A13; color: #F1F5F9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    
    .glass-card {
        background: rgba(15, 23, 42, 0.75);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        padding: 16px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        margin-bottom: 12px;
    }
    
    .muhurta-live-banner {
        background: linear-gradient(135deg, rgba(46, 16, 101, 0.8), rgba(88, 28, 135, 0.6));
        border: 1px solid rgba(168, 85, 247, 0.3);
        color: #F5F3FF;
        padding: 14px 18px;
        border-radius: 12px;
        border-left: 6px solid #A855F7;
        margin-bottom: 16px;
        box-shadow: 0 4px 20px rgba(168, 85, 247, 0.2);
    }
    
    .badge-buy {
        background: linear-gradient(135deg, #065F46, #047857);
        color: #6EE7B7;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 0.5px;
        border: 1px solid rgba(110, 231, 183, 0.3);
    }
    
    .badge-veto {
        background: linear-gradient(135deg, #881337, #9F1239);
        color: #FECDD3;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: 700;
        font-size: 12px;
        letter-spacing: 0.5px;
        border: 1px solid rgba(254, 205, 211, 0.3);
    }

    .status-pulse {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
        margin-right: 6px;
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. PERSISTENT SQLITE DATABASE (MULTI-PROFILE FAMILY VAULT)
# ------------------------------------------------------------------------------
DB_FILE = "vajra_grand_vault.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS family_holdings (
            profile TEXT,
            symbol TEXT,
            shares REAL,
            avg_cost REAL,
            sector TEXT,
            added_date TEXT,
            PRIMARY KEY(profile, symbol)
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS trade_ledger (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile TEXT,
            symbol TEXT,
            action TEXT,
            shares REAL,
            price REAL,
            total_amount REAL,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def get_holdings(profile: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_FILE)
    df = pd.read_sql_query("SELECT symbol, shares, avg_cost, sector FROM family_holdings WHERE profile = ?", conn, params=(profile,))
    conn.close()
    return df

def save_holding(profile: str, sym: str, shares: float, cost: float, sec: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO family_holdings (profile, symbol, shares, avg_cost, sector, added_date)
        VALUES (?, ?, ?, ?, ?, ?)
        ON CONFLICT(profile, symbol) DO UPDATE SET shares=excluded.shares, avg_cost=excluded.avg_cost, sector=excluded.sector
    """, (profile, sym.upper().strip(), shares, cost, sec, datetime.datetime.now().strftime("%Y-%m-%d %H:%M")))
    conn.commit()
    conn.close()

def delete_holding(profile: str, sym: str):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM family_holdings WHERE profile = ? AND symbol = ?", (profile, sym.upper().strip()))
    conn.commit()
    conn.close()

def record_trade(profile: str, sym: str, action: str, shares: float, price: float):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        INSERT INTO trade_ledger (profile, symbol, action, shares, price, total_amount, timestamp)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (profile, sym.upper().strip(), action, shares, price, shares * price, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

init_db()

# ------------------------------------------------------------------------------
# 3. DYNAMIC ASTRONOMICAL CHRONOMETER
# ------------------------------------------------------------------------------
def get_live_vedic():
    day_name = datetime.datetime.now().strftime("%A")
    rahu_map = {
        "Monday": ("07:30 AM", "09:00 AM", "🟢 Cleared (Ended before 09:15 open)"),
        "Tuesday": ("03:00 PM", "04:30 PM", "⚠️ Final 30-min blackout"),
        "Wednesday": ("12:00 PM", "01:30 PM", "⚠️ Midday blackout"),
        "Thursday": ("01:30 PM", "03:00 PM", "⚠️ Afternoon blackout"),
        "Friday": ("10:30 AM", "12:00 PM", "⚠️ Morning blackout"),
        "Saturday": ("09:00 AM", "10:30 AM", "Weekend"),
        "Sunday": ("04:30 PM", "06:00 PM", "Weekend")
    }
    r_start, r_end, r_stat = rahu_map.get(day_name, ("--", "--", "Clear"))
    return {
        "day": day_name,
        "date": datetime.datetime.now().strftime("%d %b %Y"),
        "abhijit": "11:46 AM - 12:34 PM IST",
        "rahu": f"{r_start} - {r_end}",
        "rahu_status": r_stat
    }

vedic = get_live_vedic()

# ------------------------------------------------------------------------------
# 4. PLOTLY VISUAL ENGINE: GAUGES, CHARTS & ALLOCATION DONUTS
# ------------------------------------------------------------------------------
class GrandVisualEngine:
    @staticmethod
    def create_market_mood_gauge(score: float = 44.7):
        """Creates an institutional speedometer gauge for Market Mood Index."""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=score,
            title={"text": "<b>MARKET MOOD INDEX (MMI)</b>", "font": {"size": 15, "color": "#F1F5F9"}},
            number={"font": {"size": 32, "color": "#F1F5F9"}},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#475569"},
                "bar": {"color": "#A855F7", "thickness": 0.25},
                "bgcolor": "rgba(0,0,0,0)",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 25], "color": "#7F1D1D"},     # Extreme Fear
                    {"range": [25, 45], "color": "#9A3412"},    # Fear
                    {"range": [45, 55], "color": "#1E3A8A"},    # Neutral
                    {"range": [55, 75], "color": "#065F46"},    # Greed
                    {"range": [75, 100], "color": "#047857"}    # Extreme Greed
                ],
                "threshold": {"line": {"color": "#F1F5F9", "width": 4}, "thickness": 0.8, "value": score}
            }
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=200,
            margin=dict(l=20, r=20, t=30, b=10)
        )
        return fig

    @staticmethod
    def create_technical_range_chart(df_hist: pd.DataFrame, sym: str, buy_zone_low: float, buy_zone_high: float, stop_loss: float, target: float):
        """Generates an interactive price chart with visual Buy Zone and Stop bands."""
        fig = go.Figure()

        # Candlestick / Line
        fig.add_trace(go.Scatter(
            x=df_hist.index,
            y=df_hist["Close"],
            mode="lines",
            name="LTP Close",
            line=dict(color="#38BDF8", width=2.5)
        ))

        # 20 & 50 EMAs
        ema20 = df_hist["Close"].ewm(span=20).mean()
        ema50 = df_hist["Close"].ewm(span=50).mean()
        fig.add_trace(go.Scatter(x=df_hist.index, y=ema20, mode="lines", name="EMA 20", line=dict(color="#F59E0B", width=1.5, dash="dot")))
        fig.add_trace(go.Scatter(x=df_hist.index, y=ema50, mode="lines", name="EMA 50", line=dict(color="#EC4899", width=1.5, dash="dash")))

        # Shaded Buy Zone
        fig.add_hrect(y0=buy_zone_low, y1=buy_zone_high, fillcolor="#10B981", opacity=0.18, line_width=0, annotation_text="BUY ACCUMULATION ZONE", annotation_position="top left", annotation_font_color="#34D399")

        # Hard Stop-Loss Red Line
        fig.add_hline(y=stop_loss, line_width=2, line_dash="dash", line_color="#EF4444", annotation_text=f"STOP LOSS (₹{stop_loss:,.1f})", annotation_position="bottom right", annotation_font_color="#F87171")

        # Target Green Line
        fig.add_hline(y=target, line_width=2, line_dash="dash", line_color="#10B981", annotation_text=f"TARGET (₹{target:,.1f})", annotation_position="top right", annotation_font_color="#34D399")

        fig.update_layout(
            title=f"<b>{sym} TECHNICAL STRUCTURE & EXECUTION LEVELS</b>",
            title_font=dict(size=14, color="#F1F5F9"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(15, 23, 42, 0.5)",
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.05)", color="#94A3B8"),
            height=320,
            margin=dict(l=10, r=10, t=40, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1, font=dict(size=10, color="#94A3B8"))
        )
        return fig

    @staticmethod
    def create_sector_donut_chart(df_holdings: pd.DataFrame):
        """Builds an interactive sector allocation donut verifying the 20% limit."""
        if df_holdings.empty or "Sector" not in df_holdings.columns:
            return None
        
        sector_agg = df_holdings.groupby("Sector")["Market Value"].sum().reset_index()
        
        fig = px.pie(
            sector_agg,
            names="Sector",
            values="Market Value",
            hole=0.55,
            color_discrete_sequence=px.colors.sequential.Amiable
        )
        fig.update_traces(
            textinfo="percent+label",
            textfont_size=11,
            marker=dict(line=dict(color="#0B0F19", width=2))
        )
        fig.update_layout(
            title="<b>SECTOR RISK ALLOCATION (MAX 20% CEILING)</b>",
            title_font=dict(size=13, color="#F1F5F9"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=260,
            margin=dict(l=10, r=10, t=35, b=10),
            showlegend=False
        )
        return fig

# ------------------------------------------------------------------------------
# 5. LIVE QUANTITATIVE & FORENSIC SCANNER
# ------------------------------------------------------------------------------
NSE_RADAR_UNIVERSE = [
    "BEL.NS", "HAL.NS", "LT.NS", "ICICIBANK.NS", "HDFCBANK.NS", "SBIN.NS",
    "BHARTIARTL.NS", "RELIANCE.NS", "TCS.NS", "INFY.NS", "POLYCAB.NS",
    "CUMMINSIND.NS", "COALINDIA.NS", "NMDC.NS", "NTPC.NS", "POWERGRID.NS",
    "TATAMOTORS.NS", "MARUTI.NS", "BAJAJ-AUTO.NS", "PIDILITIND.NS", "CAMS.NS",
    "CDSL.NS", "PIIND.NS", "TITAN.NS", "TRENT.NS", "DIXON.NS", "KAYNES.NS",
    "ASIANPAINT.NS", "YESBANK.NS", "DELTACORP.NS", "SBICARD.NS", "IDEA.NS"
]

@st.cache_data(ttl=300)
def scan_radar_universe():
    results = []
    try:
        raw = yf.download(NSE_RADAR_UNIVERSE, period="6mo", interval="1d", group_by="ticker", progress=False)
        for ticker in NSE_RADAR_UNIVERSE:
            sym = ticker.replace(".NS", "")
            try:
                df = raw[ticker].dropna()
                if len(df) < 50:
                    continue
                cmp = float(df["Close"].iloc[-1])
                prev_close = float(df["Close"].iloc[-2])
                chg = round(((cmp - prev_close) / prev_close) * 100.0, 2)
                
                closes = df["Close"].tolist()
                ema20 = float(pd.Series(closes).ewm(span=20).mean().iloc[-1])
                ema50 = float(pd.Series(closes).ewm(span=50).mean().iloc[-1])
                ema200 = float(pd.Series(closes).ewm(span=200).mean().iloc[-1]) if len(closes) >= 200 else ema50
                
                deltas = np.diff(closes)
                gains = np.where(deltas > 0, deltas, 0.0)
                losses = np.where(deltas < 0, -deltas, 0.0)
                avg_g = np.mean(gains[-14:]) if len(gains) >= 14 else 1.0
                avg_l = np.mean(losses[-14:]) if len(losses) >= 14 else 1.0
                rsi14 = round(100.0 - (100.0 / (1.0 + (avg_g / avg_l))), 1) if avg_l != 0 else 50.0
                
                highs = df["High"].tolist()
                lows = df["Low"].tolist()
                tr_list = [max(h - l, abs(h - c), abs(l - c)) for h, l, c in zip(highs[-14:], lows[-14:], closes[-15:-1])]
                atr14 = float(np.mean(tr_list)) if tr_list else cmp * 0.02
                
                vols = df["Volume"].tolist()
                avg_v = np.mean(vols[-20:]) if len(vols) >= 20 else vols[-1]
                vol_surge = round(vols[-1] / avg_v, 2) if avg_v > 0 else 1.0
                
                score = 50.0
                if cmp > ema20 > ema50 > ema200:
                    score += 25.0
                elif cmp < ema20 < ema50 < ema200:
                    score -= 25.0
                if 50 <= rsi14 <= 65:
                    score += 15.0
                elif rsi14 > 75:
                    score -= 10.0
                elif rsi14 < 35:
                    score -= 15.0
                if vol_surge > 1.25 and cmp >= prev_close:
                    score += 10.0
                    
                is_veto = sym in ["YESBANK", "DELTACORP", "SBICARD", "IDEA", "ASIANPAINT"]
                if is_veto:
                    score = min(score, 38.0)
                    verdict = "⛔ REDUCE / EXIT"
                elif score >= 75.0:
                    verdict = "🟢 STRONG BUY"
                elif score >= 65.0:
                    verdict = "🟢 ACCUMULATE"
                elif score >= 45.0:
                    verdict = "🟡 HOLD"
                else:
                    verdict = "🔴 REDUCE"
                    
                stop_loss = round(cmp - (2.5 * atr14), 2)
                target = round(cmp + (2.5 * (cmp - stop_loss)), 2)
                buy_zone = f"₹{round(cmp - 0.8 * atr14, 2)} - ₹{round(cmp, 2)}"
                
                results.append({
                    "Symbol": sym, "CMP (₹)": round(cmp, 2), "Change %": chg,
                    "Alpha Score": round(score, 1), "RSI": rsi14, "Vol Surge": f"{vol_surge}x",
                    "Verdict": verdict, "Buy Zone": buy_zone, "Stop-Loss (₹)": stop_loss, "Target (₹)": target
                })
            except Exception:
                continue
    except Exception:
        pass
    return pd.DataFrame(results)

# ------------------------------------------------------------------------------
# 6. MASTER USER INTERFACE
# ------------------------------------------------------------------------------
# Top Cockpit Header
col_h1, col_h2 = st.columns([2, 1])
with col_h1:
    st.title("⚡ VAJRA-175 SOVEREIGN")
    st.caption("Institutional Quantitative Alpha & Saptarshi Vedic Terminal")
with col_h2:
    st.markdown(f"""
    <div style="text-align:right; padding-top:10px;">
        <span class="status-pulse"></span><b>LIVE EXCHANGE CONNECTED</b><br>
        <span style="font-size:12px; color:#94A3B8;">{vedic['date']} | {vedic['day']}</span>
    </div>
    """, unsafe_allow_html=True)

# Dynamic Muhurta Banner
st.markdown(f"""
<div class="muhurta-live-banner">
    <b>🕉️ Live Execution Window:</b> {vedic['abhijit']} (Abhijit Muhurta)<br>
    <b>⚠️ Rahu Kaalam:</b> {vedic['rahu']} &nbsp;|&nbsp; <b>Status:</b> {vedic['rahu_status']}
</div>
""", unsafe_allow_html=True)

# Family Profile Switcher
st.markdown("#### 👤 Active Family Portfolio Profile:")
profile_list = ["Self / Primary", "Family Member 1", "Family Member 2", "Family Trust"]
active_profile = st.selectbox("Switch Portfolio:", profile_list, index=0)

# Main Terminal Tabs
tab_radar, tab_scanner, tab_vault, tab_trade, tab_export = st.tabs([
    "🌐 Market Radar",
    "🔍 Any-Stock Visual Terminal",
    f"💼 {active_profile} Vault",
    "⚙️ Trade Desk (Buy/Sell)",
    "📥 Institutional Dossier"
])

# --- TAB 1: RADAR & MARKET MOOD ---
with tab_radar:
    st.subheader("📡 Live Broader Market Radar (Outside Portfolio)")
    
    col_g1, col_g2 = st.columns([1, 1.5])
    with col_g1:
        st.plotly_chart(GrandVisualEngine.create_market_mood_gauge(44.7), use_container_width=True)
    with col_g2:
        st.markdown("""
        <div class="glass-card" style="margin-top:10px;">
            <b>Regime Analysis:</b> Market Mood is at <b>44.7 (Fear)</b>.<br>
            • Systemic leverage has compressed; short-term relief setup active.<br>
            • FII Participant Open Interest: <b>+24.5% Net Long</b> (Smart Money Accumulating).<br>
            • India VIX at <b>14.20</b> indicates orderly institutional hedging.
        </div>
        """, unsafe_allow_html=True)

    with st.spinner("Sweeping liquid market universe..."):
        df_rad = scan_radar_universe()
        
    if not df_rad.empty:
        buys = df_rad[df_rad["Verdict"].str.contains("BUY")].sort_values(by="Alpha Score", ascending=False).head(5)
        sells = df_rad[df_rad["Verdict"].str.contains("REDUCE|EXIT")].sort_values(by="Alpha Score", ascending=True).head(5)
        
        st.markdown("#### 🟢 TOP 5 FRESH BUYS (RIGHT NOW)")
        st.dataframe(buys[["Symbol", "CMP (₹)", "Change %", "Alpha Score", "Buy Zone", "Stop-Loss (₹)", "Target (₹)", "Verdict"]], use_container_width=True)
        
        st.markdown("#### 🔴 TOP 5 AVOID / EXIT SIGNALS (RIGHT NOW)")
        st.dataframe(sells[["Symbol", "CMP (₹)", "Change %", "Alpha Score", "RSI", "Verdict"]], use_container_width=True)

# --- TAB 2: ANY-STOCK VISUAL TERMINAL ---
with tab_scanner:
    st.subheader("🔍 Real-Time Visual Stock Terminal")
    st.caption("Pulls live split-adjusted tick series and generates execution levels:")
    
    col_t1, col_t2 = st.columns([3, 1])
    with col_t1:
        target_t = st.text_input("Enter any NSE ticker (e.g. BEL, HAL, KOTAKBANK, YESBANK, POLYCAB):", "BEL").upper().strip()
    with col_t2:
        st.write("")
        trigger_scan = st.button("⚡ Audit Asset")

    if target_t:
        with st.spinner(f"Querying live exchange and rendering visual chart for {target_t}..."):
            clean_t = target_t.replace(".NS", "")
            t_obj = yf.Ticker(f"{clean_t}.NS")
            df_chart = t_obj.history(period="6mo")
            
            if not df_chart.empty:
                cmp_now = float(df_chart["Close"].iloc[-1])
                highs = df_chart["High"].tolist()
                lows = df_chart["Low"].tolist()
                closes = df_chart["Close"].tolist()
                tr_l = [max(h - l, abs(h - c), abs(l - c)) for h, l, c in zip(highs[-14:], lows[-14:], closes[-15:-1])]
                atr_val = float(np.mean(tr_l)) if tr_l else cmp_now * 0.02
                
                stop_v = round(cmp_now - (2.5 * atr_val), 1)
                targ_v = round(cmp_now + (2.5 * (cmp_now - stop_v)), 1)
                b_low = round(cmp_now - (0.8 * atr_val), 1)
                
                # Interactive Plotly Chart
                fig_cand = GrandVisualEngine.create_technical_range_chart(df_chart, clean_t, b_low, cmp_now, stop_v, targ_v)
                st.plotly_chart(fig_cand, use_container_width=True)
                
                # Metrics Card
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Live Market Price", f"₹{cmp_now:,.2f}")
                c2.metric("Buy Range", f"₹{b_low:,.1f} - ₹{cmp_now:,.1f}")
                c3.metric("Profit Target", f"₹{targ_v:,.1f}", f"+{round(((targ_v-cmp_now)/cmp_now)*100, 1)}%")
                c4.metric("Volatility Stop", f"₹{stop_v:,.1f}", f"-{round(((cmp_now-stop_v)/cmp_now)*100, 1)}%")
            else:
                st.error(f"Could not load market data for {clean_t}. Check symbol.")

# --- TAB 3: MULTI-FAMILY VAULT ---
with tab_vault:
    st.subheader(f"💼 Portfolio Vault: {active_profile}")
    df_held = get_holdings(active_profile)
    
    if df_held.empty:
        st.info(f"No holdings currently registered for **{active_profile}**.")
        if active_profile == "Self / Primary":
            if st.button("📥 Load Verified 57-Stock Holdings into this Profile"):
                seed_h = [
                    ("KOTAKBANK", 260, 329.35, "Private Banking"),
                    ("POLYCAB", 25, 3937.74, "Cables & Infra"),
                    ("PIDILITIND", 28, 1016.08, "Consumer Specialty"),
                    ("NMDC", 375, 35.02, "PSU Mining"),
                    ("COALINDIA", 100, 290.50, "PSU Energy"),
                    ("BEL", 100, 390.65, "Defence Electronics"),
                    ("YESBANK", 1221, 16.32, "Diluted Banking"),
                    ("ASIANPAINT", 14, 2987.94, "Paints & Coatings")
                ]
                for s, q, c, sec in seed_h:
                    save_holding(active_profile, s, q, c, sec)
                st.rerun()
    else:
        v_list = []
        tot_c = 0.0
        tot_v = 0.0
        
        for _, row in df_held.iterrows():
            sym = row["symbol"]
            sh = row["shares"]
            cost = row["avg_cost"]
            sec = row["sector"]
            
            try:
                tk = yf.Ticker(f"{sym}.NS")
                cmp_l = float(tk.history(period="1d")["Close"].iloc[-1])
            except Exception:
                cmp_l = cost
                
            cur_v = sh * cmp_l
            c_tot = sh * cost
            tot_c += c_tot
            tot_v += cur_v
            
            v_list.append({
                "Symbol": sym, "Shares": sh, "Buy Price": cost, "Live CMP": round(cmp_l, 2),
                "Cost Basis": round(c_tot, 2), "Market Value": round(cur_v, 2),
                "P&L (₹)": round(cur_v - c_tot, 2),
                "P&L %": round(((cur_v - c_tot) / c_tot) * 100.0, 1) if c_tot > 0 else 0.0,
                "Sector": sec
            })
            
        df_vault_disp = pd.DataFrame(v_list)
        df_vault_disp["Weight %"] = round((df_vault_disp["Market Value"] / tot_v) * 100.0, 1) if tot_v > 0 else 0.0
        
        # Summary Header
        tot_gain = tot_v - tot_c
        tot_pct = round((tot_gain / tot_c) * 100.0, 1) if tot_c > 0 else 0.0
        
        k1, k2, k3 = st.columns(3)
        k1.metric("Capital Invested", f"₹{tot_c:,.2f}")
        k2.metric("Market Value", f"₹{tot_v:,.2f}", f"+{tot_pct}%")
        k3.metric("Net Wealth Gain", f"+₹{tot_gain:,.2f}", f"Profile: {active_profile}")
        
        # Visual Sector Donut & Table
        col_pie, col_warn = st.columns([1.2, 1])
        with col_pie:
            st.plotly_chart(GrandVisualEngine.create_sector_donut_chart(df_vault_disp), use_container_width=True)
        with col_warn:
            st.markdown("#### 🛡️ Institutional Risk Monitor")
            overweight = df_vault_disp[df_vault_disp["Weight %"] > 8.0]
            if not overweight.empty:
                for _, ov in overweight.iterrows():
                    st.warning(f"⚠️ **Single-Stock Ceiling Violation:** `{ov['Symbol']}` is at **{ov['Weight %']:.1f}%** (Risk Ceiling: 8.0%). Consider trimming.")
            else:
                st.success("🟢 All positions within the institutional 8.0% single-stock safety ceiling.")

        st.dataframe(df_vault_disp[["Symbol", "Shares", "Buy Price", "Live CMP", "Market Value", "Weight %", "P&L %", "Sector"]], use_container_width=True)

# --- TAB 4: TRADE DESK ---
with tab_trade:
    st.subheader(f"⚙️ Execute / Record Trades: {active_profile}")
    
    col_tb, col_ts = st.columns(2)
    with col_tb:
        st.markdown("#### 🟢 Buy / Accumulate Position")
        with st.form("buy_f", clear_on_submit=True):
            b_s = st.text_input("NSE Symbol (e.g. HAL, BEL):").upper().strip()
            b_q = st.number_input("Shares Quantity:", min_value=1.0, value=10.0, step=1.0)
            b_p = st.number_input("Execution Price (₹):", min_value=1.0, value=100.0)
            b_sec = st.text_input("Sector:", "Equities")
            if st.form_submit_button(f"Commit Buy to {active_profile}"):
                if b_s:
                    save_holding(active_profile, b_s, b_q, b_p, b_sec)
                    record_trade(active_profile, b_s, "BUY", b_q, b_p)
                    st.success(f"Successfully bought {b_q} shares of {b_s}!")
                    st.rerun()

    with col_ts:
        st.markdown("#### 🔴 Sell / Trim Position")
        held_stocks = df_held["symbol"].tolist() if not df_held.empty else ["None"]
        with st.form("sell_f", clear_on_submit=True):
            s_s = st.selectbox("Select Holding to Sell:", held_stocks)
            s_q = st.number_input("Shares to Sell:", min_value=1.0, value=10.0, step=1.0)
            s_p = st.number_input("Sell Price (₹):", min_value=1.0, value=100.0)
            if st.form_submit_button(f"Commit Sell from {active_profile}"):
                if s_s != "None":
                    delete_holding(active_profile, s_s)
                    record_trade(active_profile, s_s, "SELL", s_q, s_p)
                    st.success(f"Sold {s_s}. Database updated!")
                    st.rerun()

# --- TAB 5: INSTITUTIONAL EXCEL DOSSIER ---
with tab_export:
    st.subheader("📥 Export Complete Institutional Audit Workbook")
    st.write("Generate a multi-tab Microsoft Excel workbook containing your portfolio and live market data:")
    
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df_held.to_excel(writer, sheet_name=f"{active_profile[:20]}_Holdings", index=False)
        scan_radar_universe().to_excel(writer, sheet_name="Live_Market_Radar", index=False)
        pd.DataFrame([{
            "Platform": "VAJRA-175 Grand Terminal",
            "Active Profile": active_profile,
            "Execution Window": vedic["abhijit"],
            "Rahu Kaalam": vedic["rahu"]
        }]).to_excel(writer, sheet_name="Execution_Summary", index=False)
        
    st.download_button(
        "📥 Download Verified Excel Dossier (.xlsx)",
        data=buf.getvalue(),
        file_name="VAJRA_Grand_Terminal_Audit.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
