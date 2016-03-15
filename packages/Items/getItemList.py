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
from packages.Items.addItem import __get_userid_from_key
from packages.Log import kwlog
from packages.Database import MySQL


def __get_product_information(Product):
    # Get the product information
    # return list
    return MySQL.get_product_by_barcode(Product)


#def __get_group_image(group_id):
    # Get the image of a product for a group
    # return str
#    return MySQL.get_group_image_by_id(group_id)


def __get_items_for_user(userid):
    # Get items for a userid
    # Return list
    return MySQL.get_inventory_list_for_user(userid)

def __get_group_name(gid):
    return MySQL.get_group_name_from_group_id(gid)

def __create_response_list(items):
    # Create and return the list of products
    # Return list
    final = []
    kwlog.log("Create list of products, for UI")

    for i in items:
        temp = __get_product_information(str(i[1]))
        if __get_group_name(str(temp[5])):
            k = [i[0], temp[0], temp[1], temp[2], temp[3], temp[4], str(__get_group_name(str(temp[5]))[0]), temp[6], temp[7], temp[8]]
        else:
            k = [i[0], temp[0], temp[1], temp[2], temp[3], temp[4], "NONE", temp[6], temp[7], temp[8]]
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
