###################################################################
#####   `   Add item for KitchenWizard                        #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  02/12/2016                                     #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to add a    #####
#####          new item for a user to the inventory           #####
###################################################################

from datetime import datetime

def log(message, lev):
    # Log messages
    # Return void
    if debug_on:
        if lev <= log_level:
            ti = str(datetime.now())
            print("[%s]addItem --> %s" % (ti, message))

def __vaildate_sessionkey(key):
    # Check if session key is vaild
    # Return bool


def __get_userid_from_key(key):
    # Gets userid from session key
    # Return str


def __get_product_details(barcode):
    # Get details of product
    # Return list

def __add_item_to_inventory(item):
    # Add item to inventory
    # Return bool

def add_new_item(barcode, session):
    # Add new item to inventory of user
    # Return bool
    log("Adding new item", 1)
    userid=__get_userid_from_key(session)
    if userid == 'BAD_KEY':
        log("Add item failed", 1)
        return False
    else:
        item =  __get_product_details(barcode)
        if item:
            if __add_item_to_inventory(item):
                log("New item added", 1)
                return True
            else:
                log("Add item failed", 1)
                return False
        else:
            ("Add item failed", 1)
            return False
