import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='10.220.239.211')
)
channel = connection.channel()
channel.queue_declare(queue='redes_tarea2')

message = 'Prueba practica de trafico AMQP a traves de la red ZeroTier.'
channel.basic_publish(exchange='', routing_key='redes_tarea2', body=message)
print(f" [+] Mensaje enviado con exito: '{message}'")
connection.close()
