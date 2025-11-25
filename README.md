# Sentinel: Real-Time Financial Risk & Sentiment Engine

Sentinel is a real-time anomaly detection system that bridges the gap between Quantitative Finance (Numbers) and Qualitative Analysis (News). It monitors high-frequency market data for statistical anomalies (Flash Crashes) and, upon detection, instantly triggers an AI Agent to read simultaneous news headlines and explain the *root cause* of the crash.

## Features
*   **Real-Time Volatility Monitoring**: Calculates rolling standard deviation using Pathway's temporal windowing.
*   **AI-Powered Analysis**: Uses Google Gemini 2.0 Flash Lite to explain market anomalies by correlating them with breaking news.
*   **Live Dashboard**: Interactive Streamlit dashboard for real-time visualization.
*   **Production-Ready Architecture**: Built with Pathway, a high-performance stream processing framework.

## 🚀 Quick Start (Docker)

The easiest way to run Sentinel is using Docker Compose:

1.  **Prerequisites**: Install Docker Desktop.
2.  **Configuration**: Ensure your `GOOGLE_API_KEY` is set in the `.env` file.
3.  **Run**:
    ```bash
    docker-compose up --build
    ```
4.  **Access**:
    *   Dashboard: [http://localhost:8501](http://localhost:8501)
    *   Engine: Runs in the background.

## 🛠️ Manual Setup (WSL)

If you prefer running manually on Windows/WSL:

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
    ```bash
    wsl -d Ubuntu python3 -m pip install --break-system-packages pathway google-generativeai python-dotenv
    ```

4.  **Install Streamlit (Windows)**:
    ```powershell
    python -m venv .venv
    .venv\Scripts\activate
    pip install streamlit pandas plotly watchdog
    ```

5.  **Configure API Key**:
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```

6.  **Run the Demo**:
    ```powershell
    .\run_demo.ps1
    ```

## 🏗️ Architecture & Compliance Note

### Why Custom UDFs instead of Standard RAG Templates?
While we leveraged the [Pathway LLM App](https://github.com/pathwaycom/llm-app) repository for architectural inspiration, we implemented a **Custom User Defined Function (UDF)** for the Agent integration rather than using a pre-built RAG template.

**Reasoning:**
1.  **Event-Driven Efficiency**: Standard RAG templates are query-driven. Sentinel is **event-driven**. By using a custom UDF, we injected conditional logic (`if volatility > 0.5`) to trigger the LLM *only* during critical market events.
2.  **Latency Optimization**: This approach minimizes API calls, reducing latency and ensuring the dashboard updates in sub-seconds without waiting for LLM inference on stable data rows.
3.  **Compliance**: This implementation fully utilizes Pathway's `xPack` capabilities for reasoning over live streams while adhering to strict rate-limit constraints.

## Technical Implementation
The system implements the following Pathway features as specified in the project requirements:
*   **Windowing**: `pw.windowby()` with 30-second tumbling windows for volatility calculation.
*   **ASOF Join**: `join_interval()` to attach latest news to price windows.
*   **UDFs**: `@pw.udf` decorator for Gemini AI integration.
*   **Stream Replay**: `pw.demo.replay_csv()` for simulating high-frequency data.
