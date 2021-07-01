import socket
import time
import struct
import random
import threading
from threading import Thread
from Queue import Queue


my_list = ["www.gnoosic.com","www.namasha.com"]
queue=Queue()
for host in my_list:
    queue.put(host)
    print("The host "+format(host)+" added for pinging.")

def make_packet(data = 'd'):
    raw = struct.pack(
        'bbHHh',
        8, #type //icmp_echo_request
        0, #code
        0, #checksm
        1, #id
        1, #seq
    )


    raw = struct.pack(
        'bbHHh',
        8,
        0,
        checksum(raw + data),
        1,
        1,
    )

    packet = raw + data
    return packet

def worker_pinger():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW,1)
    mypacket = make_packet()
    while not queue.empty():
        host = queue.get()
    
        for packet in range(4):# packet size
            sock.sendto(mypacket, (host, 1))
            time_sent = time.time()
            sock.settimeout(1)

            try:
                received= sock.recvfrom(4096)
                time_received = time.time()
                print("reply from<"+format(host)+"> in "+format(time_received-time_sent)+" ms")
            except:
                print("reply from "+ format(host)+" was timed out ")
                
            
def run_Ping(threadslen):
    threads = []

    for t in range(threadslen):
        thread = threading.Thread(target=worker_pinger)
        threads.append(thread)
        thread.start()

    for t in threads:
        t.join() 


def checksum(packet):
    sum = 0
    for i in range(0, len(packet), 2):
        a = ord(packet[i])
        b = ord(packet[i+1])
        sum = sum + (a+(b<<8))

    sum = sum + (sum>>16)
    sum = ~sum & 0xffff

    return sum


run_Ping(4)
