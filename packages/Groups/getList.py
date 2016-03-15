###################################################################
#####   `   Add item for KitchenWizard                        #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  --                                             #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to get a    #####
#####          list of generic items                          #####
###################################################################

from packages.Log import kwlog
from packages.Database import MySQL


def get_list_of_generic_items():
    # Get list of generic Items
    # Return: str
    return MySQL.get_groups()
