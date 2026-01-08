# O exchange do tipo Topic envia mensagens para filas com base na chave de roteamento
# a chave pode ser por exemplo logs de erro, info, debug 
# Utiliza também de wildcards como * (um palavra) e # (zero ou mais palavras)
#na hora de rodar o scruipt cada consumidor deve passar como argumento a severidade que quer receber
 
# Comando para rodar Python 5_sender.py A.*
# pode rodar o comando com # também para chaves compostas de varios elementos é como um *
# ou também com *.* 
 


import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='topic_logs', exchange_type='topic')

messages = ["primeiro log,", "segundo log,", "terceiro log.","quarto log.","quinto log."]
severities = ['info', 'error', 'warning', 'error', 'info']
components = ['A','B','A','A','B']

for i in range(0,5):
    routing_key = components[i] + '.' + severities[i]
    channel.basic_publish(exchange='topic_logs', routing_key=routing_key, body=messages[i])
    print(f" [x] Enviado %r:%r" % (routing_key, messages[i]))
    time.sleep(2)
connection.close()
