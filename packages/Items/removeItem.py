###################################################################
#####   `   Remove item for KitchenWizard                     #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  02/26/2016                                     #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to remove   #####
#####          a item for a user to the inventory             #####
###################################################################

from datetime import *
from packages.Items.addItem import __get_userid_from_key
from packages.Log import kwlog
from packages.Database import MySQL


def __item_in_inventory(item_id, userid):
    if MySQL.is_item_in_inventory(item_id, userid):
        return True
    else:
        return False

def __remove_item_from_db(item_id):
    return MySQL.remove_item_from_inventory(item_id)

def remove_item(item_id, session_key):
    userid = __get_userid_from_key(session_key)
    item_id = int(item_id)
    if not __item_in_inventory(item_id, userid):
        kwlog.log("Item not in inventory")
        return False
    else:
        if __remove_item_from_db(item_id):
            kwlog.log("Item removed from DB")
            return True
        else:
            kwlog.log("Item failed to be removed")
            return False
