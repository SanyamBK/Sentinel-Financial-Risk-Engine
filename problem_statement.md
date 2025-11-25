Pathway Hackathon Problem Statement

1. Pathway Overview
Pathway - a Python-based framework for real-time AI pipelines - is designed to ingest data streams from more than 300 sources, process them on the fly, and make the results queryable with large-language models (LLMs). It provides connectors for files, databases, message queues and enterprise services, automatically detects new records and updates, chunks and embeds documents, and maintains a live vector index.

Unlike most retrieval-augmented generation (RAG) stacks that rely on external vector databases, Pathway's Document Store keeps the vector index inside the pipeline. It combines semantic similarity search with BM25 full-text search to return relevant documents and is automatically synchronised with data sources. This live indexing avoids the need to re-ingest data in batches and allows generative models to answer queries using the latest information.

2. Key Ideas Behind Real-Time AI and RAG
• Real-Time vs Batch Processing
Traditional batch systems process data periodically; this introduces delays and stale information. Real-time streaming ingests, processes and outputs data within milliseconds, enabling decision-makers to react quickly and avoid outdated insights. Finance requires fast reaction to events; real-time streaming is therefore a competitive differentiator.

• Freshness of Indexes
LLMs do not have an inherent sense of time. To answer queries using up-to-date information, RAG systems must ensure their indexes stay synchronised with external data. Pathway's Document Store continuously parses, chunks, embeds and indexes documents as they arrive.

• Event-Driven Architecture
Modern AI agents require access to consistent, real-time data. Event-driven architectures (EDA) are the backbone of agentic AI. Without high-integrity streaming data, autonomous agents may act on stale or inconsistent information.

3. Use-Case Theme: Financial Services
1. Real-Time Market Analytics and Risk Management
Streaming ETL is essential for processing tick-by-tick market data, computing option Greeks and other risk metrics. Pathway ingests historical and live market data and continuously computes risk metrics (e.g., Delta, Gamma, Theta, Vega). The pipeline updates values in real time, making it suitable for traders who need live exposures.

4. Developer Resources and Technical Requirements
To ensure your project demonstrates strong real-time and production-readiness capabilities, all teams must adhere to the following requirements and leverage the official Pathway developer ecosystem.

Exploit pathway to the max

1. Live Data Ingestion with Pathway Connectors
Your system must utilize Pathway's real-time connectors to ingest streaming data relevant to your chosen use case. Pathway provides built-in connectors for files, databases, message queues, APIs, and web sources, all operating in streaming mode, ensuring results update in real time as data changes.

Artificial Data Streams with the demo Module (in case you find it difficult to access free streaming data APIs):
https://pathway.com/developers/user-guide/connect/artificial-streams

If live data is unavailable, teams may simulate streaming input by replaying static datasets with realistic time intervals.

2. Streaming Transformations and Feature Engineering
All data transformations must be performed in streaming mode using Pathway's transformation APIs. Your pipeline should support:
• Incremental joins, filters, and aggregations
• Stateful window computations
• Real-time feature engineering for signals and indicators

Documentation: https://pathway.com/developers/user-guide/data-transformation/table-operations
Temporal Data Windows: https://pathway.com/developers/user-guide/temporal-data/windows-manual

3. LLM Integration for Real-Time Insights
To make your system interactive and human-centric, integrate Pathway's LLM xPack enabling smooth orchestration of retrieval, summarization, and reasoning over live data.
You may use it for: Explainable insights (e.g., risk decision rationale, market summary reports)

Documentation: https://pathway.com/developers/user-guide/llm-xpack/overview

4. Mandatory Learning Resources and Templates
Templates
RAG App Templates (YAML): https://pathway.com/developers/templates/

Advanced Notebooks
Check out this cookbook for agent deployment:
https://github.com/pathwaycom/llm-app/blob/main/cookbooks/self-rag-agents/pathway_agentic_rag.ipynb

Reference Implementations
Option Greeks Computation with Databento (Mathematical Reference for Risk Engine):
https://pathway.com/developers/templates/etl/option-greeks/

Evaluation & Benchmarks
Evaluating RAG Applications with RAGAS: https://pathway.com/blog/evaluating-rag