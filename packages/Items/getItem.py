###################################################################
#####   `         Get item for KitchenWizard                  #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  --                                             #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to get a    #####
#####          item from the inventory for a user             #####
###################################################################

import MySQLdb
from packages.Log import kwlog
from addItem import __get_userid_from_key


def __check_item_owner(uid, user):
    


def __get_item_for_uid(uid):


def __create_response_list(uid, userid):


def getItem(uid, SessionKey):
    userid = __get_userid_from_key(SessionKey)
    if userid == 'BAD_KEY':
        kwlog.log("Bad Session Key")
        return "BAD_KEY"
    else:
        return __create_response_list(uid, userid)
