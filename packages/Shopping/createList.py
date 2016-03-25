from packages.Log import kwlog
from packages.Items.addItem import __get_userid_from_key
from packages.Database import MySQL

create_new_list(name, sessionkey):
    if len(sessionkey) > 0:
        userid =  __get_userid_from_key(session_key)
    else:
        return "INVAILD_FORMAT"

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    else:
        if not len(name) > 0:
            return "INVAILD_FORMAT"
        if MySQL.create_new_shopping_list(name, userid):
            return "LIST_CREATED"
        else:
            return "FAILED_TO_CREATE_LIST"
