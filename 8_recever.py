#usando dead letter exchange para receber mensagens com routing key específica
# Utilizado para ver os erros e entender por que a mensagem não foi entregue
# serve para reprocessar as mensagens que falharam
# utilize o comando python recever.py A.info para reproduzir os resultados 

import pika
import sys

def callback(ch, method, properties, body):
    print(" [x] Mensagem Recebida %r:%r" % (method.routing_key, body))
    channel.basic_nack(delivery_tag=method.delivery_tag,requeue=False)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='dlx_logs', exchange_type='topic')
result = channel.queue_declare(queue='dlq_logs', exclusive=False)
channel.queue_bind(exchange='dlx_logs',queue='dlq_logs', routing_key='#')

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

result = channel.queue_declare('', exclusive=True,arguments={
    'x-dead-letter-exchange': 'dlx_logs'})

queue_name = result.method.queue


binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Uso: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Aguardando por logs. Para sair pressione CTRL+C')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=False)
channel.start_consuming()   