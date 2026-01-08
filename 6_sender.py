#utiliza os cabeçalhos das mensagens para rotear as mensagens para as filas corretas

# para rodar vc usa o comando: Python 6_recever.py A error
# pode usar também Python 6_recever.py B info

import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='headers_logs', exchange_type='headers')

messages = ["primeiro log,", "segundo log,", "terceiro log.","quarto log.","quinto log."]
severities = ['info', 'error', 'warning', 'error', 'info']
components = ['A','B','A','A','B']

for i in range(0,5):
    props = pika.BasicProperties(headers={"component": components[i], "severity": severities[i]})
    channel.basic_publish(exchange='headers_logs', routing_key='', body=messages[i], properties=props)
    print(f" [x] Enviado headers %r:%r" % (props.headers, messages[i])) 
    time.sleep(2)
connection.close()
