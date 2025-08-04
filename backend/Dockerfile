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
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Create media directory
RUN mkdir -p /app/media

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose correct port for Cloud Run
EXPOSE 8080

# Use Gunicorn on correct port
CMD ["gunicorn", "manager_backend.wsgi:application", "--bind", "0.0.0.0:8080"]
