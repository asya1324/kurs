# ===== Django + Python =====
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    default-libmysqlclient-dev \
    pkg-config \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Inside your Dockerfile, after the apt-get install block:

# ⚠️ FIX 1: Update system certificates hash links (forces recognition of the installed CA file)
RUN update-ca-certificates

# ⚠️ FIX 2: Create a symbolic link to satisfy Python's common hardcoded fallback path
# We link the actual CA bundle to a path Python often checks internally.
RUN ln -sf /etc/ssl/certs/ca-certificates.crt /usr/local/share/ca-certificates/ca-bundle.pem

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Inside the Dockerfile, after COPY . /app/
RUN chmod +x /app/entrypoint.sh

RUN python manage.py collectstatic --noinput

# додати сертифікат
COPY isrgrootx1.pem /etc/ssl/certs/isrgrootx1.pem
ENV SSL_CERT_FILE=/etc/ssl/certs/isrgrootx1.pem

# Replace the final Gunicorn CMD with this:
CMD ["/bin/bash", "-c", "/app/entrypoint.sh"]