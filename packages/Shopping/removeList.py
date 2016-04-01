from packages.Log import kwlog
from packages.Items.addItem import __get_userid_from_key
from packages.Database import MySQL
from packages.Shopping import removeItem

def remove_shopping_list(sid, session):
    if removeItem.remove_all_items_from_list(sid, session) == "REMOVE_ITEMS_COMPLETE":
        userid =  __get_userid_from_key(session_key)
        if userid == 'BAD_KEY':
            kwlog.log("Invaild session key")
            return "BAD_KEY"
        else:
            if len(sid) == 0:
                kwlog.log("Format of request is invaild")
                return "INVAILD_FORMAT"
            if not MySQL.is_vaild_shopping_list(sid, userid):
                kwlog.log("Invaild shopping list id")
                return "INVAILD_SHOPPING_LIST"
        if MySQL.remove_shopping_list(sid):
            return True
        else:
            return False
    else:
        return False
