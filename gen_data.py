import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def generate_data():
    print("Generating data...")
    
    # Configuration
    start_time = datetime(2025, 11, 25, 0, 0, 0)
    duration_seconds = 3600  # 1 hour
    ticker = "AAPL"
    base_price = 150.0
    
    # Time index
    timestamps = [start_time + timedelta(seconds=i) for i in range(duration_seconds)]
    
    # Generate Prices
    prices = []
    current_price = base_price
    
    for i, ts in enumerate(timestamps):
        # 0-45 mins: Stable
        if i < 45 * 60:
            change = np.random.normal(0, 0.1)
        # 45-47 mins: Crash (-15%)
        elif i < 47 * 60:
            change = np.random.normal(-0.5, 0.2) # Heavy downward pressure
        # 47-60 mins: Recovery/Volatile
        else:
            change = np.random.normal(0, 0.5)
            
        current_price += change
        prices.append(max(0.1, current_price)) # Ensure positive price
        
    df_prices = pd.DataFrame({
        "timestamp": timestamps,
        "ticker": ticker,
        "price": prices
    })
    
    # Generate News
    news_data = []
    
    # 1. Cause of crash (10s before crash)
    crash_time = start_time + timedelta(minutes=45) - timedelta(seconds=10)
    news_data.append({
        "timestamp": crash_time,
        "headline": "BREAKING: DOJ announces antitrust lawsuit against Apple"
    })
    
    # 2. Random filler news
    for _ in range(5):
        rand_time = start_time + timedelta(seconds=np.random.randint(0, duration_seconds))
        news_data.append({
            "timestamp": rand_time,
            "headline": "Market update: Tech sector sees mixed results"
        })
        
    df_news = pd.DataFrame(news_data).sort_values("timestamp")
    
    # Save to CSV
    os.makedirs("data", exist_ok=True)
    df_prices.to_csv("data/stream_prices.csv", index=False)
    df_news.to_csv("data/stream_news.csv", index=False)
    
    print(f"Generated {len(df_prices)} price records and {len(df_news)} news records.")
    print("Files saved to data/stream_prices.csv and data/stream_news.csv")

if __name__ == "__main__":
    generate_data()
