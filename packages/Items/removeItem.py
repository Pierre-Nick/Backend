###################################################################
#####   `   Remove item for KitchenWizard                     #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  02/--/2016                                     #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to remove   #####
#####          a item for a user to the inventory             #####
###################################################################

from datetime import *
import MySQLdb
from addItem import __get_userid_from_key

debug_on = True
log_level = 3

def log(message, lev):
    # Log messages
    # Return void
    if debug_on:
        if lev <= log_level:
            ti = str(datetime.now())
            print("[%s]addItem --> %s" % (ti, message))


def __item_in_inventory(item_id, userid):
    log("Checking if item is in inventory", 2)
    sql = "SELECT * FROM Inventory WHERE UserID = '%s' AND InventoryID = '%s';" % (str(userid), str(item_id))
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchone()
    db.close()
    log("DB closed", 3)

    if data:
        return True
    else:
        return False

def __remove_item_from_db(item_id):
    log("Request to remove item from db", 2)
    sql = "DELETE FROM Inventory WHERE InventoryID = '%s';" % (item_id)
    print sql
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
        log("Error adding to DB", 1)
        return False


def remove_item(item_id, session_key):
    userid = __get_userid_from_key(session_key)
    item_id = int(item_id)
    if not __item_in_inventory(item_id, userid):
        log("Item not in inventory", 1)
        return False
    else:
        if __remove_item_from_db(item_id):
            log("Item removed from DB", 1)
            return True
        else:
            log("Item failed to be removed", 1)
            return False
