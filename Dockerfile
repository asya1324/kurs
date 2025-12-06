# ===== Django + Python =====
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# додати сертифікат
COPY ca.pem /etc/ssl/certs/tidb-ca.pem
ENV SSL_CERT_FILE=/etc/ssl/certs/tidb-ca.pem

CMD ["gunicorn", "itestoria.wsgi:application", "--bind", "0.0.0.0:8000"]

