#!/usr/bin/env python3
import pika, time
conn = pika.BlockingConnection(pika.ConnectionParameters(host='10.220.239.211', heartbeat=10))
ch = conn.channel(); ch.queue_declare(queue='redes_tarea2')
N, t0 = 100, time.time()
for i in range(N):
    ch.basic_publish(exchange='', routing_key='redes_tarea2', body=f'msg {i}')
dt = time.time()-t0
print(f"{N} mensajes en {dt:.3f}s -> {N/dt:.1f} msg/s")
conn.close()
