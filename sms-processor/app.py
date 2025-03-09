import pika
import re
import json
import os


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
        pika.ConnectionParameters(
            host=os.environ.get('RABBITMQ_HOST', 'rabbitmq'),
            port=int(os.environ.get('RABBITMQ_PORT', 5672))
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='sms_queue')
    channel.basic_consume(queue='sms_queue', on_message_callback=process_sms)
    channel.start_consuming()


