from dbs import dbs
from scripts import mail_generator



def validate_headers(headers,validate_token=True,validate_content_type=True):
    try:
        if validate_content_type:
            if not "Content-Type" in headers:
                return {"status":False,"remarks":"please contact adminstrator"}
            elif not headers["Content-Type"] == "application/json":
                return {"status":False,"remarks":"please contact adminstrator"}
            elif not validate_token:
                return {"status":True,"remarks":"headers validated"}

        if validate_token:
            if "Authorization" in headers:
                # query = conn.execute("select * from users where access_token='{access_token}'".format(access_token=access_token))
                d_s = dbs.get_row("users",which_="all",where_={"access_token":headers["Authorization"]})
                # print("d_s",d_s)
                q_c = list(d_s["values"])
                if q_c:
                    details = list(q_c[0])
                    return {"status":True,"email":details[0],"access_token":details[1]}
                else:
                    return {"status":False,"remarks":"Invalid access token"}
            else:
                return {"status":False,"remarks":"please provide access token"}
    except Exception as e:
        return {"status":False,"remarks":str(e)}

def drop_user_creation_email(data):

    host="wittyautoreport@gmail.com"
    password = "WittyReport"
    to = [data['email']]
    subject = "web app automation report"
    body = "<div>Hi {name},</div><br><div>Welcome to AutoReport, An account is created  with {email} and your password would be <div><b>{password}.</b></div></div><br><div>Login at <a href='http://52.172.27.204:443/'> <u>AutoReport Website </u></a></div><br><br>".format(name=data['name'].capitalize(),email=data['email'],password=data['password'])+"Regards,<br>AutoReport Support"
    format_type = "html"
    mail = mail_generator.Mail(host,password)
    mail.send_mail(to, subject, body, format=format_type)
