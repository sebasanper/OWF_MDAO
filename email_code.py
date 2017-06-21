import base64

def send_message(message):
    from smtplib import SMTP
    memory_access = base64.b64decode("c2ViYXNhbnBlckB5YWhvby5jb20=")
    receivers = [base64.b64decode('c2ViYXNhbnBlckBnbWFpbC5jb20=')]
    probe = base64.b64decode("c2ViYXNhbnBlcg==")
    filename = base64.b64decode("TWlzaGFvcmlvbjEh")
    smtpObj = SMTP(base64.b64decode("c210cC5tYWlsLnlhaG9vLmNvbQ=="))
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login(probe, filename)
    smtpObj.sendmail(memory_access, receivers, message)
    smtpObj.quit()
    print "Succesfully sent"

if __name__ == '__main__':
    send_message("todo escondido")

