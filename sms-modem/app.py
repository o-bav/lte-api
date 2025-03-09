import gammu
import time
import yaml
import pika
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

try:
    with open('config.yml', 'r') as f:
        config = yaml.safe_load(f)

    SERIAL_PORT = config['modem']['serial_port']
    RABBITMQ_HOST = config['rabbitmq']['host']
    RABBITMQ_PORT = config['rabbitmq']['port']

    logging.info("Configuration loaded successfully.")

except FileNotFoundError:
    logging.error("Configuration file 'config.yml' not found.")
    exit(1)
except yaml.YAMLError as e:
    logging.error(f"Error parsing configuration file: {e}")
    exit(1)
except KeyError as e:
    logging.error(f"Missing configuration key: {e}")
    exit(1)

def send_message(message):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
        )
        channel = connection.channel()
        channel.queue_declare(queue='sms_queue')
        channel.basic_publish(exchange='', routing_key='sms_queue', body=message)
        connection.close()
        logging.info("SMS message sent to RabbitMQ.")
    except pika.exceptions.AMQPConnectionError as e:
        logging.error(f"Failed to connect to RabbitMQ: {e}")

def read_sms():
    try:
        sm = gammu.StateMachine()
        sm.ReadConfig()
        sm.Init()
        sms = sm.GetNextSMS()
        if sms:
            return sms[0]['Text']
        return None
    except gammu.GSMError as e:
        logging.error(f"Gammu error: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        return None

if __name__ == '__main__':
    while True:
        sms_text = read_sms()
        if sms_text:
            logging.info(f'Received SMS: {sms_text}')
            send_message(sms_text)
        time.sleep(10)