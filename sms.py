from twilio.rest import Client
from itertools import islice

def sendSms(mensaje):
    account_sid = "AC82547c8b8ab90f2700ac5d02de712f4e"
    auth_token = "0c2ecab3139b79769138fe347077d0bb"
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        to="+5215572316487",
        from_="+12028835634",
        body=mensaje)
    print ("Mensaje enviado")
    print(message.sid)



def countLines():
    fname = "log.log"
    num_lines = 0
    with open(fname, 'r') as f:
        for line in f:
            num_lines += 1
    print("Numero de lineas del archivo:")
    print(num_lines)
    return  num_lines

def checkLevelNot():
    filepath = 'log.log'
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        level0 = 0
        level1 = 0
        level2 = 0
        level3 = 0
        level4 = 0
        level5 = 0
        otro = 0
        while line:
            print("Line {}: {}".format(cnt, line.strip()))
            line = fp.readline()
            cnt += 1
            if (line.strip().find('SYS-5') != -1):
                level5 += 1
            elif (line.strip().find('SYS-4') != -1):
                level4 = level4 + 1
            elif (line.strip().find('SYS-3') != -1):
                level3 = level3 + 1
            elif (line.strip().find('SYS-2') != -1):
                level2 = level2 + 1
            elif (line.strip().find('SYS-1') != -1):
                level1 = level1 + 1
            elif (line.strip().find('SYS-0') != -1):
                level0 = level0 + 1
            else:
                otro = otro + 1
    f = open("NotifyNews.txt", "w")
    f.write("lv5:" + str(level5) + " ")
    f.write("lv4:" + str(level4) + " ")
    f.write("lv3:" + str(level3) + " ")
    f.write("lv2:" + str(level2) + " ")
    f.write("lv1:" + str(level1) + " ")
    f.write("lv0:" + str(level0) + " ")
    f.write("other:" + str(otro))

