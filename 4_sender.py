# O exchange do tipo direct envia mensagens para filas com base na chave de roteamento
# a chave pode ser por exemplo logs de erro, info, debug 


import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

messages = ["primeiro log,", "segundo log,", "terceiro log.","quarto log.","quinto log."]
severities = ['info', 'error', 'warning', 'error', 'info']

for i in range(5):
    channel.basic_publish(exchange='direct_logs', routing_key=severities[i], body=messages[i])
    print(f" [x] Enviado %r:%r" % (severities[i], messages[i]))
    time.sleep(2)
connection.close()
