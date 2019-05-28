import subprocess
import threading
import time


ip1 = '50.0.0.1'
ip2 = '10.0.80.6'

def ping(ip, segundos):
    go = True
    inicial = time.time()
    limite = inicial + segundos
    while go:
        res = subprocess.call(['ping', '-c', '1', ip], stdout=False)
        if time.time() >= limite:
            go = False


def h1():
    print("hilo1")
    ping(ip1, 60)
    time.sleep(60)
    print("hilo1")
    ping(ip1, 60)


def h2():
    print("hilo2")
    ping(ip2, 120)
    time.sleep(60)
    print("hilo2")
    ping(ip2, 120)


h1 = threading.Thread(target=h1)
h2 = threading.Thread(target=h2)
h1.run()
h2.run()
time.sleep(500)
