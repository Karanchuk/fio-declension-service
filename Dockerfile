FROM python:3.10-slim

WORKDIR /app

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY app ./app
COPY data/exceptions.json ./data/

EXPOSE 8000

# Запуск сервиса
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
