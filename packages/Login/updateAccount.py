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
    data = get_active_status(userid)
    if str(data[0]) == '1':
        return True
    else:
        return False


def __update_act_status(userid):
    # Updates activation status to activated
    # Return bool
    return MySQL.update_activation_status_for_user(userid)


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
