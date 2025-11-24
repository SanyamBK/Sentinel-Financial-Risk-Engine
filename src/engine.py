import pandas as pd
import numpy as np
import time
import json
import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime, timedelta

# --- Configuration ---
load_dotenv() # Load environment variables from .env

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("WARNING: GOOGLE_API_KEY not found in .env. AI features will fail.")
else:
    genai.configure(api_key=API_KEY)

# Get the directory where this script is located (src/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Data dir is sibling to src/ -> ../data
DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")

OUTPUT_FILE = os.path.join(DATA_DIR, "sentinel_output.jsonl")
PRICES_FILE = os.path.join(DATA_DIR, "stream_prices.csv")
NEWS_FILE = os.path.join(DATA_DIR, "stream_news.csv")

# Simulation Speed (Fast Forward)
# 1 hour of data in ~3 minutes -> 20x speed
# Real 1 sec = Sim 20 sec
SIMULATION_SPEED_MULTIPLIER = 20 
WINDOW_SIZE_SECONDS = 30
VOLATILITY_THRESHOLD = 0.5

def analyze_crash(volatility, headline):
    """
    Analyzes the crash using Gemini if volatility is high.
    """
    if volatility < VOLATILITY_THRESHOLD:
        return "Market Stable"
    
    if not headline:
        return "High Volatility detected, but no recent news found."

    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        prompt = f"Market Volatility is High (Score: {volatility:.2f}). Latest News is: '{headline}'. Explain the connection in 1 sentence."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI Analysis Failed: {str(e)}"

def run_engine():
    print("Starting Sentinel Engine (Pure Python)...")
    
    # 1. Load Data
    if not os.path.exists(PRICES_FILE) or not os.path.exists(NEWS_FILE):
        print("Error: Data files not found. Run gen_data.py first.")
        return

    df_prices = pd.read_csv(PRICES_FILE)
    df_prices['timestamp'] = pd.to_datetime(df_prices['timestamp'])
    
    df_news = pd.read_csv(NEWS_FILE)
    df_news['timestamp'] = pd.to_datetime(df_news['timestamp'])
    
    # Sort just in case
    df_prices = df_prices.sort_values('timestamp')
    df_news = df_news.sort_values('timestamp')
    
    # 2. Simulation Loop
    # We iterate through the price stream
    start_sim_time = df_prices['timestamp'].iloc[0]
    end_sim_time = df_prices['timestamp'].iloc[-1]
    
    current_sim_time = start_sim_time
    
    # Clear output file
    with open(OUTPUT_FILE, 'w') as f:
        pass
        
    print(f"Simulation Start: {start_sim_time}")
    
    # We'll process in 1-second steps (simulated time)
    # To be efficient, we can iterate through the dataframe rows
    # But we need a rolling window.
    
    # Let's use a buffer for the window
    price_window = [] # List of (timestamp, price)
    
    # News cursor
    news_idx = 0
    latest_headline = None
    
    # Real-time synchronization
    real_start_time = time.time()
    
    for index, row in df_prices.iterrows():
        sim_timestamp = row['timestamp']
        price = row['price']
        
        # Sync with real time
        # How much sim time has passed?
        sim_elapsed = (sim_timestamp - start_sim_time).total_seconds()
        # How much real time should have passed?
        target_real_elapsed = sim_elapsed / SIMULATION_SPEED_MULTIPLIER
        
        current_real_elapsed = time.time() - real_start_time
        
        if target_real_elapsed > current_real_elapsed:
            time.sleep(target_real_elapsed - current_real_elapsed)
            
        # Update Window
        price_window.append((sim_timestamp, price))
        
        # Remove old data (< 30s ago)
        cutoff_time = sim_timestamp - timedelta(seconds=WINDOW_SIZE_SECONDS)
        price_window = [x for x in price_window if x[0] > cutoff_time]
        
        # Calculate Volatility (StdDev of prices in window)
        if len(price_window) > 1:
            window_prices = [x[1] for x in price_window]
            volatility = np.std(window_prices)
        else:
            volatility = 0.0
            
        # Update News (ASOF Join logic)
        # Check if any news happened up to this sim_timestamp
        while news_idx < len(df_news) and df_news.iloc[news_idx]['timestamp'] <= sim_timestamp:
            latest_headline = df_news.iloc[news_idx]['headline']
            news_idx += 1
            
        # AI Trigger
        ai_analysis = "Market Stable"
        if volatility > VOLATILITY_THRESHOLD:
            # Rate limit or just call? 
            # For demo, we might want to avoid calling every second if it stays high.
            # But the requirement says "IF Volatility > Threshold... Trigger".
            # We'll call it. To save cost/time, maybe we cache or only call if it changed?
            # Let's just call it. It's a demo.
            # Optimization: Only call if we haven't analyzed this specific headline + crash state recently?
            # Let's keep it simple.
            ai_analysis = analyze_crash(volatility, latest_headline)
            
        # Output
        output_record = {
            'timestamp': sim_timestamp.isoformat(),
            'price': price,
            'volatility': volatility,
            'headline': latest_headline,
            'ai_analysis': ai_analysis
        }
        
        with open(OUTPUT_FILE, 'a') as f:
            f.write(json.dumps(output_record) + "\n")
            
        # Print status occasionally
        if index % 20 == 0:
            print(f"Sim Time: {sim_timestamp} | Price: {price:.2f} | Vol: {volatility:.4f}")

    print("Simulation Complete.")

if __name__ == "__main__":
    run_engine()
