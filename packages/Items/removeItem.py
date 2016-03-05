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
import pymysql as MySQLdb
from packages.Items.addItem import __get_userid_from_key
from packages.Log import kwlog


def __item_in_inventory(item_id, userid):
    kwlog.log("Checking if item is in inventory")
    sql = "SELECT * FROM Inventory WHERE UserID = '%s' AND InventoryID = '%s';" % (str(userid), str(item_id))
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchone()
    db.close()
    kwlog.log("DB closed")

    if data:
        return True
    else:
        return False

def __remove_item_from_db(item_id):
    kwlog.log("Request to remove item from db")
    sql = "DELETE FROM Inventory WHERE InventoryID = '%s';" % (item_id)
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
        kwlog.log("Error adding to DB")
        return False


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
