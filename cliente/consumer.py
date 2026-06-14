import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='10.220.239.211')
)
channel = connection.channel()
channel.queue_declare(queue='redes_tarea2')

def callback(ch, method, properties, body):
    print(f" [!!!] Mensaje recibido del servidor: {body.decode()}")

channel.basic_consume(queue='redes_tarea2', on_message_callback=callback, auto_ack=True)
print(' [*] Consumidor activo. Esperando mensajes. CTRL+C para salir.')
channel.start_consuming()
