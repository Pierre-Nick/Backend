###################################################################
#####   `   Get items for user for KitchenWizard              #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  02/27/2016                                     #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to get a    #####
#####          list of item for a user                        #####
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
            print("[%s]getItemList --> %s" % (ti, message))


def __get_product_information(Product):
    # Get the product information
    # return list
    log("Get product information", 2)
    sql = "SELECT * FROM ProductInformation WHERE ProductID = '%s';" % (str(Product))
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchone()
    db.close()
    log("DB closed", 3)
    return data


def __get_group_image(group_id):
    # Get the image of a product for a group
    # return str
    log("Get url for group image", 2)
    sql = "SELECT GroupImage FROM Grouping WHERE GroupID = '%s';" % (group_id)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchone()
    db.close()
    log("DB closed", 3)
    return str(data[0])


def __get_items_for_user(userid):
    # Get items for a userid
    # Return list
    log("Get items for user from DB", 2)
    sql = "SELECT ProductID FROM Inventory WHERE UserID = '%s';" % (userid)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    log("Connected to DB", 3)
    cursor = db.cursor()
    cursor.execute(sql)
    log("SQL excuted correctly", 3)
    data = cursor.fetchall()
    db.close()
    log("DB closed", 3)
    return data


def __create_response_list(items):
    # Create and return the list of products
    # Return list
    temp = []
    final = []
    log("Create list of products, for UI", 2)

    for i in items:
        temp.append(__get_product_information(str(i[0])))

    for j in temp:
        k=[j[0], j[1], j[2], j[3], j[4], __get_group_image(str(j[5]))]
        final.append(k)

    return final


def get_item_list(session_key):
    # Get items for a userid
    # Return list
    log("Get items for a user", 1)
    userid = __get_userid_from_key(session_key)
    user_list = __get_items_for_user(userid)
    return __create_response_list(user_list)
