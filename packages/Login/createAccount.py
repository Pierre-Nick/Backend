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
def check_if_email_exist():
    return False


def add_new_user(username, fname, lname, email, hash):
    if(user_exist("mr7657") == "NO_ID_FOUND"):
        # no id found, check email
        #   -> if email exist, account already exist for this email
        #   -> if no email, create account
        if check_if_email_exist():
            return "ACCOUNT_ALREADY_EXIST_FOR_EMAIL"
        else:
            create_account(username, fname, lname, email, hash)
    elif(user_exist("mr7657") == "ID_FOUND"):
        # check if email already exist
        #   -> if so account already exist, reset pass
        #   -> if no email, username already taken
    else:
        # bad username choice
        #   -> maybe someone trying sql injection