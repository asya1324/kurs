FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=10000

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# CRITICAL FIX: Remove conflicting SQL migration files
RUN rm -rf main/migrations

# Collect static files
RUN python manage.py collectstatic --no-input

# Run standard migrations for Sessions (SQLite)
RUN python manage.py migrate

CMD ["gunicorn", "itestoria.wsgi:application", "--bind", "0.0.0.0:10000"]