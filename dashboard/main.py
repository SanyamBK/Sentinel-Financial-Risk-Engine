import streamlit as st
import time
from utils import get_data_paths, load_data
from components import render_css, render_metrics, render_chart, render_alert

# --- Configuration ---
st.set_page_config(
    page_title="Sentinel: AI Risk Engine",
    page_icon="🛡️",
    layout="wide"
)

def main():
    render_css()
    st.title("🛡️ Sentinel: Real-Time Risk & Sentiment Engine")

    # --- Layout ---
    # Create placeholders for dynamic content
    placeholder_metrics = st.empty()
    placeholder_chart = st.empty()
    placeholder_alert = st.empty()

    output_file = get_data_paths()

    # --- Main Loop ---
    while True:
        df = load_data(output_file)
        
        if not df.empty:
            # Get latest row
            latest = df.iloc[-1]
            
            # Extract values
            price = float(latest.get('price', 0))
            volatility = float(latest.get('volatility', 0))
            ai_analysis = latest.get('ai_analysis', "Market Stable")
            
            # Render Components
            render_metrics(placeholder_metrics, price, volatility)
            render_chart(placeholder_chart, df)
            render_alert(placeholder_alert, volatility, ai_analysis)
                
        else:
            placeholder_alert.warning("Waiting for data stream...")
            
        time.sleep(1)

if __name__ == "__main__":
    main()
