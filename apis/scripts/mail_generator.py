from config import *
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.utils import make_msgid
from email.utils import formatdate

class Mail:

    def __init__(self,host,password):
        self.host = host
        self.password = password

    def send_mail(self,to=None,subject="web app report",body="",format="html",attachments=[],cc=None):
#         to_all = ["web_app_automation_watchers"]
        to_all=[]
        if to:
            to_all.extend(to)
        else:
            to_all.extend(["web_app_automation_watchers"])
        msg = MIMEMultipart()
        msg['To'] = ",".join(to_all)
        msg['From'] = self.host
        if cc:
            msg['Cc'] = ",".join(cc)
        msg['Message-Id'] = make_msgid()
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, format))
        for filename in attachments:
            part = MIMEApplication(open(filename).read())
            part.add_header('Content-Disposition',
                'attachment; filename="%s"' % os.path.basename(filename))
            msg.attach(part)

        try:
            srv = smtplib.SMTP('smtp.gmail.com')
            srv.set_debuglevel(1)
            srv.ehlo()
            srv.starttls()
            srv.ehlo()
            srv.login(self.host,self.password)
            srv.sendmail(msg['From'],to, msg.as_string())
            srv.quit()
            print("Mail sent successfully")
        except Exception as e:
            print("Mail not success fully", str(e))


    def send_mail_outlook(self,to=[],subject="web app report",body="",format="html",attachments=[]):
        msg = MIMEMultipart()
#         print(msg.keys())
        msg['To'] = "web_app_automation_watchers"
        msg['From'] = self.host
        msg['Message-Id'] = make_msgid()
        msg['Date'] = formatdate(localtime=True)
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        for filename in attachments:
            part = MIMEApplication(open(filename).read())
            part.add_header('Content-Disposition',
                'attachment; filename="%s"' % os.path.basename(filename))
            msg.attach(part)

        try:
            srv = smtplib.SMTP('smtp.office365.com')
            srv.set_debuglevel(1)
            srv.ehlo()
            srv.starttls()
            srv.ehlo()
            srv.login(self.host,self.password)
            srv.sendmail(msg['From'],to, msg.as_string())
            srv.quit()
            print("Mail sent successfully")
        except Exception as e:
            print("Mail not success fully", str(e))


if __name__ == '__main__':
    host="wittyautoreport@gmail.com"
    password = "WittyReport"

#     host = "dhaneesh@wittyparrot.com"
#     password = "Vidya@11"
    to = ['dhaneesh@wittyparrot.com']
    subject = "web app automation report"
    body = "web app automation ran on 6/16/2015"
#     format = "html"
#     attachments =[]
# #     attachments.append("C:/Users/Dhaneesh/Desktop/today_16_6.html")
    mail = Mail(host,password)
    mail.send_mail(to=to, subject=subject, body=body, Cc=['dhaneeshattesting@gmail.com'])
#     mail.send_mail_outlook(to, subject, body, format, attachments)
    pass
