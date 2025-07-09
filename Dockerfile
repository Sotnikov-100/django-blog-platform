FROM python:3.12-alpine

LABEL maintainer="Django Blog Platform"

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk update && \
    apk add --no-cache \
    postgresql-dev \
    gcc \
    python3-dev \
    musl-dev \
    zlib-dev \
    jpeg-dev \
    && rm -rf /var/cache/apk/*

WORKDIR /app

# Create logs directory
RUN mkdir -p /app/logs

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create media directory
RUN mkdir -p /app/media

# Set permissions
RUN chmod +x /app/manage.py

# Expose port
EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]
