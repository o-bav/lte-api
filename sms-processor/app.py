import pika
import re
import json
import yaml

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

RABBITMQ_HOST = config['rabbitmq']['host']
RABBITMQ_PORT = config['rabbitmq']['port']


def process_sms(ch, method, properties, body):
    sms_data = body.decode('utf-8')
    sender = re.findall(r'\+CMGL: \d+,"REC UNREAD","(.*?)"', sms_data)[0]
    message = re.findall(r'\r\n(.*?)\r\n\r\nOK', sms_data, re.DOTALL)[0]
    print(f"Received SMS from {sender}: {message}")
    # Тут можно добавить логику обработки SMS
    data = {"sender": sender, "message": message}
    print(json.dumps(data))
    ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == '__main__':
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()
    channel.queue_declare(queue='sms_queue')
    channel.basic_consume(queue='sms_queue', on_message_callback=process_sms)
    channel.start_consuming()