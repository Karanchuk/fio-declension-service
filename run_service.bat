@echo off
where docker >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Docker не найден. Установите Docker Desktop.
    exit /b
)
docker-compose up --build -d
echo Сервис запущен! Откройте http://localhost:8000/docs
pause