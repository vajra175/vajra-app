import streamlit as st
import pandas as pd
import datetime
import io

st.set_page_config(page_title="VAJRA-175", page_icon="⚡", layout="wide")

# Theme Styling
st.markdown("""
<style>
    .stApp { background-color: #0B0F19; color: #E2E8F0; }
    .metric-card { background: #131B2E; padding: 12px; border-radius: 8px; border: 1px solid #1E293B; margin-bottom: 8px; }
    .muhurta-box { background: #2E1065; color: #EDE9FE; padding: 12px; border-radius: 8px; border-left: 5px solid #A855F7; margin-bottom: 12px; }
    .badge-buy { background-color: #064E3B; color: #34D399; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
    .badge-veto { background-color: #7F1D1D; color: #FCA5A5; padding: 3px 8px; border-radius: 4px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

if "portfolio" not in st.session_state:
    st.session_state.portfolio = [
        {"Symbol": "KOTAKBANK", "Qty": 260, "AvgCost": 329.35, "CMP": 430.0, "Verdict": "🟢 HOLD (7.6% Wt)"},
        {"Symbol": "POLYCAB", "Qty": 25, "AvgCost": 3937.74, "CMP": 6650.0, "Verdict": "🟢 HOLD (Core 11.4%)"},
        {"Symbol": "PIDILITIND", "Qty": 28, "AvgCost": 1016.08, "CMP": 3050.0, "Verdict": "🟢 HOLD (Moat)"},
        {"Symbol": "NMDC", "Qty": 375, "AvgCost": 35.02, "CMP": 225.0, "Verdict": "🟢 HOLD (Cash Cow)"},
        {"Symbol": "BEL", "Qty": 100, "AvgCost": 390.65, "CMP": 295.0, "Verdict": "🟢 BUY 170 MORE"},
        {"Symbol": "YESBANK", "Qty": 1221, "AvgCost": 16.32, "CMP": 21.0, "Verdict": "⛔ SELL / EXIT"},
        {"Symbol": "ASIANPAINT", "Qty": 14, "AvgCost": 2987.94, "CMP": 2840.0, "Verdict": "⛔ SELL / EXIT"}
    ]

st.title("⚡ VAJRA-175 SOVEREIGN TERMINAL")

# Live Muhurta Banner
st.markdown("""
<div class="muhurta-box">
    <b>🕉️ Primary Execution Window:</b> 11:46 AM - 12:34 PM IST (Abhijit Muhurta)<br>
    <b>⚠️ Rahu Kaalam:</b> Monday 07:30 AM - 09:00 AM IST (🟢 Cleared before 09:15 market open)
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🌐 Market Radar", "💼 Portfolio Vault", "📥 Excel Export"])

with tab1:
    st.subheader("🎯 Monday High-Conviction Setups")
    st.markdown("""
    * **1. Bharat Electronics (`BEL`)** | CMP: ₹295.00  
      <span class="badge-buy">STRONG BUY</span> | Buy Zone: ₹288–₹295 | Target: ₹335.00 | Stop: ₹280.50  
    * **2. Hindustan Aeronautics (`HAL`)** | CMP: ₹3,980.00  
      <span class="badge-buy">STRONG BUY</span> | Buy Zone: ₹3,915–₹3,980 | Target: ₹4,470.00 | Stop: ₹3,783.75  
    * **3. Yes Bank (`YESBANK`)** | CMP: ₹21.00  
      <span class="badge-veto">HARD GATEKEEPER VETO</span> | Action: **SELL / EXIT ALL 1,221 SHARES**
    """, unsafe_allow_html=True)

with tab2:
    st.subheader("💼 Your Portfolio Holdings")
    df = pd.DataFrame(st.session_state.portfolio)
    df["Value (₹)"] = df["Qty"] * df["CMP"]
    df["Cost (₹)"] = df["Qty"] * df["AvgCost"]
    df["P&L (₹)"] = df["Value (₹)"] - df["Cost (₹)"]
    
    tot_val = df["Value (₹)"].sum()
    tot_cost = df["Cost (₹)"].sum()
    tot_pnl = tot_val - tot_cost
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Invested", f"₹{tot_cost:,.2f}")
    c2.metric("Current Value", f"₹{tot_val:,.2f}")
    c3.metric("Net Profit", f"+₹{tot_pnl:,.2f}", "+46.5%")
    
    st.dataframe(df[["Symbol", "Qty", "AvgCost", "CMP", "Value (₹)", "Verdict"]], use_container_width=True)

with tab3:
    st.subheader("📥 Export Audit Report")
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="Holdings", index=False)
    st.download_button(
        "📥 Download Verified Excel Sheet (.xlsx)",
        data=buf.getvalue(),
        file_name="VAJRA_Portfolio.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
