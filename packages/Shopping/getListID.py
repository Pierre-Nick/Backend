from packages.Items.addItem import __get_userid_from_key
from packages.Database import MySQL

def get_list_ID(session_key):
    userid =  __get_userid_from_key(session_key)

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    else:
        sid = MySQL.get_shopping_list_id_for_user(userid)
        if sid == "NONE":
            name = "%s list" % str(userid)
            createList.create_new_list(name, session_key)
            sid = MySQL.get_shopping_lists(userid)[0][0]
        print(sid)
        return str(sid)
