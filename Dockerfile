# ===== Django + Python =====
FROM python:3.12-slim

# створюємо робочу директорію
WORKDIR /app

# копіюємо requirements
COPY requirements.txt /app/

# ставимо залежності
RUN pip install --no-cache-dir -r requirements.txt

# копіюємо увесь проєкт
COPY . /app/

# збираємо статику
RUN python manage.py collectstatic --noinput

# запускаємо gunicorn
CMD ["gunicorn", "itestoria.wsgi:application", "--bind", "0.0.0.0:8000"]

