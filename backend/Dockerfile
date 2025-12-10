FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (for psycopg2, etc.)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . /app

# Expose FastAPI port
EXPOSE 8000

# Run with uvicorn (no reload, production-style)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
