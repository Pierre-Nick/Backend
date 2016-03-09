###################################################################
#####   `             MySQL Manger Script                     #####
###################################################################
##### Version: 0.5                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  --                                             #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to perform  #####
#####          the SQL queries to the database in one         #####
#####          location, this will help cut down on           #####
#####          duplications of mods                           #####
###################################################################

import pymysql as MySQLdb
from datetime import *

global db
global cursor

def init():
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    cursor = db.cursor()
    kwlog.log("Connected to DB")


def close():
    db.close()
    kwlog.log("DB connection closed")


def get_generic_item_list():
    sql = "SELECT GroupName FROM Grouping"
    cursor.execute(sql)
    return cursor.fetchall()


def get_session_key_expire_data(key):
    kwlog.log("Get exp date for key")
    sql = "SELECT AgeOffDate FROM Session_Key WHERE SessionKey = '%s'" % (str(key))
    cursor.execute(sql)
    data = cursor.fetchone()
    return str(data[0])

def get_userid_from_session_key(key):
    kwlog.log("Get userid from session key")
    sql = "SELECT UserID FROM Session_Key WHERE SessionKey = '%s';" % (key)
    cursor.execute(sql)
    data = cursor.fetchone()
    return str(data[0])


def get_product_by_barcode(barcode):
    kwlog.log("Get product by barcode")
    sql = "SELECT * FROM ProductInformation WHERE ProductID = '%s';" % (barcode)
    cursor.execute(sql)
    return cursor.fetchone()


def get_group_by_name(name):
    kwlog.log("Get category by name")
    sql = "SELECT * FROM Grouping WHERE GroupName = '%s'" % (name)
    cursor.execute(sql)
    return cursor.fetchone()


def put_group(name):
    kwlog.log("Put group")
    sql = "INSERT INTO `KitchenWizard`.`Grouping` (`GroupName`, `DateAdded`) VALUES (%s, %s);"
    try:
        cursor.execute(sql, (str(name), str(datetime.now())))
        db.commit()
        return True
    except:
        db.rollback()
        kwlog.log("Error adding new group")
        return False


def put_new_product(item):
    kwlog.log("Put new product")
    sql = "INSERT INTO `KitchenWizard`.`ProductInformation` (`ProductID`, `ProductName`, `ProductDiscription`, `Manufacturer`, `Quantity`, `GroupID`) VALUES (%s, %s, %s, %s, %s, %s);"
    try:
        cursor.execute(sql,(str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(item[5])))
        db.commit()
        return True
    except:
        db.rollback()
        kwlog.log("Error adding new product")
        return False


def put_item_in_inventory(barcode, userid):
    kwlog.log("Put item in inventory")
    sql = "INSERT INTO `KitchenWizard`.`Inventory` (`UserID`, `ProductID`, `DateAdded`) VALUES (%s, %s, %s);"
    try:
        cursor.execute(sql, (str(userid), str(barcode), str(datetime.now())))
        db.commit()
        return True
    except:
        db.rollback()
        kwlog.log("Error adding item to inventory")
        return False
