import pika
import time
def callback(ch, method, properties, body):
    print(" [x] Mensagem Recebida %r" % body)
    time.sleep(2)
    print(" [x] Processamento da mensagem concluído")
    ch.basic_ack(delivery_tag=method.delivery_tag)


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()


channel.queue_declare(queue='hello')

channel.basic_consume(queue='hello', on_message_callback=callback, auto_ack=False)

print(' [*] Aguardando por mensagens. Para sair pressione CTRL+C')

channel.start_consuming()
