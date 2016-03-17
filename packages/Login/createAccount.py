###################################################################
#####   `       Create User Account for KitchenWizard         #####
###################################################################
##### Version: 0.2                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  02/18/2016                                     #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to allow    #####
#####          users to create a new account and to make sure #####
#####          all information from the user is vaild         #####
###################################################################

from packages.Login.checkLogin import user_exist
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from packages.Log import kwlog
from validate_email import validate_email
from datetime import datetime, timedelta
from packages.Database import MySQL
import string
import hashlib
import random

def check_if_email_exist(email):
    data = MySQL.is_email_in_database(email)
    if not data:
        return False
    else:
        return True


def add_confirmation_to_db(code, username):
    # Adds confirmation code to DB
    # Return bool
    return MySQL.put_confirmation_code_in_database(code, username)


def generate_confirmation_code(username):
    # Generate confirmation code
    # Return str
    chars=string.ascii_uppercase + string.digits
    code = ''.join(random.choice(chars) for _ in range(25))
    kwlog.log("Code created")
    if add_confirmation_to_db(code, username):
        kwlog.log("Code added to DB")
        return code
    else:
        kwlog.log("Error adding code")
        return "ERROR_ADDING_CODE_DB"


def send_confirmation_email(fname, email, code, userid):
    # Sends confirmation email
    # Return bool
    kwlog.log("Create email request")
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login("homekitchenwizzard@gmail.com", "KitchenWizard")
    kwlog.log("Login to email - complete")
    msg = MIMEMultipart()
    msg['From'] = "homekitchenwizzard@gmail.com"
    msg['To'] = email
    msg['Subject'] = "Welcome To Kitchen Wizard - Account Activation"
    body = """
        Welcome %s,

        Let us be the first to welcome you to the easiest way to track what is happening in your kitchen. Before we get started we need you to complete the activation process by clicking the link below.

        CLICK HERE: http://52.36.126.156:8080?command=activate&code=%s&

        Thank You,
        Kitchen Wizard Support Team
        """ % (fname, code)
    msg.attach(MIMEText(body, 'plain'))
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


def create_confirmation_email(fname, email, username):
    # Generates confirmation email, once account was created
    # Return bool
    try:
        code = generate_confirmation_code(username)
        if code == "ERROR_ADDING_CODE_DB":
            kwlog.log("Unable to add code to DB, Failing")
            return False
        if send_confirmation_email(fname, email, code, username):
            kwlog.log("Email sent!")
            return True
        else:
            kwlog.log("Email failed to be sent")
            return False
    except:
        raise
        kwlog.log("Error during code generation")


def encrypt_password(password):
    # Make password more secure
    # Return str
    kwlog.log("hashing hash")
    h = hashlib.md5()
    h.update(password)
    h.update(b"EVERYONE_LOVES_KITCHENWIZARD!")
    return h.hexdigest()


def create_account(username, fname, lname, email, hash):
    # Create account and add to DB
    # Return bool
    if MySQL.put_new_account(username, fname, lname, email, hash):
        if create_confirmation_email(fname, email, username):
            kwlog.log("Account Created, all good")
            return True
        else:
            kwlog.log("Error during creating confirmation email")
            return False
    else:
        return False


def add_new_user(username, fname, lname, email, hash):
    # Create new account, but must check vaild email and username
    # Return str
    kwlog.log("Request to create a new account")
    if(user_exist(username) == "NO_ID_FOUND"):
        kwlog.log("UserID passed test")
        if check_if_email_exist(email):
            kwlog.log("Email check failed")
            kwlog.log("Email already connected to another account")
            return "ACCOUNT_ALREADY_EXIST_FOR_EMAIL"
        elif not validate_email(str(email)):
            kwlog.log("Email is invaild")
            return "EMAIL_NOT_VAILD"
        else:
            kwlog.log("Checks passed, creating account")
            if create_account(username, fname, lname, email, hash):
                kwlog.log("Account created, sending email confirmation")
            else:
                kwlog.log("Error during account creation")
            return "ACCOUNT_CREATED"
    elif(user_exist(username) == "ID_FOUND"):
        if check_if_email_exist(email):
            kwlog.log("Email check failed")
            kwlog.log("Email already connected to another account")
            return "ACCOUNT_ALREADY_EXIST_FOR_EMAIL"
        else:
            kwlog.log("Username check failed")
            kwlog.log("Username already taken by another user")
            return "USERNAME_TAKEN"
    else:
        kwlog.log("Bad username")
        return "INVAILD_USERNAME"
