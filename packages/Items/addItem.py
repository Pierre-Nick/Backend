###################################################################
#####   `   Add item for KitchenWizard                        #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  02/--/2016                                     #####
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


def __check_vaild_date(key):
    # Checks if key vaild date has passed
    # return bool
    return True

def __session_key_exist(key):
    # Checks Session Key exist
    # Return bool
    if __check_vaild_date(key):
        sql = "SELECT UserID FROM Session_Key WHERE SessionKey = '%s';" % (key)
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
    else:
        log("Hey has expired", 2)
        return False


def __vaildate_sessionkey(key):
    # Check if session key is vaild
    # Return bool
    if __session_key_exist(key):
        if __check_vaild_date(key):
            log("Key is vaild", 2)
            return True
        else:
            log("Invaild key", 2)
            return False
    else:
        log("Invaild key", 2)
        return False


def __get_userid_from_key(key):
    # Gets userid from session key
    # Return str
    log("Get userid from key", 2)
    if(__vaildate_sessionkey(key)):
        sql = "SELECT UserID FROM Session_Key WHERE SessionKey = '%s';" % (key)
        db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
        log("Connected to DB", 3)
        cursor = db.cursor()
        cursor.execute(sql)
        log("SQL excuted correctly", 3)
        data = cursor.fetchone()
        db.close()
        log("DB closed", 3)
        return str(data[0])
    else:
        return "BAD_KEY"


def __product_is_in_DB(barcode):
    # Check if the product is in the DB
    # Return bool
    sql = "SELECT * FROM ProductInformation WHERE ProductID = '%s';" % (key)
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


def __get_product_details_from_api(barcode):
    # Get details of product
    # Return list
    item = {}



def __add_product_to_DB(item):
    # Add product details from API to Database
    # Return bool
    #{0: Name, 1:details, 2:Maker, 3:size, 4:group}


def __add_item_to_inventory(barcode, userid):
    # Add item to inventory
    # Return bool
    if not __product_is_in_DB(barcode):
        item = __get_product_details_from_api(barcode)
        if not __add_product_to_DB(item):
            return False

    # Add item to inventory


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
