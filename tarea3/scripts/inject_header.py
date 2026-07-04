#!/usr/bin/env python3
import socket
import time

SERVIDOR = "10.220.239.211"
PUERTO = 5672

# Cabecera AMQP pidiendo una version inexistente (9-9)
payload = b"AMQP\x00\x00\x09\x09"

print(f"[*] Conectando a {SERVIDOR}:{PUERTO}...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVIDOR, PUERTO))
print(f"[+] Conectado exitosamente.")

print(f"\n[*] Enviando cabecera AMQP con version 9-9 (inexistente)...")
print(f"[*] Payload: {payload.hex()} ({payload})")
s.send(payload)
time.sleep(0.5)

print(f"\n[*] Esperando respuesta del broker...")
resp = s.recv(128)

print(f"\n[<] RESPUESTA DEL BROKER:")
print(f"[<] Respuesta cruda (hex): {resp.hex()}")
print(f"[<] Respuesta cruda: {resp}")

if resp.startswith(b'AMQP'):
    print(f"\n[!] NEGOCIACION DE VERSION:")
    print(f"[!] Protocolo: {resp[:4]}")
    print(f"[!] Version soportada por RabbitMQ: {resp[4]}.{resp[5]}.{resp[6]}.{resp[7]}")
    print(f"[!] Bytes de version: {list(resp[4:8])}")
    print(f"\n[!] El broker RECHAZA la version 9-9 y responde con su propia version 0-9-1")
else:
    print(f"[!] Respuesta no es una cabecera AMQP valida")

s.close()
print(f"\n[*] Conexion cerrada por el broker.")
