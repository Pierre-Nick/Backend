###################################################################
#####   `   Remove recipe for KitchenWizard                     #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Robert M                                       #####
##### Tested:  Not even once                                  #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to remove   #####
#####          a recipe for a user to the inventory           #####
###################################################################

from datetime import *
from packages.Items.addItem import __get_userid_from_key
from packages.Log import kwlog
from packages.Database import MySQL


def __recipe_in_inventory(recipe_id, userid):
    if MySQL.is_recipe_in_db(recipe_id, userid):
        return True
    else:
        return False

def __remove_recipe_from_db(recipe_id):
    return MySQL.remove_recipe_from_db(recipe_id)

def remove_recipe(recipe_id, session_key):
    userid = __get_userid_from_key(session_key)
    recipe_id = int(recipe_id)
    if not __recipe_in_inventory(recipe_id, userid):
        kwlog.log("Recipe not in inventory")
        return False
    else:
        if __remove_recipe_from_db(recipe_id):
            kwlog.log("recipe removed from DB")
            return True
        else:
            kwlog.log("recipe failed to be removed")
            return False
