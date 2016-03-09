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
from urllib.request import urlopen
import json
import pymysql as MySQLdb
from packages.Log import kwlog


def __get_session_key_expire_data(key):
    # Get expiration date for key
    # Return str
    sql = "SELECT AgeOffDate FROM Session_Key WHERE SessionKey = '%s'" % (str(key))
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchone()
    db.close()
    kwlog.log("DB closed")
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
    else:
        kwlog.log("Hey has expired")
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
        sql = "SELECT UserID FROM Session_Key WHERE SessionKey = '%s';" % (key)
        db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
        kwlog.log("Connected to DB")
        cursor = db.cursor()
        cursor.execute(sql)
        kwlog.log("SQL excuted correctly")
        data = cursor.fetchone()
        db.close()
        kwlog.log("DB closed")
        return str(data[0])
    else:
        return "BAD_KEY"


def __product_is_in_DB(barcode):
    # Check if the product is in the DB
    # Return bool
    sql = "SELECT * FROM ProductInformation WHERE ProductID = '%s';" % (barcode)
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


def __group_in_db(name):
    # Checks if group is contained in DB
    # Return bool
    sql = "SELECT * FROM Grouping WHERE GroupName = '%s'" % (name)
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


def __add_group_to_db(name):
    # Adds group to DB
    # Return bool
    kwlog.log("Add group to DB request")
    sql = "INSERT INTO `KitchenWizard`.`Grouping` (`GroupName`, `DateAdded`) VALUES ('%s', '%s');" % (str(name), str(datetime.now()))
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


def __get_group_id(name):
    # Get group ID
    # Return str
    if not __group_in_db(name):
        __add_group_to_db(name)

    # Get ID
    sql = "SELECT GroupID FROM Grouping WHERE GroupName = '%s'" % (name)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchone()
    db.close()
    kwlog.log("DB closed")
    return str(data[0])


def __get_product_details_from_api(barcode):
    # Get details of product
    # Return list
    url = "http://api.foodessentials.com/labelarray?u=%s&sid=9fe4492b-492e-4336-86b8-7d278e02aa51&n=2&s=0&f=json&api_key=mvdrrzwt9327ttazxse6f95b" % (str(barcode))
    response = urlopen(url).read()
    if len(response) > 0:
        j_obj = json.loads(response.decode("utf-8"))
        print(j_obj['productsArray'])
        item = []
        for i in j_obj['productsArray']:
            item.append(str(barcode))
            item.append(str(i['product_name']))
            item.append(str(i['product_description']))
            item.append(str(i['manufacturer']))
            item.append(str(i['product_size']))
            item.append(str(__get_group_id(str(i['shelf']))))
        return item
    else:
        return "No_Information"


def __clean_item_return_from_api(item):
    k = []
    for i in item:
        print(i)
        if "'" in str(i):
            i = i[:i.index("'")] + "'" + i[i.index("'"):]
        k.append(i)
    print(k)
    return k

def __add_product_to_DB(item):
    # Add product details from API to Database
    # Return bool
    #{0: Barcode, 1: Name, 2:details, 3:Maker, 4:size, 5:group}
    kwlog.log("Add product request")
    item = __clean_item_return_from_api(item)
    sql = "INSERT INTO `KitchenWizard`.`ProductInformation` (`ProductID`, `ProductName`, `ProductDiscription`, `Manufacturer`, `Quantity`, `GroupID`) VALUES (%s, %s, '%s', '%s', '%s', '%s');" % (str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5]))
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    try:
        kwlog.log("Inside try")
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


def __add_item_to_inventory(barcode, userid):
    # Add item to inventory
    # Return bool
    if not __product_is_in_DB(barcode):
        item = __get_product_details_from_api(barcode)
        if item == "No_Information":
            kwlog.log("API does not contain product")
            return "No_Information_Available"
        if not __add_product_to_DB(item):
            return False

    # Add item to inventory
    kwlog.log("Add to inventory request")
    sql = "INSERT INTO `KitchenWizard`.`Inventory` (`UserID`, `ProductID`, `DateAdded`) VALUES ('%s', '%s', '%s');" % (str(userid), str(barcode), str(datetime.now()))
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


def __clean_barcode(barcode):
    # Clean '+' out of some barcode
    # Return: str
    kwlog.log("Clean barcode")
    if '+' in barcode:
        return barcode.strip('+')
    else:
        return barcode


def add_new_item(barcode, session):
    # Add new item to inventory of user
    # Return str
    kwlog.log("Adding new item")
    userid=__get_userid_from_key(session)
    barcode = __clean_barcode(barcode)
    if userid == 'BAD_KEY':
        kwlog.log("Add item failed")
        return "ADD_FAILED"
    else:
        ret = __add_item_to_inventory(barcode, userid)
        if ret:
            if ret == "No_Information_Available":
                return "ADD_FAILED_PRODUCT_NOT_IN_API"
            kwlog.log("New item added")
            return "ITEM_ADDED"
        else:
            kwlog.log("Add item failed")
            return "ADD_FAILED"
