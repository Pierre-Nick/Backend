###################################################################
#####   `         Add Recipe for KitchenWizard                #####
###################################################################
##### Version: 0.5                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  ---                                            #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to add a    #####
#####          new recipe for a user                          #####
###################################################################

from packages.Log import kwlog
from packages.Items.addItem import __get_userid_from_key
from packages.Database import MySQL

def create_recipe(recipe, userid):



def add_recipe(session_key, recipe):
    # Adds a recipe for a user
    # Return string
    # recipe[] = [0:Name, 1:Discription, 2:directions, 3:[items], 4:image, 5:Prep Time, 6:Cook Time]
    # items[] = [gen_id, size]
    userid =  __get_userid_from_key(session_key)

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    else:
        if (len(recipe[0]) > 0) and (len(recipe[1]) > 0) and (len(recipe[2]) > 0) and (len(recipe[3]) > 0) and (len(recipe[4]) > 0) and (len(recipe[5]) > 0) and (len(recipe[6]) > 0):

        else:
            return "BAD_ARGUMENTS"
