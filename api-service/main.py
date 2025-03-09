from fastapi import FastAPI
import pika
import yaml
import uvicorn
from pydantic import BaseModel

# Загружаем конфиг
with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

RABBITMQ_HOST = config["rabbitmq"]["host"]
RABBITMQ_PORT = config["rabbitmq"]["port"]
API_PORT = config["api"]["port"]

app = FastAPI()


@app.get("/sms")
async def get_sms():
    """Получает сообщение из RabbitMQ."""
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()
    channel.queue_declare(queue="sms_queue")
    
    method_frame, header_frame, body = channel.basic_get(queue="sms_queue", auto_ack=True)
    connection.close()

    if body:
        sms_data = body.decode("utf-8")
        return {"sms": sms_data}
    else:
        return {"message": "No SMS messages found"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=API_PORT)
