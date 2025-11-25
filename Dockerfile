# Base Image
FROM python:3.11-slim

# Install system dependencies required for Pathway
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Default command: Generate data then run engine
CMD sh -c "python src/gen_data.py && python src/pathway_app.py"
