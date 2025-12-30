import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

messages = ["primeira mensagem,", "segunda mensagem,", "terceira mensagem.","quarta mensagem.","quinta mensagem."]



for message in messages:
    channel.basic_publish(exchange='', routing_key='hello', body=message)
    print(f" [x] Mensagem Enviada '{message}'")
    time.sleep(1)  # Simula um atraso entre as mensagens

connection.close() 