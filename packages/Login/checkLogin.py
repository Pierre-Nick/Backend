###################################################################
#####   `   Supports Login procedure for KitchenWizard        #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  02/12/2016                                     #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to perform  #####
#####          the login process for active users to the      #####
#####          KitchenWizard system.                          #####
###################################################################

import pymysql as MySQLdb
import random
from datetime import datetime, timedelta
import hashlib
from packages.Log import kwlog


def encrypt_password(password):
    # Make password more secure
    # Return str
    kwlog.log("hashing hash")
    h = hashlib.md5()
    h.update(password)
    h.update(b"EVERYONE_LOVES_KITCHENWIZARD!")
    return h.hexdigest()


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
    kwlog.log("Checking if user is in DB")
    if(safetyCheck(usr)):
        kwlog.log("safety check, passed")
        db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
        kwlog.log("Connected to DB")
        cursor = db.cursor()
        sql = "SELECT UserID FROM User_Information WHERE UserID = '%s'" % usr
        cursor.execute(sql)
        kwlog.log("SQL excuted correctly")
        data = cursor.fetchone()
        db.close()
        kwlog.log("DB closed")
        if data:
            return "ID_FOUND"
        else:
            return "NO_ID_FOUND"
    else:
        kwlog.log("safety check, failed")
        return "BAD_ID"


def get_hash_for_user(userid):
    # Get hash for user, return hash
    # Return str
    kwlog.log("DB request for DB-Password")
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    sql = "SELECT PasswordHash FROM Password WHERE User_id = '%s'" % userid
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchone()
    db.close()
    kwlog.log("DB closed")
    return data


def check_password_hash(userid, hash):
    # Completes password check for user
    # Return bool
    kwlog.log(("Checking password for login request by %s" % userid))
    dbhash = get_hash_for_user(userid)
    dbhash = str(dbhash[0])
    hash = encrypt_password(hash)
    if dbhash == hash:
        kwlog.log("Password correct")
        return True
    else:
        kwlog.log("Password incorrect")
        return False


#def check_password_date(username):
# Check if date has past required reset date (180 days)
# Return bool
# Add in later version (1.0)

def uppdate_session_key(username, ses):
    # Update Session key in DB
    # Return void
    kwlog.log("DB request update session key")
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    date = datetime.today()
    date = date + timedelta(6 * 30)
    sql = "UPDATE `KitchenWizard`.`Session_Key` SET `SessionKey`='%d', `AgeOffDate`='%s' WHERE `USERID`='%s';" % (ses, date, username)
    try:
        cursor.execute(sql)
        kwlog.log("SQL excuted correctly")
        db.commit()
    except:
        db.rollback()
    db.close()
    kwlog.log("DB closed")


def check_active_status(username):
    # Checks if account has been activated
    # Return bool
    kwlog.log("Check status of account")
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    sql = "SELECT IsActivated FROM User_Information WHERE UserID = '%s'" % username
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchone()
    db.close()
    kwlog.log("DB closed")
    if data[0] == 0:
        kwlog.log("Account not activated")
        return False
    else:
        kwlog.log("Account activated")
        return True


def generate_session_key(username):
    # When login complete generate session key
    # Return str
    kwlog.log("Generating session key")
    ses = random.randint(100000000, 100000000000)
    kwlog.log("Updating key in DB")
    uppdate_session_key(username, ses)
    ses = str(ses)
    kwlog.log("Session key returned")
    return ses


def login_to_account(username, password):
    # Performs login of the account
    # Return str
    kwlog.log(("Login request by " + username))
    if(user_exist(username) == "ID_FOUND"):
        if(check_password_hash(username, password)):
            if(check_active_status(username)):
                kwlog.log("Vaild login, generating session key")
                ses = generate_session_key(username)
                return ses
            else:
                return "ACCOUNT_NOT_ACTIVE"
        else:
            kwlog.log("Invaild login")
            return "INVAILD_LOGIN"

    else:
        kwlog.log("Bad login request")
        return "INVAILD_LOGIN"
