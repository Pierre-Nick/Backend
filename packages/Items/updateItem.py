
from packages.Log import kwlog
from packages.Database import MySQL
from packages.Items.addItem import __get_userid_from_key

def update_inventory_item(info, uid, session_key):
    # Update inventory information for user
    # Return: string
    # info[] = [ExperationDate, PercentUsed]
    userid = __get_userid_from_key(session_key)
    if userid == 'BAD_KEY':
        kwlog.log("Bad Session Key")
        return "BAD_KEY"
    else:
        if MySQL.is_item_owned_by_user(userid, uid):
            return MySQL.update_inventory_item(uid, info)
        else:
            "INVAILD_INVENTORY_ID"
