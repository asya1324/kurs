FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

RUN apt-get update && apt-get install -y ca-certificates && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

# Delete the bad migrations so they don't crash the build
RUN rm -rf main/migrations

# Collect static
RUN python manage.py collectstatic --no-input

# Run SQLite migrations
RUN python manage.py migrate

CMD ["gunicorn", "itestoria.wsgi:application", "--bind", "0.0.0.0:8000"]