# Dockerfile — Clean Production Version for Django + Render

# 1. Base Image
FROM python:3.12-slim

# 2. App directory and environment
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# 3. System packages
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    pkg-config \
    ca-certificates \
    bash \
    && rm -rf /var/lib/apt/lists/*

# 4. Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy application code
COPY . /app/

# 6. Make entrypoint executable
RUN chmod +x /app/entrypoint.sh

# NOTE:
# collectstatic MUST NOT be run inside Dockerfile on Render.
# Render runs it during build automatically.

# 7. Start the app
CMD ["bash", "/app/entrypoint.sh"]

