from packages.Log import kwlog
from packages.Items.addItem import __get_userid_from_key
from packages.Database import MySQL
from packages.Shopping import createList

def add_item_to_list(gid, measurment, sid, session):
    userid =  __get_userid_from_key(session)

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    else:
        if len(gid) == 0 or len(measurment) == 0 or len(sid) == 0:
            kwlog.log("Format of request is invaild")
            return "INVAILD_FORMAT"
        if not MySQL.is_vaild_group(gid):
            kwlog.log("Group ID is not vaild")
            return "INVAILD_GROUP"
        if not MySQL.is_vaild_shopping_list(sid, userid):
            kwlog.log("Invaild shopping list id")
            name = "%s list" % str(userid)
            createList.create_new_list(name, session)
            sid = MySQL.get_shopping_lists(userid)[0][0]
            if not MySQL.insert_item_to_list(sid, gid, measurment, userid):
                kwlog.log("Unable to add item to list")
                return "FAILED_TO_ADD_ITEM"
            else:
                return "ADD_ITEM_COMPLETE"
            return "INVAILD_SHOPPING_LIST"
        if not MySQL.insert_item_to_list(sid, gid, measurment, userid):
            kwlog.log("Unable to add item to list")
            return "FAILED_TO_ADD_ITEM"
        else:
            return "ADD_ITEM_COMPLETE"
