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
from packages.Database import MySQL
from packages.Items.addItem import __get_userid_from_key
from packages.Items.updateItem import __vaildate_sessionkey


def __check_code(userid, code):
    # Check code aginst DB
    # Return bool
    d_code = MySQL.get_act_code(userid)
    if d_code == code:
        kwlog.log("Activation code matches")
        return True
    else:
        kwlog.log("Activation code does not match")
        return False


def __check_act_status(userid):
    # Check if account is activated
    # Return bool
    data = MySQL.get_active_status(userid)
    if str(data[0]) == '1':
        return True
    else:
        return False


def __update_act_status(userid):
    # Updates activation status to activated
    # Return bool
    return MySQL.update_activation_status_for_user(userid)


def __encrypt_password(password):
    # Make password more secure
    # Return str
    kwlog.log("hashing hash")
    h = hashlib.md5()
    h.update(password)
    h.update(b"EVERYONE_LOVES_KITCHENWIZARD!")
    return h.hexdigest()


def __get_userid_from_key(key):
    # Gets userid from session key
    # Return str
    kwlog.log("Get userid from key")
    if(__vaildate_sessionkey(key)):
        return __get_userid_from_key(key)
    else:
        return "BAD_KEY"


def __get_userid_from_activation_code(code):
    # Get userid linked with act code
    # Return: str
    return MySQL.get_userid_linked_to_act_code(code)


def update_account_activation_stats(code):
    # Update activation status if code is correct
    # Return bool
    kwlog.log("Update activation code, request")
    userid = __get_userid_from_activation_code(code)
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


def update_account_information(fname, lname, email, password, sessionkey):
    kwlog.log("request to update account information")
    userid = __get_userid_from_key(sessionkey)
    if len(fname) > 0:
        if not MySQL.update_first_name_for_user(userid, fname):
            return False
    if len(lname) > 0:
        if not MySQL.update_last_name_for_user(userid, lname):
            return False
    if len(email) > 0:
        if not MySQL.update_email_for_user(userid, email):
            return False
    if len(password) > 0:
        password = __encrypt_password(password)
        if not MySQL.update_password_for_user(userid, password):
            return False
    return True
