# a logica de feedback do consumidor de RPC - Recebedor, que processa as requisições e envia as respostas de volta pra mesma fila.


import pika
import uuid

corr_id = ''

def on_response(ch, method, properties, body):
    if corr_id == properties.correlation_id:
        print("[.] Got %r" % body)

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

result = channel.queue_declare('', exclusive=True)
callback_queue = result.method.queue


channel.basic_consume(queue=callback_queue,
                      on_message_callback=on_response,
                        auto_ack=True)

print(" [x] Requesting data 30 * 30 ")

corr_id = str(uuid.uuid4())
channel.basic_publish(exchange='',
                      routing_key='rpc_queue',
                      properties=pika.BasicProperties(
                          reply_to=callback_queue,
                          correlation_id=corr_id,
                      ),
                      body=str(30))

channel.start_consuming()