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

from packages.Login.checkLogin import *
import smtplib
import pymysql as MySQLdb
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from packages.Log import kwlog
import string
import hashlib


def check_if_email_exist(email):
    sql = "SELECT * FROM User_Information WHERE Email = '%s';" % (email)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchone()
    db.close()
    kwlog.log("DB closed")
    if not data:
        return False
    else:
        return True


def add_confirmation_to_db(code, username):
    # Adds confirmation code to DB
    # Return bool
    sql = "INSERT INTO `KitchenWizard`.`Activation_Key` (`Key`, `UserID`) VALUES ('%s', '%s');" % (str(code), str(username))
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        kwlog.log("SQL excuted correctly")
        db.commit()
        db.close()
        kwlog.log("DB closed")
        return True
    except:
        db.rollback()
        db.close()
        kwlog.log("Error adding confirmation to DB")
        return False


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


def send_confirmation_email(fname, email, code):
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

        CLICK HERE: http://52.36.126.156?type=activate&code=%s

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
        if send_confirmation_email(fname, email, code):
            kwlog.log("Email sent!")
            return True
        else:
            kwlog.log("Email failed to be sent")
            return False
    except:
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
    kwlog.log("Creating Account")
    d = str(datetime.now())
    date = datetime.today()
    date = date + timedelta(6 * 30)
    hash = encrypt_password(hash)
    f_sql = "INSERT INTO User_Information (UserID, FirstName, LastName, Email, CreationDate) VALUES ('%s', '%s', '%s', '%s', '%s');" % (username, fname, lname, email, d)
    p_sql = "INSERT INTO Password (PasswordHash, User_id, UpdatedOn) VALUES ('%s', '%s', '%s');" % (hash, username, d)
    s_sql = "INSERT INTO Session_Key (SessionKey, UserID, AgeOffDate) VALUES ('%s', '%s', '%s');" % ('000000000', username, date)

    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    try:
        cursor.execute(f_sql)
        kwlog.log("User_Information SQL completed")
        cursor.execute(p_sql)
        kwlog.log("Password SQL completed")
        cursor.execute(s_sql)
        kwlog.log("Session SQL completed")
        kwlog.log("SQL excuted correctly")
        db.commit()
        db.close()
        kwlog.log("DB closed")
        if create_confirmation_email(fname, email, username):
            kwlog.log("Account Created, all good")
            return True
        else:
            kwlog.log("Error during creating confirmation email")
            return True
    except:
        #db.rollback()
        #db.close()
        kwlog.log("Database Error in create account")
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
