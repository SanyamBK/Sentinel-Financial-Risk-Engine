import pathway as pw
import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import timedelta

# --- Configuration ---
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    print("WARNING: GOOGLE_API_KEY not found. AI features will fail.")
else:
    genai.configure(api_key=API_KEY)

# --- UDF Definition ---
@pw.udf
def analyze_crash(volatility: float | None, headline: str | None) -> str:
    """
    Analyzes the crash using Gemini if volatility is high.
    """
    if volatility is None or volatility < 0.5:
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
    windowed_stats = prices.windowby(
        prices.timestamp,
        window=pw.temporal.tumbling(duration=timedelta(seconds=30)),
        behavior=pw.temporal.common_behavior()
    ).reduce(
        window_end=pw.this._pw_window_end,
        volatility=pw.reducers.stddev(pw.this.price),
        current_price=pw.reducers.latest(pw.this.price)
    )

    # 3. Enrichment (ASOF Join)
    # Attach the latest news to each price window
    enriched = windowed_stats.asof_join(
        news,
        windowed_stats.window_end,
        news.timestamp,
        how=pw.JoinMode.LEFT
    ).select(
        timestamp=windowed_stats.window_end,
        price=windowed_stats.current_price,
        volatility=windowed_stats.volatility,
        headline=news.headline
    )
    
    # 4. AI Analysis & Output
    final_stream = enriched.select(
        timestamp=pw.this.timestamp,
        price=pw.this.price,
        volatility=pw.this.volatility,
        headline=pw.this.headline,
        ai_analysis=analyze_crash(pw.this.volatility, pw.this.headline)
    )

    # Output to JSONL
    pw.io.jsonlines.write(
        final_stream,
        "data/sentinel_output.jsonl"
    )

    # Run the engine
    pw.run()

if __name__ == "__main__":
    run_sentinel()
