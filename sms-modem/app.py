import serial
import time
import os
import pika


def send_message(message):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.environ.get('RABBITMQ_HOST', 'rabbitmq'),
            port=int(os.environ.get('RABBITMQ_PORT', 5672))
        )
    )
    channel = connection.channel()
    channel.queue_declare(queue='sms_queue')
    channel.basic_publish(exchange='', routing_key='sms_queue', body=message)
    connection.close()


def read_sms():
    ser = serial.Serial(
        os.environ.get('SERIAL_PORT', '/dev/ttyUSB0'), 115200, timeout=5
    )
    ser.write(b'AT+CMGF=1\r')
    time.sleep(1)
    ser.write(b'AT+CMGL="REC UNREAD"\r')
    time.sleep(1)
    response = ser.read(2048).decode('utf-8')
    ser.write(b'AT+CMGD=1,4\r')  # Delete read messages
    ser.close()
    return response


if __name__ == '__main__':
    while True:
        sms_data = read_sms()
        if "+CMGL:" in sms_data:
            send_message(sms_data)
        time.sleep(10)
       
