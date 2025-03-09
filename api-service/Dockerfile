FROM python:3.8-slim-buster

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gammu \
    libgammu-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Обновляем pip и устанавливаем зависимости, включая gunicorn
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Запускаем приложение через gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]