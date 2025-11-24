import pathway as pw
import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

# --- Configuration ---
# Load .env file (assuming it's in the project root, accessible via relative path or mounted volume)
# In WSL, we might need to be careful about paths. 
# We'll assume the script is run from the project root.
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("WARNING: GOOGLE_API_KEY not found. AI features will fail.")
else:
    genai.configure(api_key=API_KEY)

# --- UDF Definition ---
@pw.udf
def analyze_crash(volatility: float, headline: str) -> str:
    """
    Analyzes the crash using Gemini if volatility is high.
    """
    if volatility < 0.5:
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

def run_sentinel():
    # Data Paths
    # In WSL, we are running from the project root (mounted path).
    # We can use relative paths "data/..."
    
    # 1. Ingestion
    # input_rate=20 means 1 hour of data plays in ~3 minutes
    prices = pw.demo.replay_csv(
        path="data/stream_prices.csv",
        schema=pw.schema_from_csv("data/stream_prices.csv"),
        input_rate=20
    )
    
    news = pw.demo.replay_csv(
        path="data/stream_news.csv",
        schema=pw.schema_from_csv("data/stream_news.csv"),
        input_rate=20
    )

    # 2. Windowing & Volatility Calculation
    # 30-second tumbling window
    windowed_stats = (
        prices.windowby(
            pw.this.timestamp,
            window=pw.temporal.tumbling(duration=30),
            behavior=pw.temporal.common_behavior(
                cutoff=pw.temporal.cutoff.delayed_by(1)
            )
        ).reduce(
            window_end=pw.this._pw_window_end,
            volatility=pw.reductions.std(pw.this.price),
            current_price=pw.reductions.last(pw.this.price),
        )
    )

    # 3. Enrichment (ASOF Join / Interval Join)
    # We want to attach the latest news to the price window.
    # We use join_interval to look back 10 minutes for news.
    enriched = windowed_stats.join_interval(
        news,
        lower_bound=pw.temporal.Timestamp(minutes=10), 
        upper_bound=pw.temporal.Timestamp(0),
        left_time=windowed_stats.window_end,
        right_time=news.timestamp
    ).reduce(
        window_end=pw.this.window_end,
        volatility=pw.this.volatility,
        current_price=pw.this.current_price,
        # Get the headline with the max timestamp (latest news)
        headline=pw.reductions.max(pw.this.headline, key=pw.this.timestamp_right)
    )
    
    # 4. AI Analysis & Output
    final_stream = enriched.select(
        timestamp=pw.this.window_end,
        price=pw.this.current_price,
        volatility=pw.this.volatility,
        headline=pw.this.headline,
        ai_analysis=analyze_crash(pw.this.volatility, pw.this.headline)
    )

    # Output to JSONL
    pw.io.jsonl.write(
        final_stream,
        "data/sentinel_output.jsonl"
    )

    # Run the engine
    pw.run()

if __name__ == "__main__":
    run_sentinel()
