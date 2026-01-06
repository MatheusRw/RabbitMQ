# a logica de feedback do consumidor de RPC - Recebedor, que processa as requisições e envia as respostas de volta pra mesma fila.


import pika

def on_request(ch, method, properties, body):
    n = int(body)

    print(" [.] Calculating %s * %s" % (n, n))
    response = n * n

    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=properties.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)

# Conexão e configuração do servidor RPC
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='rpc_queue')
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()
