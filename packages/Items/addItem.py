###################################################################
#####   `   Add item for KitchenWizard                        #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  02/26/2016                                     #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to add a    #####
#####          new item for a user to the inventory           #####
###################################################################

from datetime import *
from urllib2 import urlopen
import json
import MySQLdb

debug_on = True
log_level = 3

def log(message, lev):
    # Log messages
    # Return void
    if debug_on:
        if lev <= log_level:
            ti = str(datetime.now())
            print("[%s]addItem --> %s" % (ti, message))


def __get_session_key_expire_data(key):
    # Get expiration date for key
    # Return str
    sql = "SELECT AgeOffDate FROM Session_Key WHERE SessionKey = '%s'" % (str(key))
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchone()
    db.close()
    log("DB closed", 3)
    return str(data[0])

def __check_vaild_date(key):
    # Checks if key vaild date has passed
    # return bool
    d = str(__get_session_key_expire_data(key))
    d1 = datetime.strptime(d, "%Y-%m-%d %H:%M:%S")
    d2 = datetime.now()
    return d1 > d2

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
    sql = "SELECT * FROM ProductInformation WHERE ProductID = '%s';" % (barcode)
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


def __group_in_db(name):
    # Checks if group is contained in DB
    # Return bool
    sql = "SELECT * FROM Grouping WHERE GroupName = '%s'" % (name)
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


def __add_group_to_db(name):
    # Adds group to DB
    # Return bool
    log("Add group to DB request", 2)
    sql = "INSERT INTO `KitchenWizard`.`Grouping` (`GroupName`, `DateAdded`) VALUES ('%s', '%s');" % (str(name), str(datetime.now()))
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


def __get_group_id(name):
    # Get group ID
    # Return str
    if not __group_in_db(name):
        __add_group_to_db(name)

    # Get ID
    sql = "SELECT GroupID FROM Grouping WHERE GroupName = '%s'" % (name)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchone()
    db.close()
    log("DB closed", 3)
    return str(data[0])


def __get_product_details_from_api(barcode):
    # Get details of product
    # Return list
    url = "http://api.foodessentials.com/labelarray?u=%s&sid=9fe4492b-492e-4336-86b8-7d278e02aa51&n=2&s=0&f=json&api_key=mvdrrzwt9327ttazxse6f95b" % (str(barcode))
    response = urlopen(url)
    j_obj = json.load(response)
    item = []
    for i in j_obj['productsArray']:
        item.append(str(barcode))
        item.append(str(i['product_name']))
        item.append(str(i['product_description']))
        item.append(str(i['manufacturer']))
        item.append(str(i['product_size']))
        item.append(str(__get_group_id(str(i['shelf']))))
    return item

def __add_product_to_DB(item):
    # Add product details from API to Database
    # Return bool
    #{0: Barcode, 1: Name, 2:details, 3:Maker, 4:size, 5:group}
    log("Add product request", 2)
    sql = "INSERT INTO `KitchenWizard`.`ProductInformation` (`ProductID`, `ProductName`, `ProductDiscription`, `Manufacturer`, `Quantity`, `GroupID`) VALUES ('%s', '%s', '%s', '%s', '%s', '%s');" % (str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]))
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    try:
        log("Inside try", 3)
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


def __add_item_to_inventory(barcode, userid):
    # Add item to inventory
    # Return bool
    if not __product_is_in_DB(barcode):
        item = __get_product_details_from_api(barcode)
        if not __add_product_to_DB(item):
            return False

    # Add item to inventory
    log("Add to inventory request", 2)
    sql = "INSERT INTO `KitchenWizard`.`Inventory` (`UserID`, `ProductID`, `DateAdded`) VALUES ('%s', '%s', '%s');" % (str(userid), str(barcode), str(datetime.now()))
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


def __get_inventory_id(barcode, userid):
    # Get id for latest item added with particular barcode by user
    # Return str
    sql = "SELECT InventoryID FROM Inventory WHERE ProductID = '%s' AND UserID = '%s';" % (str(barcode), str(userid))
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchall()
    db.close()
    log("DB closed", 3)
    return str(data[(len(data)-1)])

def add_new_item(barcode, session):
    # Add new item to inventory of user
    # Return str
    log("Adding new item", 1)
    userid=__get_userid_from_key(session)
    if userid == 'BAD_KEY':
        log("Add item failed", 1)
        return "ADD_FAILED"
    else:
        if __add_item_to_inventory(barcode, userid):
            log("New item added", 1)
            return __get_inventory_id(barcode, userid)
        else:
            log("Add item failed", 1)
            return "ADD_FAILED"
