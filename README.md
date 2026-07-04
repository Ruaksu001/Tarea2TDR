# Tarea 2/3
link video tarea 2 -> https://youtu.be/mAZLMaACt_s
link video tarea 3 -> https://youtu.be/iaBkwlvFP_o
> Taller de Redes y Servicios · Universidad Diego Portales · Semestre 2026-1

Despliegue y análisis de una arquitectura de mensajería **AMQP 0-9-1** entre dos máquinas
Linux conectadas por una red privada **ZeroTier**, usando contenedores **Docker construidos
con Dockerfiles propios**. El servidor es **RabbitMQ** y el cliente la biblioteca **Pika**;
el tráfico generado se captura y disecciona con **Wireshark**.

## Tabla de contenidos

- [Descripción](#descripción)
- [Arquitectura](#arquitectura)
- [Requisitos previos](#requisitos-previos)
- [Estructura del repositorio](#estructura-del-repositorio)
- [Instalación y uso](#instalación-y-uso)
  - [1. Servidor (RabbitMQ)](#1-servidor-rabbitmq)
  - [2. Cliente (Pika)](#2-cliente-pika)
  - [3. Análisis de tráfico](#3-análisis-de-tráfico)
- [Tecnologías](#tecnologías)
- [Autores](#autores)

## Descripción

El protocolo asignado fue **AMQP**. El par de software original era **Apache ActiveMQ +
Pika**, pero resultó incompatible: ActiveMQ expone AMQP **1.0** y Pika implementa solo AMQP
**0-9-1**, por lo que el *handshake* no se completa. Con autorización del equipo docente se
sustituyó el servidor por **RabbitMQ 3.13.7**, compatible nativamente con Pika, manteniendo
AMQP como objeto de estudio.

Ambos extremos corren en contenedores Docker creados con su propio Dockerfile, no con las
imágenes oficiales sin modificar.

## Arquitectura

| Nodo | Rol | IP ZeroTier | SO | Servicios |
|------|-----|-------------|----|-----------|
| Matías | Servidor | `10.220.239.211` | CachyOS (Linux) | 5672 (AMQP), 15672 (Web) |
| Lucas | Cliente | `10.220.239.95` | Ubuntu (VM) | `mi_cliente_python` |

Red ZeroTier: **my-first-network** · ID `633e31d8a2bf6c67`

```
[ producer.py / consumer.py ]        [ RabbitMQ broker ]
        Pika (cliente)    --- AMQP 5672 --->   imagen_servidor_rabbitmq
        10.220.239.95        (túnel ZeroTier)      10.220.239.211
```

## Requisitos previos

- Docker instalado en ambos nodos.
- ZeroTier instalado y ambos nodos autorizados en la red `633e31d8a2bf6c67`.
- Wireshark (en el nodo cliente) para la captura de tráfico.

## Estructura del repositorio

```
Tarea2TDR/
├── servidor/
│   └── Dockerfile            # Imagen propia de RabbitMQ (FROM rabbitmq:3)
├── cliente/
│   ├── Dockerfile            # Imagen propia con Python + Pika
│   ├── requirements.txt
│   ├── producer.py           # Publica el mensaje en la cola
│   └── consumer.py           # Se subscribe y recibe el mensaje
├── capturas/
│   └── CapturaAMQP.pcapng    # Captura de tráfico Wireshark
├── informe/
│   └── Tarea2.pdf            # Informe (capítulos I y II)
└── README.md
```

## Instalación y uso

### 1. Servidor (RabbitMQ)

En el nodo de Matías (`10.220.239.211`):

```bash
cd servidor
sudo docker build -t imagen_servidor_rabbitmq .
sudo docker run -d --hostname rabbitmq --name rabbitmq_server \
  -p 5672:5672 -p 15672:15672 imagen_servidor_rabbitmq
sudo docker ps
```

Panel de administración web: `http://10.220.239.211:15672` (usuario `guest`, clave `guest`).

### 2. Cliente (Pika)

En el nodo de Lucas (`10.220.239.95`):

```bash
cd cliente
sudo docker build -t imagen_cliente_pika .
sudo docker run -d --name mi_cliente_python imagen_cliente_pika

# Terminal 1 — consumidor (queda esperando)
sudo docker exec -it mi_cliente_python python consumer.py

# Terminal 2 — productor (envía el mensaje)
sudo docker exec -it mi_cliente_python python producer.py
```

Salida esperada:

```
[+] Mensaje enviado con exito: 'Prueba practica de trafico AMQP a traves de la red ZeroTier.'
[!!!] Mensaje recibido del servidor: Prueba practica de trafico AMQP a traves de la red ZeroTier.
```

### 3. Análisis de tráfico

Captura realizada con Wireshark sobre la interfaz virtual `ztxooi5ngf` (ZeroTier),
aplicando el filtro de visualización `amqp`. El archivo resultante es
`capturas/CapturaAMQP.pcapng` (53 paquetes totales, 30 AMQP). En él se observan el
*handshake*, el `Basic.Publish` (paquete 42) y el `Basic.Deliver` (paquete 48), con el
payload visible en texto plano.

## Tecnologías

- **RabbitMQ 3.13.7** — message broker (servidor)
- **Pika 1.3.2** — cliente AMQP en Python
- **Python 3.10**
- **Docker** — contenerización con imágenes propias
- **ZeroTier** — red privada virtual
- **Wireshark** — análisis de tráfico
- **AMQP 0-9-1** — protocolo de mensajería

## Autores

- **Lucas Herrada** — nodo cliente (Pika / Wireshark)
- **Matías Cáceres** — nodo servidor (RabbitMQ)
