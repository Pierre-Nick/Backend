
from packages.Log import kwlog
from packages.Database import MySQL
from datetime import *

def __check_vaild_date(key):
    # Checks if key vaild date has passed
    # return bool
    d = str(MySQL.get_session_key_expire_data(key))
    d1 = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.now()
    return d1 > d2

def __session_key_exist(key):
    # Checks Session Key exist
    # Return bool
    if __check_vaild_date(key):
        if MySQL.get_userid_from_session_key(key):
            return True
        else:
            return False
    else:
        kwlog.log("Key has expired")
        return False


def __vaildate_sessionkey(key):
    # Check if session key is vaild
    # Return bool
    if __session_key_exist(key):
        if __check_vaild_date(key):
            kwlog.log("Key is vaild")
            return True
        else:
            kwlog.log("Invaild key")
            return False
    else:
        kwlog.log("Invaild key")
        return False


def __get_userid_from_key(key):
    # Gets userid from session key
    # Return str
    kwlog.log("Get userid from key")
    if(__vaildate_sessionkey(key)):
        return MySQL.get_userid_from_session_key(key)
    else:
        return "BAD_KEY"



def update_inventory_item(info, uid, session_key):
    # Update inventory information for user
    # Return: string
    # info[] = [ExperationDate, PercentUsed]
    userid = __get_userid_from_key(session_key)
    if userid == 'BAD_KEY':
        kwlog.log("Bad Session Key")
        return "BAD_KEY"
    else:
        if MySQL.is_item_owned_by_user(userid, uid):
            return MySQL.update_inventory_item(uid, info)
        else:
            "INVAILD_INVENTORY_ID"


def update_group_of_item(groupid, barcode, session_key):
    userid = __get_userid_from_key(session_key)
    if userid == 'BAD_KEY':
        kwlog.log("Bad Session Key")
        return "BAD_KEY"
    else:
        if not MySQL.get_group_by_barcode(barcode):
            kwlog.log("Group Already Assigned")
            return "GROUP_ALREADY_ASSIGNED"
        else:
            kwlog.log("Updating group for product")
            return MySQL.update_group_of_item(groupid, barcode)
