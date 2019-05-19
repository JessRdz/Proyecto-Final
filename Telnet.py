import telnetlib

routers = {"r1": "50.0.0.1", "r4": "10.0.3.2"}

for router, direccion in routers.items():
    tn = telnetlib.Telnet(direccion)

    print(tn.read_until(str.encode("Password: ")).decode())
    tn.write(str.encode("pass\n"))

    tn.write(str.encode("enable\npass\nconfig t\nip ftp username sonia\nip ftp password Heladodelimon05\nexit\n"))

    tn.write(str.encode("copy ftp: startup-config\n50.0.0.2\n" + router + "\n\nexit\n"))

    print((tn.read_all()).decode())