# PROJECT DOCUMENTATION: SENTINEL
# TYPE: Real-Time Financial Risk & Sentiment Engine
# BUILDER TARGET: Google Antigravity / Project IDX / AI Agent
# THEME: Financial Services
# CONSTRAINTS: Zero Cost (Free Tier Only), Python-Native

# ==================================================================================
# 1. PRODUCT REQUIREMENTS DOCUMENT (PRD)
# ==================================================================================

## 1.1 Executive Summary
"Sentinel" is a real-time anomaly detection system that bridges the gap between Quantitative Finance (Numbers) and Qualitative Analysis (News). It monitors high-frequency market data for statistical anomalies (Flash Crashes) and, upon detection, instantly triggers an AI Agent to read simultaneous news headlines and explain the *root cause* of the crash.

## 1.2 Problem Statement
* **The Gap:** Traditional risk engines calculate volatility but cannot explain "Why" a price is moving. Traders lose critical seconds manually cross-referencing charts with news feeds (Bloomberg/Reuters).
* **The Solution:** An event-driven pipeline that automates this correlation, providing a "Reason" alongside the "Risk Score" in sub-seconds.

## 1.3 Technical Architecture & Workflow
1.  **Ingestion Layer:** Simulate two high-speed data streams (Stock Ticks & News Headlines) using static CSV replay.
2.  **Processing Engine (Pathway):**
    * **Windowing:** Calculate `Standard Deviation` (Volatility) on a 30-second rolling window.
    * **Logic:** IF `Volatility > Threshold` (e.g., 0.5), FLAG the event.
    * **Enrichment:** Use an `ASOF JOIN` (Temporal Join) to attach the *most recent* news headline to the crash event.
3.  **Intelligence Layer (AI Agent):**
    * **Trigger:** The LLM is *only* called for flagged events (Cost Optimization).
    * **Model:** Google Gemini 2.5 Flash (Free Tier).
    * **Prompt:** "Market Volatility is High. Latest News is {headline}. Explain the connection."
4.  **Presentation Layer:** A Streamlit dashboard that updates every second with live metrics and a "Red Alert" box for AI insights.

## 1.4 Explicit Constraints
* **NO PAID APIs:** Do not generate code requiring API keys for Bloomberg, Polygon, or AlphaVantage. Use Pathway's `demo.replay_csv` for all data.
* **FREE AI ONLY:** Use `google-generativeai` library with the `gemini-2.5-flash` model.
* **EFFICIENCY:** The logic must include a conditional check (`if volatility < threshold: return "Stable"`) *before* calling the LLM to prevent rate-limit errors.

# ==================================================================================
# 2. STEP-BY-STEP IMPLEMENTATION PLAN
# ==================================================================================

## PHASE 1: Scenario Generation (The "Truth")
**Goal:** Create a deterministic dataset that guarantees a successful live demo.
* **Action:** Create a script `gen_data.py` that generates two CSV files: `stream_prices.csv` and `stream_news.csv`.
* **Price Logic:** Generate 1 hour of data (1 tick/sec) for Ticker 'AAPL'.
    * 00:00 - 45:00: Stable price (low noise).
    * 45:00 - 47:00: **CRASH EVENT** (Price drops 15% rapidly).
    * 47:00 - 60:00: High volatility recovery.
* **News Logic:** Generate sparse headlines.
    * **Crucial:** Insert a specific "Cause" headline (e.g., "BREAKING: DOJ announces antitrust lawsuit against Apple") at timestamp 44:50 (10 seconds before the crash starts).

## PHASE 2: The Pathway Backend (The "Engine")
**Goal:** Build `main.py` to ingest, process, and analyze the streams.
1.  **Ingestion:** Use `pw.demo.replay_csv` to read both CSV files. Set `input_rate=20` to "fast forward" the 1-hour scenario into a 3-minute demo.
2.  **Transformation (Math):** Use `windowby` with a `tumbling` window of 30 seconds. Inside the reducer, calculate `pw.reductions.std` (Volatility) and `pw.reductions.last` (Current Price).
3.  **Transformation (Context):** Use `pw.join` (specifically an interval join or ASOF join pattern) to link the Price Window with the News Stream. The condition must be: `News_Timestamp <= Window_End_Timestamp`.
4.  **Agent Integration:** Write a User Defined Function (UDF) `@pw.udf`.
    * Input: `volatility`, `headline`.
    * Logic: If `volatility > 0.5`, call `gemini-2.5-flash` to analyze the headline. Else, return "Market Stable".
5.  **Output:** Write the final result stream to `sentinel_output.jsonl`.

## PHASE 3: The Dashboard (The "Face")
**Goal:** Visualize the results.
* **Tool:** Streamlit (`app.py`).
* **Logic:** Continuously poll `sentinel_output.jsonl` for new lines.
* **Visuals:**
    * Metric 1: Price (Green/Red based on change).
    * Metric 2: Volatility Score (Turn RED if > 0.5).
    * **Main Feature:** An "AI Analyst" text box that only appears/updates when the AI detects a crash explanation.

# ==================================================================================
# 3. CRITICAL REFERENCE MATERIAL (FOR THE AI BUILDER)
# ==================================================================================

To build this correctly, you must reference the following repositories and documentation.

### A. GitHub Repository: `pathwaycom/pathway`
* **Relevance:** **PRIMARY (The Body)**. This repo contains the core engine, math operators, and simulation tools.
* **What to use from here:**
    * **Simulation:** Look for usage of `pw.demo.replay_csv`. This is REQUIRED to fake the stream.
    * **Math:** Look for `examples/showcases/` (specifically "Bollinger Bands" or "VWAP") to understand how to calculate `std` and `avg` on sliding windows.
    * **Link:** https://github.com/pathwaycom/pathway

### B. GitHub Repository: `pathwaycom/llm-app`
* **Relevance:** **SECONDARY (The Brain)**. This repo contains the patterns for connecting the engine to an LLM.
* **What to use from here:**
    * **Alerting Pattern:** Look at `examples/pipelines/alerting`. It demonstrates the "Conditional Trigger" architecture (only call LLM if X happens), which is required for our Efficiency Constraint.
    * **RAG Logic:** Use the patterns here for structuring the UDF (User Defined Function) prompt.
    * **Link:** https://github.com/pathwaycom/llm-app

### C. Essential Documentation Links
* **Simulating Data:** https://pathway.com/developers/user-guide/connect/artificial-streams
* **Windowing (Math):** https://pathway.com/developers/user-guide/temporal-data/windows-manual/
* **ASOF Join (Joining News to Prices):** https://pathway.com/developers/user-guide/temporal-data/asof-join/
* **UDFs (Connecting Gemini):** https://pathway.com/developers/user-guide/data-transformation/user-defined-function