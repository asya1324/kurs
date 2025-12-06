# ===== Django + Python =====
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# RUN apt-get update && apt-get install -y \
#     build-essential \
#     libpq-dev \
#     default-libmysqlclient-dev \
#     pkg-config \
#     ca-certificates \
#     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --noinput

# додати сертифікат
COPY isrgrootx1.pem /etc/ssl/certs/isrgrootx1.pem
ENV SSL_CERT_FILE=/etc/ssl/certs/isrgrootx1.pem

CMD ["gunicorn", "itestoria.wsgi:application", "--bind", "0.0.0.0:8000"]