import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

def generate_data():
    # --- Configuration ---
    START_TIME = datetime.now().replace(microsecond=0, second=0, minute=0) # Start at top of the hour
    DURATION_MINUTES = 60
    TICKER = 'AAPL'
    BASE_PRICE = 150.0
    
    # Ensure data directory exists
    # Get the directory where this script is located (src/)
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    # Data dir is sibling to src/ -> ../data
    DATA_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "data")
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # --- 1. Generate Prices ---
    print("Generating Prices...")
    timestamps = [START_TIME + timedelta(seconds=i) for i in range(DURATION_MINUTES * 60)]
    prices = []
    current_price = BASE_PRICE
    
    for t in timestamps:
        minutes_elapsed = (t - START_TIME).total_seconds() / 60.0
        
        # Logic:
        # 00:00 - 45:00: Stable (Random Walk)
        # 45:00 - 47:00: CRASH (Drop 15%)
        # 47:00 - 60:00: Recovery/High Volatility
        
        if minutes_elapsed < 45:
            change = np.random.normal(0, 0.05) # Low volatility
        elif 45 <= minutes_elapsed < 47:
            change = np.random.normal(-0.5, 0.2) # Heavy downward pressure
        else:
            change = np.random.normal(0.1, 0.3) # High volatility recovery
            
        current_price += change
        # Ensure price doesn't go negative (unlikely but good practice)
        current_price = max(0.01, current_price)
        prices.append(round(current_price, 2))
        
    df_prices = pd.DataFrame({
        'timestamp': timestamps,
        'ticker': TICKER,
        'price': prices
    })
    
    # Save to CSV
    df_prices.to_csv(os.path.join(DATA_DIR, 'stream_prices.csv'), index=False)
    print(f"Saved {os.path.join(DATA_DIR, 'stream_prices.csv')} with {len(df_prices)} rows.")

    # --- 2. Generate News ---
    print("Generating News...")
    # Sparse headlines
    news_data = []
    
    # Random background news
    for i in range(0, 60, 5): # Every 5 minutes roughly
        t = START_TIME + timedelta(minutes=i) + timedelta(seconds=random.randint(0, 60))
        news_data.append({
            'timestamp': t,
            'ticker': TICKER,
            'headline': f"Analyst note: {TICKER} showing steady performance."
        })

    # THE CAUSE
    # 44:50 (10 seconds before crash at 45:00)
    crash_cause_time = START_TIME + timedelta(minutes=44, seconds=50)
    news_data.append({
        'timestamp': crash_cause_time,
        'ticker': TICKER,
        'headline': "BREAKING: DOJ announces antitrust lawsuit against Apple. Stock expected to plummet."
    })
    
    df_news = pd.DataFrame(news_data)
    df_news = df_news.sort_values('timestamp')
    
    df_news.to_csv(os.path.join(DATA_DIR, 'stream_news.csv'), index=False)
    print(f"Saved {os.path.join(DATA_DIR, 'stream_news.csv')} with {len(df_news)} rows.")

if __name__ == "__main__":
    generate_data()
