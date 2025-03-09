FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Установка Gammu и python3-gammu
RUN apt-get update && apt-get install -y gammu python3-gammu

COPY . .

CMD ["python", "app.py"]