#!/bin/bash
# проверяем наличие docker
if ! command -v docker &> /dev/null
then
    echo "Docker не установлен. Пожалуйста, установите Docker Desktop."
    exit
fi

# проверяем наличие docker-compose
if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose не установлен. Пожалуйста, установите Docker Compose."
    exit
fi

# поднимаем сервис
docker-compose up --build -d

echo "Сервис запущен! Перейдите в браузере на http://localhost:8000/docs"
