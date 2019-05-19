from sms import sendSms, countLines, checkLevelNot
from Email import send_notification
if countLines() % 100 == 0:
        checkLevelNot()
        with open('NotifyNews.txt', 'r') as myfile:
            data = myfile.read()
            with open('log.log', 'r') as myfile2:
                data2 = myfile2.read()
            sendSms("New Alerts : " + data)
            send_notification("alaidleonz@gmail.com", "Nuevas Alertas", "New Alerts : " + data + "\n Details:" + data2  )



