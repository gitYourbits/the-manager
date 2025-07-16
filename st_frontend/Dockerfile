FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        g++ \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir \
    streamlit==1.28.1 \
    requests==2.31.0 \
    python-dotenv==1.0.0

# Copy project
COPY . .

# Expose port
EXPOSE 8501

# Default command
CMD ["streamlit", "run", "main.py", "--server.port", "8501", "--server.address", "0.0.0.0"] 