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
import pymysql as MySQLdb
from packages.Items.addItem import __get_userid_from_key
from packages.Log import kwlog


def __get_product_information(Product):
    # Get the product information
    # return list
    kwlog.log("Get product information")
    sql = "SELECT * FROM ProductInformation WHERE ProductID = '%s';" % (str(Product))
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchone()
    db.close()
    kwlog.log("DB closed")
    return data


def __get_group_image(group_id):
    # Get the image of a product for a group
    # return str
    kwlog.log("Get url for group image")
    sql = "SELECT GroupImage FROM Grouping WHERE GroupID = '%s';" % (group_id)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchone()
    db.close()
    kwlog.log("DB closed")
    return str(data[0])


def __get_items_for_user(userid):
    # Get items for a userid
    # Return list
    kwlog.log("Get items for user from DB")
    sql = "SELECT InventoryID, ProductID FROM Inventory WHERE UserID = '%s';" % (userid)
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    kwlog.log("Connected to DB")
    cursor = db.cursor()
    cursor.execute(sql)
    kwlog.log("SQL excuted correctly")
    data = cursor.fetchall()
    db.close()
    kwlog.log("DB closed")
    return data


def __create_response_list(items):
    # Create and return the list of products
    # Return list
    final = []
    kwlog.log("Create list of products, for UI")

    for i in items:
        temp = __get_product_information(str(i[0]))
        k=[i[0], temp[1], temp[2], temp[3], temp[4], __get_group_image(str(temp[5]))]
        final.append(k)

    return final


def get_item_list(session_key):
    # Get items for a userid
    # Return list
    kwlog.log("Get items for a user")
    userid = __get_userid_from_key(session_key)
    if userid == 'BAD_KEY':
        kwlog.log("Bad Session Key")
        return "BAD_KEY"
    else:
        user_list = __get_items_for_user(userid)
        return __create_response_list(user_list)
