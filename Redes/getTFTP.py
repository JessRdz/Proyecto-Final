import tftpy

routers = {"r1": "50.0.0.1", "r2": "10.0.1.1", "r3": "10.0.2.2", "r4": "10.0.3.2", "r5": "10.0.4.2", "r6": "10.0.7.2",
           "r7": "10.0.7.1", "r8": "50.0.1.2", "r9": "50.0.4.2", "r10": "50.0.2.2", "r11": "50.0.3.2",
           "r12": "20.0.1.1", "r13": "20.0.1.2", "r14": "20.0.4.1", "r15": "20.0.2.2", "r16": "20.0.8.1",
           "r17": "20.0.7.2", "r18": "30.0.1.1", "r19": "30.0.1.2", "r20": "30.0.2.2"}

for router, direccion in routers.items():
    try:
        tftpy.TftpClient(direccion, 69).download('startup-config', router)
    except:
        print("Falló la comunicación con " + router + ":" + direccion)