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
            print("[%s]checkLogin --> %s" % (ti, message))


def check_if_email_exist():
    return False


def create_account(username, fname, lname, email, hash):
# Create account and add to DB
# Return bool


def add_confirmation_to_db():
# Adds confirmation code to DB
# Return bool


def generate_confirmation_code(username):
# Generate confirmation code
# Return str


def send_confirmation_email(fname, email, code):
# Sends confirmation email
# Return bool


def create_confirmation_email(fname, email, username):
# Generates confirmation email, once account was created
# Return bool


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
