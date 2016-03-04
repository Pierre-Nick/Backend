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

from packages.Login.checkLogin import *
from datetime import datetime
from packages.Log import kwlog
import pymysql as MySQLdb


def __get_act_code(userid):
    # Get activation form DB
    # Return str
    sql = "SELECT Code FROM Activation_Key WHERE UserID = '%s';" % (userid)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchone()
    db.close()
    kwlog.log("DB closed")
    return str(data[0])


def __check_code(userid, code):
    # Check code aginst DB
    # Return bool
    d_code = __get_act_code(userid)
    if d_code == code:
        kwlog.log("Activation code matches")
        return True
    else:
        kwlog.log("Activation code does not match")
        return False


def __check_act_status(userid):
    # Check if account is activated
    # Return bool
    sql = "SELECT IsActivated FROM User_Information WHERE UserID = '%s';" % (userid)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchone()
    db.close()
    kwlog.log("DB closed")
    if str(data[0]) == '1':
        return True
    else:
        return False


def __update_act_status(userid):
    # Updates activation status to activated
    # Return bool
    kwlog.log("Update activation status")
    sql = "UPDATE User_Information SET IsActivated = '1' WHERE UserID = '%s';" % (userid)
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
        kwlog.log("Error updating activation status to DB")
        return False


def update_account_activation_stats(userid, code):
    # Update activation status if code is correct
    # Return bool
    # Primary
    kwlog.log("Update activation code, request")
    if user_exist(userid) == "ID_FOUND":
        kwlog.log("Username exist")
        if not __check_act_status(userid):
            kwlog.log("Account not activated")
            if __check_code(userid, code):
                if __update_act_status(userid):
                    kwlog.log("Account activated")
                    return True
                else:
                    kwlog.log("DB error occured")
                    return False
            else:
                kwlog.log("Bad activation code")
                return False
        else:
            kwlog.log("Account already activated")
            return False
    else:
        kwlog.log("Userid not found")
        return False
