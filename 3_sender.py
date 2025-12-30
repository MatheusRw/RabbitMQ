import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.exchance_declare(exchange='logs', exchange_type='fanout')

messages = ["primeiro log,", "segundo log,", "terceiro log.","quarto log.","quinto log."]

for message in messages:
    channel.basic_publish(exchange='logs', routing_key='', body=message)
    print(f" [x] Log Enviado '{message}'")
    time.sleep(2)
connection.close()


