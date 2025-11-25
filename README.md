# Sentinel: Real-Time Financial Risk & Sentiment Engine

Sentinel is a real-time anomaly detection system that bridges the gap between Quantitative Finance (Numbers) and Qualitative Analysis (News). It monitors high-frequency market data for statistical anomalies (Flash Crashes) and, upon detection, instantly triggers an AI Agent to read simultaneous news headlines and explain the *root cause* of the crash.

## Features
*   **Real-Time Volatility Monitoring**: Calculates rolling standard deviation using Pathway's temporal windowing.
*   **AI-Powered Analysis**: Uses Google Gemini 2.5 Flash to explain market anomalies by correlating them with breaking news.
*   **Live Dashboard**: Interactive Streamlit dashboard for real-time visualization.
*   **Production-Ready Architecture**: Built with Pathway, a high-performance stream processing framework.

## Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/SanyamBK/Sentinel-Financial-Risk-Engine.git
    cd Sentinel-Financial-Risk-Engine
    ```

2.  **Install WSL (Windows Only)**:
    ```powershell
    wsl --install -d Ubuntu
    ```

3.  **Install Dependencies in WSL**:
*   `src/gen_data.py`: Generates synthetic price and news streams.
*   `src/pathway_app.py`: **Pathway engine** - Uses `pw.windowby`, `pw.join_interval`, `pw.udf`.
*   `dashboard/`: Streamlit application components.
*   `data/`: Stores generated streams and output logs.

## Technical Implementation
The system implements the following Pathway features as specified in the project requirements:
*   **Windowing**: `pw.windowby()` with 30-second tumbling windows for volatility calculation.
*   **ASOF Join**: `join_interval()` to attach latest news to price windows.
*   **UDFs**: `@pw.udf` decorator for Gemini AI integration.
*   **Stream Replay**: `pw.demo.replay_csv()` for simulating high-frequency data.
