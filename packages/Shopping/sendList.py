import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from packages.Log import kwlog
from validate_email import validate_email
from datetime import datetime, timedelta
from packages.Database import MySQL
from packages.Items.addItem import __get_userid_from_key

def __create_list(sid):
    l = list(get_list_of_shopping_items(sid))
    final = ""
    for k in l:
        final = final + "<li>" + str(MySQL.get_group_name_from_group_id(gidk[2])) + "</li>"
    return final


def __send_email(userid, sid):
    email = MySQL.get_email_for_user(userid)
    list_str = __create_list

    if list_str == "FAILED":
        return False

    kwlog.log("Create email request")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("homekitchenwizzard@gmail.com", "KitchenWizard")
    kwlog.log("Login to email - complete")
    msg = MIMEMultipart()
    msg['From'] = "homekitchenwizzard@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Kitchen Wizard - Shopping List"
    body = """
        <html>
            <head></head>
            <body>
                <h1>Shopping List</h1>
                <ul>%s</ul>
            </body>
        </html>
        """ % (list_str)
    msg.attach(MIMEText(body, 'html'))
    kwlog.log("Sending message...")
    try:
        server.sendmail("homekitchenwizzard@gmail.com", email, msg.as_string())
        server.close()
        kwlog.log("Message sent")
        return True
    except:
        server.close()
        kwlog.log("Message Failed")
        return False


def send_list(sid, session_key):
    userid =  __get_userid_from_key(session_key)

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    if not MySQL.is_vaild_shopping_list(sid, userid):
        kwlog.log("Invaild Shopping List")
        return "BAD_LIST"
    if not __send_email(userid):
        kwlog.log("Failed to send shopping list")
        return "SEND_FAILED"
    else:
        return "EMAIL_SENT"
