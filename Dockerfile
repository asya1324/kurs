# Dockerfile: Final Version

# 1. Base Image
FROM python:3.12-slim

# 2. Set Working Directory
WORKDIR /app

# 3. Environment Variables (Unbuffered output, no pyc files)
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# --- System Dependencies and Certificates ---.
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    ca-certificates \
    bash \  
    # ⚠️ FIX: The continuation character is needed on the previous line.
    && rm -rf /var/lib/apt/lists/*

# Fix for Outbound SSL: Creates the directory needed for the symlink
# This resolves the FileNotFoundError in ssl.py on minimal images.
RUN mkdir -p /usr/local/ssl/

# Fix for Outbound SSL: Create the definitive symlink for Python to find the CA bundle.
RUN ln -sf /etc/ssl/certs/ca-certificates.crt /usr/local/ssl/ca-bundle.pem

# --- Python Dependencies ---
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# --- Application Code ---
COPY . /app/

# Ensure the entrypoint script is executable
RUN chmod +x /app/entrypoint.sh

# --- Static Files ---
# Collects all static files into STATIC_ROOT (/app/staticfiles/)
RUN python manage.py collectstatic --noinput

# --- Final Command ---
# Runs the entrypoint.sh script using a robust shell execution pattern (Bash is required)
CMD ["/bin/bash", "-c", "/app/entrypoint.sh"]