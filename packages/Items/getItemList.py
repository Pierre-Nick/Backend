###################################################################
#####   `   Get items for user for KitchenWizard              #####
###################################################################
##### Version: 0.3                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  02/--/2016                                     #####
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
            print("[%s]addItem --> %s" % (ti, message))
