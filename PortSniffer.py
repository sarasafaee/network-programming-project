from queue import Queue
import socket
import threading
import time

# set the domain
domain = "vu.um.ac.ir"
print_lock = threading.Lock()

def portsnif(port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # set time out
        s.settimeout(0.4)
        s.connect((domain,port))
        with print_lock:
            print('Port: ' + str(port) + ' is open')
        s.close()
        
        return True
    except:
        return False

queue = Queue()

def put_ports(g_type):
    if g_type == 1:
        for port in range(1, 1500):
            queue.put(port)

    elif g_type == 2:
        reserved_ports = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443]
        for port in reserved_ports:
            queue.put(port)
    elif g_type == 3: 
        print("Enter a number 1.HTTP 2.TLS 3.SMTP 4.FTP 5.TELNET 6.SSH")
        number=input()
        if int(number) == 1:
            queue.put(80)
        elif int(number) == 2:
            queue.put(443)
        elif int(number) == 3:
            queue.put(25)
        elif int(number) == 4:
            queue.put(20)
            queue.put(21)
        elif int(number) == 5:
            queue.put(23)
        elif int(number) == 6: 
            queue.put(22)               
                
open_ports = []
close_ports = []
def worker():
    while not queue.empty():
        port = queue.get()
        tstart=time.time()
        if portsnif(port):
            tend=time.time()
            print("time taken ="+format(tend-tstart))
            open_ports.append(port)
        else:
            close_ports.append(port)    

def run_Sniffer(threadslen, type):

    put_ports(type)

    threads = []

    for t in range(threadslen):
        thread = threading.Thread(target=worker)
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for t in threads:
        t.join() 

    print("Open ports :", open_ports)
    # print("Close ports :", close_ports)


# set amount of treads and the type of get_ports
run_Sniffer(150, 2)                           
