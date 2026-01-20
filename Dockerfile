FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . . 

ENV PYTHONUNBUFFERED=1

CMD ["sh", "-c", "python manage.py run_grpc & gunicorn core.wsgi:application --bind 0.0.0.0:8000"]
EXPOSE 8000 50051

