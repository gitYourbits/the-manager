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

# Collect static files (safe to run even if not using Whitenoise)
RUN python manage.py collectstatic --noinput || true

# Expose port (Render default is 10000)
EXPOSE 10000

# Start with Gunicorn for production
CMD ["gunicorn", "backend.wsgi:application", "--bind", "0.0.0.0:10000"]