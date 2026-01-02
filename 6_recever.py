#utiliza os cabeçalhos das mensagens para rotear as mensagens para as filas corretas

# para rodar vc usa o comando: Python 6_recever.py A error
# pode usar também Python 6_recever.py B info

import pika
import sys

def callback(ch, method, properties, body):
    #print(" [x] Mensagem Recebida %r:%r" % (method.routing_key, body))
    #print(" [x] Mensagem Recebida %r:%s" % (method.routing_key, body.decode()))
    #print(f" [x] Mensagem Recebida headers={properties.headers}, body={body.decode()}")
    print(" [x] Mensagem Recebida %r:%r" % (properties.headers, body))



connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='headers_logs', exchange_type='headers')
result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Uso: %s [component] [severity]...\n" % sys.argv[0])
    sys.exit(1)

headers = {}
headers["component"] = sys.argv[1]
headers["severity"] = sys.argv[2]

channel.queue_bind(exchange='headers_logs', queue=queue_name, arguments=headers)

print(' [*] Aguardando por logs. Para sair pressione CTRL+C')

channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
channel.start_consuming()   