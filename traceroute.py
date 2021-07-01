import socket
import random

dst = "www.google.com"
hops = 30
ttl = 1
# Pick up a random port
port = random.choice(range(33434, 33535))

def run():
    try:
        dst_ip = socket.gethostbyname(dst)
    except socket.error as e:
        raise IOError('Unable to resolve {}: {}',dst, e)

    text = 'traceroute to {} ({}), {} hops max'.format(
        dst,
        dst_ip,
        hops
        )

    print(text)

    while True:
        receiver = create_receiver() 
        sender = create_sender()
        sender.sendto(b'', (dst,port))
        addr = None
        try:
            data, addr = receiver.recvfrom(1024)
        except socket.error as e:
            raise IOError('Socket error :{}'.format(e))
        finally:
            receiver.close()                
            sender.close()
        if addr:
            print('{:<4} {}'.format(ttl, addr[0]))
        else:
            print('{:<4} *'.format(ttl))
        ttl=ttl+1

        if addr[0] == dst_ip or ttl > hops:
            break

def create_receiver():
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_RAW,
        proto=socket.IPPROTO_ICMP
        )
    try:
        s.bind(('',port))
    except socket.error as e:
        raise IOError('Unable to bind receiver socket: {}'.format(e))
    return s

def create_sender():
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_DGRAM,
        proto=socket.IPPROTO_UDP
        )
    s.setsockopt(socket.SOL_IP, socket.IP_TTL,ttl)

    return s
run()    