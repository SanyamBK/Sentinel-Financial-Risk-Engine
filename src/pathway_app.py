import pathway as pw
import os
import math
from datetime import datetime
import google.generativeai as genai
from dotenv import load_dotenv

# Configuration
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# UDF to calculate standard deviation (volatility)
@pw.udf
def calculate_std(prices: list[float]) -> float:
    """Calculate standard deviation from a list/tuple of prices"""
    if not prices or len(prices) < 2:
        return 0.0
    n = len(prices)
    mean = sum(prices) / n
    variance = sum((x - mean) ** 2 for x in prices) / n
    return math.sqrt(variance)

# UDF for AI analysis
@pw.udf
def analyze_crash(volatility: float | None, headline: str | None) -> str:
    if volatility is None or volatility < 0.5:
        return "Market Stable"
    if not headline:
        return "High Volatility detected, but no recent news found."
    try:
        model = genai.GenerativeModel('gemini-2.0-flash-lite')
        prompt = f"Market Volatility is High (Score: {volatility:.2f}). Latest News is: '{headline}'. Explain the connection in 1 sentence."
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"AI Analysis Failed: {str(e)}"

# UDF to parse timestamp string to float
@pw.udf
def parse_timestamp(ts_str: str) -> float:
    try:
        # Handle potential different formats if needed, but assuming YYYY-MM-DD HH:MM:SS
        dt = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        return dt.timestamp()
    except:
        return 0.0

def run_sentinel():
    print("🚀 Sentinel Financial Risk Engine Starting...")
    
    # 1. Ingestion using Pathway's replay_csv
    # input_rate=10 throttles the pipeline to prevent hitting Gemini's 30 RPM rate limit.
    prices_raw = pw.demo.replay_csv(
        path="data/stream_prices.csv",
        schema=pw.schema_from_csv("data/stream_prices.csv"),
        input_rate=10
    )
    
    news_raw = pw.demo.replay_csv(
        path="data/stream_news.csv",
        schema=pw.schema_from_csv("data/stream_news.csv"),
        input_rate=10
    )

    # 2. Parse Timestamps - EXPLICIT SELECTION ONLY
    prices = prices_raw.select(
        timestamp=parse_timestamp(pw.this.timestamp),
        ticker=pw.this.ticker,
        price=pw.this.price
    )
    
    news = news_raw.select(
        timestamp=parse_timestamp(pw.this.timestamp),
        headline=pw.this.headline
    )
    
    # 3. Add window ID (30-second buckets) and dummy key for joining
    prices_windowed = prices.select(
        timestamp=pw.this.timestamp,
        price=pw.this.price,
        window_id=pw.apply(lambda ts: int(ts // 30), pw.this.timestamp),
        join_key=1
    )
    
    news_keyed = news.select(
        timestamp=pw.this.timestamp,
        headline=pw.this.headline,
        join_key=1
    )
    
    # 4. Group by window and calculate volatility
    windowed_stats = prices_windowed.groupby(pw.this.window_id).reduce(
        window_id=pw.this.window_id,
        join_key=pw.reducers.max(pw.this.join_key),
        price_list=pw.reducers.tuple(pw.this.price),
        last_price=pw.reducers.argmax(pw.this.timestamp, pw.this.price),
        window_end=pw.reducers.max(pw.this.timestamp)
    )
    
    # Calculate volatility
    windowed_stats = windowed_stats.select(
        window_id=pw.this.window_id,
        join_key=pw.this.join_key,
        last_price=pw.this.last_price,
        window_end=pw.this.window_end,
        volatility=calculate_std(pw.this.price_list)
    )
    
    # 5. Manual ASOF Join Workaround
    # Join on dummy key, filter for past news, and pick the latest
    joined = windowed_stats.join(
        news_keyed,
        windowed_stats.join_key == news_keyed.join_key
    ).filter(
        news_keyed.timestamp <= windowed_stats.window_end
    )
    
    enriched = joined.groupby(windowed_stats.window_id).reduce(
        window_end=pw.reducers.max(windowed_stats.window_end),
        last_price=pw.reducers.max(windowed_stats.last_price),
        volatility=pw.reducers.max(windowed_stats.volatility),
        headline=pw.reducers.argmax(news_keyed.timestamp, news_keyed.headline)
    )
    
    # 6. AI Analysis & Output
    final_stream = enriched.select(
        timestamp=pw.this.window_end,
        price=pw.this.last_price,
        volatility=pw.this.volatility,
        headline=pw.this.headline,
        ai_analysis=analyze_crash(pw.this.volatility, pw.this.headline)
    )
    
    # Write to output - use current directory to avoid path issues
    pw.io.jsonlines.write(final_stream, "sentinel_output.jsonl")
    
    print("✅ Pipeline configured successfully")
    print("🔄 Running real-time processing...")
    pw.run()
    print("✅ Processing complete!")

if __name__ == "__main__":
    run_sentinel()
