###################################################################
#####   `       Create User Account for KitchenWizard         #####
###################################################################
##### Version: 0.1                                            #####
##### Author:  Marcus Randall                                 #####
##### Tested:  N/A                                            #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to allow    #####
#####          users to create a new account and to make sure #####
#####          all information from the user is vaild         #####
###################################################################

from checkLogin import *

debug_on = True
log_level = 3

def log(message, lev):
    # Log messages
    # Return N/A
    if debug_on:
        if lev <= log_level:
            ti = str(datetime.now())
            print("[%s]createAccount --> %s" % (ti, message))


def check_if_email_exist():
    return False


def create_account(username, fname, lname, email, hash):
    # Create account and add to DB
    # Return bool
    log("Creating Account", 1)
    d = str(datetime.now())
    date = datetime.today()
    date = date + timedelta(6 * 30)
    f_sql = "INSERT INTO User_Information (UserID, FirstName, LastName, Email, CreationDate) VALUES ('%s', '%s', '%s', '%s', '%s');" % (username, fname, lname, email, d)
    p_sql = "INSERT INTO Password (PasswordHash, User_id, UpdatedOn) VALUES ('%s', '%s', '%s');" % (hash, username, d)
    s_sql = "INSERT INTO Session_Key (SessionKey, UserID, AgeOffDate) VALUES ('%s', '%s', '%s');" % ('000000000', username, date)
    
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    try:
        cursor.execute(f_sql)
        log("User_Information SQL completed", 3)
        cursor.execute(p_sql)
        log("Password SQL completed", 3)
        cursor.execute(s_sql)
        log("Session SQL completed", 3)
        log("SQL excuted correctly", 2)
        db.commit()
        if not create_confirmation_email(fname, email, username):
            return False
        else:
            db.close()
            log("DB closed", 3)
            return True
    except:
        db.rollback()
        db.close()
        return False
def add_confirmation_to_db(code, username):
    # Adds confirmation code to DB
    # Return bool
    sql = "INSERT INTO Activation_Key (Key, UserID) VALUES ('%s', '%s');" % (code, username)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        log("SQL excuted correctly", 2)
        db.commit()
        db.close()
        log("DB closed", 3)
        return True
    except:
        db.rollback()
        db.close()
        return False


def generate_confirmation_code(username):
    # Generate confirmation code
    # Return str
    chars=string.ascii_uppercase + string.digits
    code = ''.join(random.choice(chars) for _ in range(25))
    if add_confirmation_to_db(code):
        return code
    else:
        return "ERROR_ADDING_CODE_DB"


def send_confirmation_email(fname, email, code):
    # Sends confirmation email
    # Return bool
    # Need more research to send email
    return True


def create_confirmation_email(fname, email, username):
    # Generates confirmation email, once account was created
    # Return bool
    code = generate_confirmation_code(username)
    if code == "ERROR_ADDING_CODE_DB":
        log("Unable to add code to DB, Failing", 1)
        return False
    if send_confirmation_email(fname, email, code):
        log("Email sent!", 2)
        return True
    else:
        log("Email failed to be sent", 2)
        return False


def add_new_user(username, fname, lname, email, hash):
    # Create new account, but must check vaild email and username
    # Return str
    log("Request to create a new account", 1)
    if(user_exist("mr7657") == "NO_ID_FOUND"):
        log("UserID passed test", 2)
        if check_if_email_exist():
            log("Email check failed", 2)
            log("Email already connected to another account", 3)
            return "ACCOUNT_ALREADY_EXIST_FOR_EMAIL"
        else:
            log("Checks passed, creating account", 2)
            if create_account(username, fname, lname, email, hash):
                log("Account created, sending email confirmation", 1)
            else:
                log("Error during account creation", 1)
            return "ACCOUNT_CREATED"
    elif(user_exist("mr7657") == "ID_FOUND"):
        if check_if_email_exist():
            log("Email check failed", 2)
            log("Email already connected to another account", 3)
            return "ACCOUNT_ALREADY_EXIST_FOR_EMAIL"
        else:
            log("Username check failed", 2)
            log("Username already taken by another user", 3)
            return "USERNAME_TAKEN"
    else:
        log("Bad username", 2)
        return "INVAILD_USERNAME"
