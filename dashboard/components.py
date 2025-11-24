import streamlit as st

def render_css():
    """Renders custom CSS for the dashboard."""
    st.markdown("""
    <style>
        .metric-container {
            background-color: #1E1E1E;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #333;
        }
        .alert-box {
            background-color: #FF4B4B;
            color: white;
            padding: 20px;
            border-radius: 10px;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { opacity: 1; }
            50% { opacity: 0.8; }
            100% { opacity: 1; }
        }
    </style>
    """, unsafe_allow_html=True)

def render_metrics(placeholder, price, volatility):
    """Renders the key metrics (Price, Volatility)."""
    with placeholder.container():
        c1, c2 = st.columns(2)
        c1.metric("Current Price", f"${price:.2f}")
        c2.metric("Volatility (StdDev)", f"{volatility:.4f}", delta_color="inverse")

def render_chart(placeholder, df):
    """Renders the price chart."""
    chart_data = df.tail(100)
    if 'price' in chart_data.columns:
        placeholder.line_chart(chart_data['price'])

def render_alert(placeholder, volatility, ai_analysis):
    """Renders the AI alert box if volatility is high."""
    if volatility > 0.5:
        placeholder.markdown(f"""
        <div class="alert-box">
            <h3>🚨 MARKET CRASH DETECTED</h3>
            <p><strong>AI Analysis:</strong> {ai_analysis}</p>
        </div>
        """, unsafe_allow_html=True)
    else:
        placeholder.info("System Status: Monitoring... Market Stable.")
