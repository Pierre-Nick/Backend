###################################################################
#####   `   Supports account update for KitchenWizard         #####
###################################################################
##### Version: 0.1                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  02/22/2016                                     #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to process  #####
#####          all account update request from users that     #####
#####          already have accounts                          #####
###################################################################

from checkLogin import *
from datetime import datetime

debug_on = True
log_level = 3
def log(message, lev):
    # Log messages
    # Return void
    if debug_on:
        if lev <= log_level:
            ti = str(datetime.now())
            print("[%s]updateAccount --> %s" % (ti, message))


def __get_act_code(userid):
    # Get activation form DB
    # Return str
    sql = "SELECT Code FROM Activation_Key WHERE UserID = '%s';" % (userid)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchone()
    db.close()
    log("DB closed", 3)
    return str(data[0])


def __check_code(userid, code):
    # Check code aginst DB
    # Return bool
    d_code = __get_act_code(userid)
    if d_code == code:
        log("Activation code matches", 2)
        return True
    else:
        log("Activation code does not match", 2)
        return False


def __check_act_status(userid):
    # Check if account is activated
    # Return bool
    sql = "SELECT IsActivated FROM User_Information WHERE UserID = '%s';" % (userid)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchone()
    db.close()
    log("DB closed", 3)
    if str(data[0]) == '1':
        return True
    else:
        return False


def __update_act_status(userid):
    # Updates activation status to activated
    # Return bool
    log("Update activation status", 2)
    sql = "UPDATE User_Information SET IsActivated = '1' WHERE UserID = '%s';" % (userid)
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
        log("Error updating activation status to DB", 1)
        return False


def update_account_activation_stats(userid, code):
    # Update activation status if code is correct
    # Return bool
    # Primary
    log("Update activation code, request", 2)
    if user_exist(userid) == "ID_FOUND":
        log("Username exist", 2)
        if not __check_act_status(userid):
            log("Account not activated", 3)
            if __check_code(userid, code):
                if __update_act_status(userid):
                    log("Account activated", 1)
                    return True
                else:
                    log("DB error occured", 2)
                    return False
            else:
                log("Bad activation code",2)
                return False
        else:
            log("Account already activated", 2)
            return False
    else:
        log("Userid not found")
        return False
