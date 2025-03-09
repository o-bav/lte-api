from flask import Flask, jsonify
import pika
import yaml

with open('config.yml', 'r') as f:
    config = yaml.safe_load(f)

RABBITMQ_HOST = config['rabbitmq']['host']
RABBITMQ_PORT = config['rabbitmq']['port']
API_PORT = config['api']['port']

app = Flask(__name__)


@app.route('/sms', methods=['GET'])
def get_sms():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT)
    )
    channel = connection.channel()
    channel.queue_declare(queue='sms_queue')
    method_frame, header_frame, body = channel.basic_get(
        queue='sms_queue', auto_ack=True
    )
    if body:
        sms_data = body.decode('utf-8')
        return jsonify({"sms": sms_data})
    else:
        return jsonify({"message": "No SMS messages found"})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=API_PORT)