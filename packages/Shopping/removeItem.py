from packages.Log import kwlog
from packages.Items.addItem import __get_userid_from_key
from packages.Database import MySQL


def remove_item_from_list(rid, gid, session):
    userid =  __get_userid_from_key(session)

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    else:
        if not MySQL.is_vaild_group(gid):
            return "INVAILD_GROUP"
        if not MySQL.is_vaild_shopping_list(rid, userid):
            kwlog.log("List not owned by user")
            return "INVAILD_SHOPPING_LIST"
        else:
            if not MySQL.remove_item_from_shopping_list(gid, rid):
                return "UNABLE_TO_REMOVE_ITEM"
            else:
                return "REMOVE_ITEM_COMPLETE"

def remove_all_items_from_list(rid, session):
    userid =  __get_userid_from_key(session)

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    else:
        if not MySQL.is_vaild_shopping_list(rid, userid):
            kwlog.log("List not owned by user")
            return "INVAILD_SHOPPING_LIST"
        else:
            if not MySQL.remove_all_items_from_shopping_list(rid):
                kwlog.log("Unable to remove items from list")
                return "UNABLE_TO_REMOVE_ITEMS"
            else:
                kwlog.log("Remove items complete")
                return "REMOVE_ITEMS_COMPLETE"
