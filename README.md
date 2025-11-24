# Sentinel: Real-Time Financial Risk & Sentiment Engine

Sentinel is a real-time anomaly detection system that bridges the gap between Quantitative Finance (Numbers) and Qualitative Analysis (News). It monitors high-frequency market data for statistical anomalies (Flash Crashes) and, upon detection, instantly triggers an AI Agent to read simultaneous news headlines and explain the *root cause* of the crash.

## Features
*   **Real-Time Volatility Monitoring**: Calculates rolling standard deviation on live market data.
*   **AI-Powered Analysis**: Uses Google Gemini 2.5 Flash to explain market anomalies by correlating them with breaking news.
*   **Live Dashboard**: Interactive Streamlit dashboard for real-time visualization.
*   **Pure Python Architecture**: Lightweight, dependency-free simulation engine.

## Installation

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/SanyamBK/Sentinel-Financial-Risk-Engine.git
    cd Sentinel-Financial-Risk-Engine
    ```

2.  **Set up Virtual Environment**:
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Linux/Mac
    source .venv/bin/activate
    ```

3.  **Install Dependencies**:
    ```bash
    pip install pandas streamlit google-generativeai python-dotenv
    ```

4.  **Configure API Key**:
    Create a `.env` file in the root directory:
    ```env
    GOOGLE_API_KEY=your_gemini_api_key_here
    ```

## Usage

1.  **Generate Synthetic Data**:
    ```bash
    python src/gen_data.py
    ```

2.  **Run the Demo**:
    **Windows (PowerShell)**:
    ```powershell
    .\run_demo.ps1
    ```
    
    **Manual Run**:
    Terminal 1 (Engine):
    ```bash
    python src/engine.py
    ```
    Terminal 2 (Dashboard):
    ```bash
    streamlit run dashboard/main.py
    ```

## Architecture
*   `src/gen_data.py`: Generates synthetic price and news streams.
*   `src/engine.py`: Core processing engine (Simulation -> Windowing -> AI Trigger).
*   `dashboard/`: Streamlit application components.
*   `data/`: Stores generated streams and output logs.
