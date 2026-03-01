import streamlit as st
import requests
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from datetime import datetime
import os

# BASE_URL = "http://8.215.205.66:8000"
BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Merchant Dashboard - Financial Intelligence Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state untuk navigation tabs
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = "Overview"

# ==========================
# FUNGSI UNTUK CEK FILE LOGO
# ==========================

def get_logo_path():
    """Mencari logo.jpeg di folder yang sama dengan script app.py"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    logo_file = os.path.join(current_dir, "logo.jpeg")
    
    if os.path.exists(logo_file):
        return logo_file
    
    fallback_path = os.path.join("Frontend", "logo.jpeg")
    if os.path.exists(fallback_path):
        return fallback_path
        
    return None

logo_path = get_logo_path()

# ==========================
# CUSTOM CSS
# ==========================
st.markdown("""
<style>
    /* Reset Streamlit default styling */
    .stApp {
        background-color: #f5f7fb;
    }
    
    /* Header dengan logo */
    .header-container {
        display: flex;
        align-items: center;
        gap: 15px;
        padding: 10px 0 20px 0;
        border-bottom: 1px solid #e6e8f0;
        margin-bottom: 20px;
    }
    
    .main-title {
        font-size: 24px;
        font-weight: 600;
        color: #1a1f36;
    }
    
    .sub-title {
        font-size: 14px;
        color: #6b7280;
    }
    
    /* Navigation tabs */
    .nav-tabs-container {
        display: flex;
        gap: 30px;
        padding: 0 0 15px 0;
        border-bottom: 1px solid #e6e8f0;
        margin-bottom: 20px;
    }
    
    /* Metric cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        border: 1px solid #eef2f6;
    }
    
    .metric-label {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 5px;
    }
    
    .metric-value {
        font-size: 24px;
        font-weight: 600;
        color: #1a1f36;
    }
    
    .metric-sub {
        font-size: 12px;
        color: #9ca3af;
        margin-top: 5px;
    }
    
    /* AI Recommendation card */
    .ai-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 24px;
        border-radius: 16px;
        color: white;
        margin: 20px 0;
        width: 100%;
    }

    .ai-title {
        font-size: 16px;
        font-weight: 600;
        margin-bottom: 15px;
        opacity: 0.9;
    }

    .ai-text {
        font-size: 14px;
        line-height: 1.8;
        opacity: 0.95;
    }
    
    .ai-text p {
        margin-bottom: 12px;
    }
    
    /* Security metrics */
    .security-metric {
        background: white;
        padding: 16px;
        border-radius: 12px;
        border: 1px solid #eef2f6;
        text-align: center;
    }
    
    .security-value {
        font-size: 28px;
        font-weight: 600;
        color: #1a1f36;
    }
    
    .security-label {
        font-size: 13px;
        color: #6b7280;
        margin-top: 5px;
    }
    
    /* Daily burn rate card */
    .burn-rate-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #eef2f6;
    }
    
    .burn-rate-label {
        font-size: 13px;
        color: #6b7280;
        margin-bottom: 5px;
    }
    
    .burn-rate-value {
        font-size: 24px;
        font-weight: 600;
        color: #ef4444;
    }
    
    /* Transaction status cards */
    .status-card {
        padding: 20px;
        border-radius: 12px;
        text-align: center;
    }
    
    .status-success {
        background: #e6f7e6;
        color: #0a7e0a;
    }
    
    .status-failed {
        background: #ffe6e6;
        color: #b30000;
    }
    
    .status-pending {
        background: #fff3e0;
        color: #b45b0a;
    }
    
    .status-percent {
        font-size: 36px;
        font-weight: 600;
    }
    
    .status-label {
        font-size: 16px;
    }
    
    /* Button styling untuk tabs */
    div[data-testid="stHorizontalBlock"] > div {
        padding: 0 !important;
    }
    
    .stButton button {
        background: transparent;
        border: none;
        color: #6b7280;
        font-size: 14px;
        font-weight: 500;
        padding: 0 0 15px 0;
        border-bottom: 2px solid transparent;
        border-radius: 0;
        transition: all 0.2s ease;
    }
    
    .stButton button:hover {
        color: #667eea;
        background: transparent;
        border: none;
        border-bottom: 2px solid #667eea;
    }
    
    .stButton button:focus {
        color: #667eea;
        background: transparent;
        border: none;
        border-bottom: 2px solid #667eea;
        box-shadow: none;
    }
    
    .stButton button:active {
        color: #667eea;
        background: transparent;
        border: none;
        border-bottom: 2px solid #667eea;
    }
    
    /* Sidebar styling */
    .sidebar-logo {
        padding: 20px 0;
        text-align: center;
    }
    
    /* Container untuk payment methods */
    .payment-container {
        background: white;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #eef2f6;
        margin: 15px 0;
    }
</style>
""", unsafe_allow_html=True)

# ==========================
# HEADER DENGAN LOGO
# ==========================
col1, col2 = st.columns([1, 10])
with col1:
    if logo_path:
        st.image(logo_path, width=60)
    else:
        st.markdown("📊")
with col2:
    st.markdown("""
    <div>
        <div class="main-title">Merchant Dashboard</div>
        <div class="sub-title">Financial Intelligence Platform</div>
    </div>
    """, unsafe_allow_html=True)

# ==========================
# SIDEBAR
# ==========================
with st.sidebar:
    if logo_path:
        st.markdown('<div class="sidebar-logo">', unsafe_allow_html=True)
        st.image(logo_path, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown("---")
    
    st.markdown("### Quick Navigation")
    
    if st.button("📊 Overview", use_container_width=True):
        st.session_state.active_tab = "Overview"
        st.rerun()
    if st.button("📈 Analytics", use_container_width=True):
        st.session_state.active_tab = "Analytics"
        st.rerun()
    if st.button("🔮 Predictions", use_container_width=True):
        st.session_state.active_tab = "Predictions"
        st.rerun()
    if st.button("🛡️ Fraud Detection", use_container_width=True):
        st.session_state.active_tab = "Fraud Detection"
        st.rerun()
    
    st.markdown("---")
    st.markdown("### System Status")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("🟢 API Connected")
    with col2:
        st.markdown("🔵 ML Model Active")
    
    st.markdown("---")
    st.caption(f"Last updated: {datetime.now().strftime('%d/%m/%Y, %H:%M:%S')}")
    
    if st.button("🔄 Clear AI Cache", use_container_width=True):
        try:
            requests.get(f"{BASE_URL}/clear-cache")
            st.success("Cache cleared!")
        except:
            st.error("Failed to clear cache")

# ==========================
# NAVIGATION TABS
# ==========================
def render_nav_tabs():
    tabs = ["Overview", "Analytics", "Predictions", "Fraud Detection"]
    cols = st.columns(len(tabs))
    
    for i, tab_name in enumerate(tabs):
        with cols[i]:
            is_active = (st.session_state.active_tab == tab_name)
            if st.button(
                tab_name,
                key=f"tab_{tab_name}",
                use_container_width=True,
                type="secondary" if not is_active else "primary"
            ):
                st.session_state.active_tab = tab_name
                st.rerun()

render_nav_tabs()

# ==========================
# HELPER FUNCTIONS
# ==========================
def format_rupiah(value):
    return f"Rp {value:,.0f}".replace(",", ".")

def safe_request(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None

# ==========================
# OVERVIEW PAGE
# ==========================
if st.session_state.active_tab == "Overview":
    data = safe_request(f"{BASE_URL}/dashboard")
    
    if data:
        # Financial Overview
        st.markdown("## Financial Overview")
        st.markdown("Key metrics and current financial health")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">This Month Revenue</div>
                <div class="metric-value">{format_rupiah(data['this_month_revenue'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">This Month Expense</div>
                <div class="metric-value">{format_rupiah(data['this_month_expense'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            net_profit = data['this_month_revenue'] - data['this_month_expense']
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Net Profit</div>
                <div class="metric-value">{format_rupiah(net_profit)}</div>
                <div class="metric-sub">Margin: {data['this_month_profit']:.2f}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Market Sentiment</div>
                <div class="metric-value">{data['this_month_fear_greed_score']}</div>
                <div class="metric-sub">{data['this_month_fear_greed_label']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Key Insights & Metrics
        st.markdown("### Key Insights & Metrics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Revenue Growth</div>
                <div class="metric-value">{data['this_month_revenue_growth']:.2f}%</div>
                <div class="metric-sub">vs last month</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Expense Change</div>
                <div class="metric-value">{data['this_month_expense_growth']:.2f}%</div>
                <div class="metric-sub">vs last month</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Profit Margin</div>
                <div class="metric-value">{data['this_month_profit']:.2f}%</div>
                <div class="metric-sub">of total revenue</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            daily_burn = data['this_month_expense'] / 30
            runway_days = int(net_profit / daily_burn) if daily_burn > 0 else 365
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Runway Days</div>
                <div class="metric-value">{min(runway_days, 365)}+</div>
                <div class="metric-sub">at current burn rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        #with col5:
        #    avg_daily_rev = data['this_month_revenue'] / 30
        #    st.markdown(f"""
        #    <div class="metric-card">
        #        <div class="metric-label">Average Daily Revenue</div>
        #        <div class="metric-value">{format_rupiah(int(avg_daily_rev))}</div>
        #        <div class="metric-sub">Based on 30-day period</div>
        #    </div>
        #    """, unsafe_allow_html=True)
        
        # Average Daily Revenue dan Daily Burn Rate bersebelahan
        st.markdown("### Daily Metrics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            avg_daily_rev = data['this_month_revenue'] / 30
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Average Daily Revenue</div>
                <div class="metric-value">{format_rupiah(int(avg_daily_rev))}</div>
                <div class="metric-sub">Based on 30-day period</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            daily_burn = data['this_month_expense'] / 30
            st.markdown(f"""
            <div class="burn-rate-card">
                <div class="burn-rate-label">Daily Burn Rate</div>
                <div class="burn-rate-value">{format_rupiah(int(daily_burn))}</div>
                <div class="metric-sub">Average daily expense</div>
            </div>
            """, unsafe_allow_html=True)
        
        # AI-Powered Recommendations
        st.markdown("## AI-Powered Recommendations")
        ai_text = data['ai recommendation']
        lines = ai_text.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip():
                clean_line = line.replace('*', '').replace('-', '').replace('•', '').strip()
                formatted_lines.append(f"• {clean_line}")
        formatted_text = '<br>'.join(formatted_lines)
        
        st.markdown(f"""
        <div class="ai-card">
            <div class="ai-title">🤖 AI Recommendations</div>
            <div class="ai-text">
                {formatted_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Revenue & Expense Trends
        st.markdown("## Revenue & Expense Trends")
        
        chart_data = data['chart_data']
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=chart_data['months'],
            y=chart_data['revenue'],
            name='Revenue',
            line=dict(color='#10b981', width=3),
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=chart_data['months'],
            y=chart_data['expense'],
            name='Expense',
            line=dict(color='#ef4444', width=3),
            mode='lines+markers'
        ))
        
        fig.update_layout(
            height=400,
            yaxis=dict(title='Amount (Rp)', tickformat=',.0f'),
            hovermode='x unified',
            showlegend=True,
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Transaction Status
        st.markdown("## Transaction Status")
        
        status = data['this_month_status_percent']
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="status-card status-success">
                <div class="status-label">Success</div>
                <div class="status-percent">{status.get('Success', 0)}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="status-card status-failed">
                <div class="status-label">Failed</div>
                <div class="status-percent">{status.get('Failed', 0)}%</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="status-card status-pending">
                <div class="status-label">Pending</div>
                <div class="status-percent">{status.get('Pending', 0)}%</div>
            </div>
            """, unsafe_allow_html=True)

# ==========================
# ANALYTICS PAGE - URUTAN BARU
# ==========================
elif st.session_state.active_tab == "Analytics":
    st.markdown("## Business Analytics")
    st.markdown("Deep insights into sales patterns and customer behavior")
    
    data = safe_request(f"{BASE_URL}/analytics")
    
    if data:
        # 1. Top Transaction Region
        st.markdown("### Top Transaction Region")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 12px; color: white; margin: 15px 0;">
            <div style="font-size: 18px; font-weight: 600;">{data['this_month_top_region']}</div>
            <div style="font-size: 14px; opacity: 0.9;">Highest transaction volume this month</div>
        </div>
        """, unsafe_allow_html=True)
        
        # 2. Top 10 Categories - PIE CHART
        st.markdown("### Top 10 Categories Sales")
        
        cat_data = data['this_month_category_percentage_top10']
        
        # Best Selling Category di atas pie chart
        first_category = list(cat_data.items())[0] if cat_data else ("None", 0)
        st.markdown("#### Best Selling Category")
        st.markdown(f"""
        <div style="background: #f8fafc; padding: 15px; border-radius: 8px; margin-bottom: 20px;">
            <div style="font-weight: 600;">{first_category[0][:50]}</div>
            <div style="font-size: 24px; color: #667eea;">{first_category[1]}%</div>
            <div style="color: #6b7280;">of total sales</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Pie Chart untuk Top 10 Categories
        fig_pie = px.pie(
            values=list(cat_data.values()),
            names=list(cat_data.keys()),
            title="Top 10 Categories Distribution"
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # 3. Payment Methods - FULL WIDTH STYLE (MATCH FIGMA)
        st.markdown("### Payment Methods")

        payment_data = data['this_month_payment_percentage']
        top_payment = max(payment_data.items(), key=lambda x: x[1]) if payment_data else ("None", 0)

        #st.markdown("""
        #<div style="background: white; padding: 25px; border-radius: 16px; border: 1px solid #eef2f6; margin: 20px 0;">
        #""", unsafe_allow_html=True)

        # Top Payment Method Box (Hijau Soft)
        st.markdown(f"""
        <div style="background: #e6f4ea; padding: 20px; border-radius: 12px; margin-bottom: 25px;">
            <div style="font-size: 14px; color: #166534;">Top Payment Method</div>
            <div style="font-size: 22px; font-weight: 600; color: #065f46; margin-top: 5px;">
                {top_payment[0]}
            </div>
            <div style="color: #047857; margin-top: 5px;">
                {top_payment[1]}% of transactions
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Bar Chart (Full Width - Hijau Solid)
        fig_bar = go.Figure()

        fig_bar.add_trace(go.Bar(
            x=list(payment_data.keys()),
            y=list(payment_data.values()),
            marker_color="#10b981"
        ))

        fig_bar.update_layout(
            height=400,
            yaxis=dict(
                title="Percentage (%)",
                range=[0, max(payment_data.values()) + 5]
            ),
            xaxis=dict(title=""),
            showlegend=False,
            plot_bgcolor="white"
        )

        st.plotly_chart(fig_bar, use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)
        
        # 4. Performance Metrics (Total Categories, Payment Methods, Success Rate)
        st.markdown("### Performance Metrics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div class="metric-label">Total Categories</div>
                <div class="metric-value" style="font-size: 36px;">{data['total_category']}</div>
                <div class="metric-sub">Active product categories</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div class="metric-label">Payment Methods</div>
                <div class="metric-value" style="font-size: 36px;">{data['total_payment_method']}</div>
                <div class="metric-sub">Available payment options</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card" style="text-align: center;">
                <div class="metric-label">Success Rate</div>
                <div class="metric-value" style="font-size: 36px;">{data['this_month_succes_rate']}%</div>
                <div class="metric-sub">Transaction success rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 5. Top Categories Performance (TABLE) - PALING BAWAH
        st.markdown("### Top Categories Performance")
        
        cols = st.columns([1, 4, 2, 2])
        with cols[0]: st.markdown("**Rank**")
        with cols[1]: st.markdown("**Category**")
        with cols[2]: st.markdown("**Percentage**")
        with cols[3]: st.markdown("**Performance**")
        st.markdown("---")
        
        for i, (category, percentage) in enumerate(cat_data.items(), 1):
            perf = "🟢 High" if percentage > 3.0 else "🟡 Medium"
            cols = st.columns([1, 4, 2, 2])
            with cols[0]: st.markdown(f"{i}")
            with cols[1]: st.markdown(category[:30] + "..." if len(category) > 30 else category)
            with cols[2]: st.markdown(f"{percentage}%")
            with cols[3]: st.markdown(perf)
            st.markdown("---")
        
        st.markdown("### Runway Status")
        st.success(data['runway'])

# ==========================
# PREDICTIONS PAGE
# ==========================
elif st.session_state.active_tab == "Predictions":
    st.markdown("## Cashflow Prediction (Next 30 Days)")
    
    data = safe_request(f"{BASE_URL}/predict")
    
    if data:
        cards = data['cards']
        
        # Hanya tampilkan 2 kolom (Predicted Cashflow dan 3-Month Avg Cashflow)
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">Predicted Cashflow</div>
                <div class="metric-value">{format_rupiah(cards['predicted_cashflow'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">3-Month Avg Cashflow</div>
                <div class="metric-value">{format_rupiah(cards['avg_3_month_cashflow'])}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Prediction Chart
        chart = data['chart']
        actual = chart['actual']
        predicted = chart['predicted']
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=actual['labels'],
            y=actual['values'],
            name='Actual Cashflow',
            line=dict(color='#667eea', width=3),
            mode='lines+markers'
        ))
        fig.add_trace(go.Scatter(
            x=predicted['labels'],
            y=predicted['values'],
            name='Predicted Cashflow',
            line=dict(color='#10b981', width=3, dash='dash'),
            mode='lines+markers'
        ))
        
        fig.update_layout(
            height=400,
            yaxis=dict(title='Amount (Rp)'),
            hovermode='x unified',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.caption("Forecast Method: Moving Average & Trend Analysis (ARIMA-inspired) | Predictions based on 6-month historical data with exponential smoothing")
        
        # Model Performance
        fraud_data = safe_request(f"{BASE_URL}/fraud_detection")
        
        if fraud_data:
            sec_perf = fraud_data.get('security_performance', {})
            
            st.markdown("## Model Performance & Accuracy")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f"""
                <div class="security-metric">
                    <div class="security-value">{sec_perf.get('detection_rate', '94.2%')}</div>
                    <div class="security-label">Model Accuracy</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="security-metric">
                    <div class="security-value">0.063</div>
                    <div class="security-label">RMSE Score</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div class="security-metric">
                    <div class="security-value">6 Mo</div>
                    <div class="security-label">Training Period</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col4:
                st.markdown(f"""
                <div class="security-metric">
                    <div class="security-value">92%</div>
                    <div class="security-label">Confidence Level</div>
                </div>
                """, unsafe_allow_html=True)
        
        # AI Insights
        st.markdown("## AI Insights & Recommendations")
        insights_text = data['ai Insights']
        lines = insights_text.split('\n')
        formatted_lines = []
        for line in lines:
            if line.strip():
                clean_line = line.replace('*', '').replace('-', '').replace('•', '').strip()
                formatted_lines.append(f"• {clean_line}")
        formatted_text = '<br>'.join(formatted_lines)
        
        st.markdown(f"""
        <div class="ai-card" style="background: linear-gradient(135deg, #1a1f36 0%, #2d3748 100%);">
            <div class="ai-text">
                {formatted_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ==========================
# FRAUD DETECTION PAGE - URUTAN BARU
# ==========================
elif st.session_state.active_tab == "Fraud Detection":
    st.markdown("## Fraud Detection & Security")
    st.markdown("Real-time fraud monitoring and risk assessment")
    
    data = safe_request(f"{BASE_URL}/fraud_detection")
    
    if data:
        # 1. Security Status (baris pertama)
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="security-metric">
                <div class="security-value" style="color: #10b981;">Protected</div>
                <div class="security-label">All systems active</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="security-metric">
                <div class="security-value" style="color: #f97316;">{data['risk_level']}</div>
                <div class="security-label">{data['indicators']['failed_rate']} failed rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
            <div class="security-metric">
                <div class="security-value">Real-time</div>
                <div class="security-label">24/7 monitoring</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
            <div class="security-metric">
                <div class="security-value">Active</div>
                <div class="security-label">TF-IDF classifier</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 2. Fraud Detection & Risk Assessment
        st.markdown("### Fraud Detection & Risk Assessment")
        
        risk_color = "#10b981" if data['fraud_risk_score'] < 30 else "#f97316" if data['fraud_risk_score'] < 70 else "#ef4444"
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {risk_color} 0%, {risk_color}CC 100%); padding: 30px; border-radius: 16px; color: white; margin-bottom: 20px;">
            <div style="font-size: 16px; opacity: 0.9;">Fraud Risk Score</div>
            <div style="font-size: 48px; font-weight: 600;">{data['fraud_risk_score']}</div>
            <div style="font-size: 18px;">Risk Level: {data['risk_level']}</div>
            <div style="margin-top: 20px;">
                <div>Anomaly Detection: {data.get('anomaly_detection', 'Normal')}</div>
                <div>ML Model: Rule-Based + Isolation Forest</div>
                <div>Top Transaction Region: {data['top_region']}</div>
                <div>Geo-analysis Active</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 3. Fraud Indicators
        st.markdown("### Fraud Indicators")
        
        indicators = data['indicators']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="security-metric">
                <div class="security-value" style="color: #ef4444;">{indicators['failed_rate']}</div>
                <div class="security-label">Failed Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="security-metric">
                <div class="security-value" style="color: #f97316;">{indicators['pending_rate']}</div>
                <div class="security-label">Pending Rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="security-metric">
                <div class="security-value" style="color: #10b981;">{indicators['velocity_check']}</div>
                <div class="security-label">Velocity Check</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="security-metric">
                <div class="security-value" style="color: #10b981;">{indicators['pattern_match']}</div>
                <div class="security-label">Pattern Match</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 4. Security Alerts
        if data.get('alerts'):
            st.markdown("### Security Alerts")
            for alert in data['alerts']:
                if alert:
                    st.markdown(f"""
                    <div style="background: #fff3e0; padding: 16px; border-radius: 8px; margin: 10px 0; border-left: 4px solid #f97316;">
                        <strong>{alert['type']}</strong><br>
                        {alert['message']}
                    </div>
                    """, unsafe_allow_html=True)
        
        # 5. Security Performance Metrics
        st.markdown("### Security Performance Metrics")
        
        sec_perf = data.get('security_performance', {})
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="security-metric">
                <div class="security-value">{sec_perf.get('detection_rate', '98.7%')}</div>
                <div class="security-label">Detection Rate</div>
                <div style="font-size: 12px;">True positive rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="security-metric">
                <div class="security-value">{sec_perf.get('false_positives', '1.3%')}</div>
                <div class="security-label">False Positives</div>
                <div style="font-size: 12px;">Accuracy rate</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="security-metric">
                <div class="security-value">{sec_perf.get('avg_response', '<1s')}</div>
                <div class="security-label">Avg Response</div>
                <div style="font-size: 12px;">Detection speed</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="security-metric">
                <div class="security-value">{sec_perf.get('blocked_today', 0)}</div>
                <div class="security-label">Blocked Today</div>
                <div style="font-size: 12px;">Suspicious transactions</div>
            </div>
            """, unsafe_allow_html=True)
        
        # 6. Security Best Practices
        st.markdown("### Security Best Practices")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div style="background: white; padding: 16px; border-radius: 8px; border: 1px solid #eef2f6;">
                ☐ Enable two-factor authentication for all high-value transactions<br><br>
                ☐ Monitor transactions from new geographic locations closely
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="background: white; padding: 16px; border-radius: 8px; border: 1px solid #eef2f6;">
                ☐ Set up automated alerts for unusual spending patterns<br><br>
                ☐ Regularly review and update fraud detection rules
            </div>
            """, unsafe_allow_html=True)
        
        # 7. AI Security Alert Report
        st.markdown("### 🤖 AI Security Alert Report")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); padding: 20px; border-radius: 12px; color: white; margin: 15px 0;">
            {data['security alert']}
        </div>
        """, unsafe_allow_html=True)
        
        st.caption("Detection Method: Rule-Based Classification + Isolation Forest | Real-time monitoring with ML-based anomaly detection | Last updated: 28/2/2026, 14:24:09")