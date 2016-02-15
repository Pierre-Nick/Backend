###################################################################
#####   `   Supports Login procedure for KitchenWizard        #####
###################################################################
##### Version: 0.1                                            #####
##### Author:  Marcus Randall                                 #####
##### Tested:  N/A                                            #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to perform  #####
#####          the login process for active users to the      #####
#####          KitchenWizard system.                          #####
###################################################################

import MySQLdb
import random
from datetime import datetime, timedelta

debug_on = True
log_level = 3

def log(message, lev):
    # Log messages
    # Return void
    if debug_on:
        if lev <= log_level:
            ti = str(datetime.now())
            print("[%s]checkLogin --> %s" % (ti, message))


def safetyCheck(usr):
    # Check if userid is not a sql injection
    # Return bool
    if "SELECT" in usr.upper().lower():
        return False
    elif "FROM" in usr.upper().lower():
        return False
    elif "*" in usr.upper().lower():
        return False
    elif "WHERE" in usr.upper().lower():
        return False
    else:
        return True


def user_exist(usr):
    # Check if userid exist
    # Return str
    log("Checking if user is in DB", 1)
    if(safetyCheck(usr)):
        log("safety check, passed", 2)
        db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
        log("Connected to DB", 3)
        cursor = db.cursor()
        sql = "SELECT UserID FROM User_Information WHERE UserID = '%s'" % usr
        cursor.execute(sql)
        log("SQL excuted correctly", 3)
        data = cursor.fetchone()
        db.close()
        log("DB closed", 3)
        if data:
            return "ID_FOUND"
        else:
            return "NO_ID_FOUND"
    else:
        log("safety check, failed", 2)
        return "BAD_ID"


def get_hash_for_user(userid):
    # Get hash for user, return hash
    # Return str
    log("DB request for DB-Password", 1)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    sql = "SELECT PasswordHash FROM Password WHERE User_id = '%s'" % userid
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchone()
    db.close()
    log("DB closed", 3)
    return data



def check_password_hash(userid, hash):
    # Completes password check for user
    # Return bool
    log(("Checking password for login request by %s" % userid), 1)
    dbhash = get_hash_for_user(userid)
    dbhash = str(dbhash[0])
    if dbhash == hash:
        log("Password correct", 2)
        return True
    else:
        log("Password incorrect", 2)
        return False


#def check_password_date(username):
# Check if date has past required reset date (180 days)
# Return bool
# Add in later version (1.0)

def uppdate_session_key(username, ses):
    # Update Session key in DB
    # Return void
    log("DB request update session key", 1)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    date = datetime.today()
    date = date + timedelta(6 * 30)
    sql = "UPDATE `KitchenWizard`.`Session_Key` SET `SessionKey`='%d', `AgeOffDate`='%s' WHERE `USERID`='%s';" % (ses, date, username)
    try:
        cursor.execute(sql)
        log("SQL excuted correctly", 3)
        db.commit()
    except:
        db.rollback()
    db.close()
    log("DB closed", 3)


def check_active_status(username):
    # Checks if account has been activated
    # Return bool
    log("Check status of account", 1)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    sql = "SELECT IsActivated FROM User_Information WHERE User_id = '%s'" % userid
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchone()
    db.close()
    log("DB closed", 3)
    if data[0] == 0:
        log("Account not activated", 2)
        return False
    else:
        log("Account activated", 2)
        return True


def generate_session_key(username):
    # When login complete generate session key
    # Return str
    log("Generating session key", 2)
    ses = random.randint(100000000, 100000000000)
    log("Updating key in DB", 2)
    uppdate_session_key(username, ses)
    ses = str(ses)
    log("Session key returned", 3)
    return ses


def login_to_account(username, password):
    # Performs login of the account
    # Return str
    log(("Login request by ", username), 1)
    if(user_exist(username) == "ID_FOUND"):
        if(check_password_hash(username, password)):
            if(check_active_status(username)):
                log("Vaild login, generating session key", 2)
                ses = generate_session_key(username)
                return ses
            else:
                return "ACCOUNT_NOT_ACTIVE"
        else:
            log("Invaild login", 2)
            return "INVAILD_LOGIN"

else:
    log("Bad login request", 2)
        return "INVAILD_LOGIN"