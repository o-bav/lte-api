from flask import Flask, jsonify
import pika
import os

app = Flask(__name__)


@app.route('/sms', methods=['GET'])
def get_sms():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.environ.get('RABBITMQ_HOST', 'rabbitmq'),
            port=int(os.environ.get('RABBITMQ_PORT', 5672))
        )
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
    app.run(
        debug=True,
        host='0.0.0.0',
        port=int(os.environ.get('API_PORT', 5000))
    )