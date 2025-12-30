# O exchange do tipo direct envia mensagens para filas com base na chave de roteamento
# a chave pode ser por exemplo logs de erro, info, debug 
#  O exchange que distriui as mensagens para todas as filas ligadas a ele é o fanout

import pika
import sys

def callback(ch, method, properties, body):
    print(" [x] Mensagem Recebida %r:%r" % (method.routing_key, body))

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue


severities = sys.argv[1:]
if not severities:
    sys.stderr.write("Uso: %s [info] [warning] [error]\n" % sys.argv[0])
    sys.exit(1)

for severity in severities:
    channel.queue_bind(exchange='direct_logs', queue=queue_name, routing_key=severity)

print(' [*] Aguardando por logs. Para sair pressione CTRL+C')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()   