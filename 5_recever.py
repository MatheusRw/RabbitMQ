# O exchange do tipo direct envia mensagens para filas com base na chave de roteamento
# a chave pode ser por exemplo logs de erro, info, debug 
# O exchange que distriui as mensagens para todas as filas ligadas a ele é o fanout
#na hora de rodar o scruipt cada consumidor deve passar como argumento a severidade que quer receber


# Comando para rodar Python 5_sender.py A.*
# pode rodar o comando com # também para chaves compostas de varios elementos é como um *
# ou também com *.* 
 

import pika
import sys

def callback(ch, method, properties, body):
    print(" [x] Mensagem Recebida %r:%r" % (method.routing_key, body))

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Uso: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(exchange='topic_logs', queue=queue_name, routing_key=binding_key)

print(' [*] Aguardando por logs. Para sair pressione CTRL+C')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()   