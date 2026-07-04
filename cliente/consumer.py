import pika
import time

credenciales = pika.PlainCredentials('admin', 'admin')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='10.220.239.211', port=5672, credentials=credenciales)
)
channel = connection.channel()
channel.queue_declare(queue='redes_tarea2')

def callback(ch, method, properties, body):
    print(f" [!!!] Mensaje recibido del servidor: {body.decode()}")

print(' [*] Consumidor activo. Esperando 20 segundos antes de escuchar...')
time.sleep(20)

print(' [*] Ahora escuchando mensajes. CTRL+C para salir.')
channel.basic_consume(queue='redes_tarea2', on_message_callback=callback, auto_ack=True)
channel.start_consuming()
