#!/usr/bin/env python3
from scapy.all import sniff, TCP, IP, Raw

IFACE = "ztxooi5ngf"

def procesar(pkt):
    if pkt.haslayer(Raw) and pkt.haslayer(TCP):
        carga = bytes(pkt[Raw].load)
        if b"redes_tarea2" in carga or b"Prueba" in carga:
            print(f"[{pkt[IP].src}:{pkt[TCP].sport} -> {pkt[IP].dst}:{pkt[TCP].dport}]")
            texto = "".join(chr(b) if 32 <= b < 127 else "." for b in carga)
            print("  ASCII :", texto)
            print("-"*60)

print(f"[*] Interceptando AMQP en {IFACE} (puerto 5672)...")
sniff(iface=IFACE, filter="tcp port 5672", prn=procesar, store=False)
