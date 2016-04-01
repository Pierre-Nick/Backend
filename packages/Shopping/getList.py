from packages.Log import kwlog
from packages.Items.addItem import __get_userid_from_key
from packages.Database import MySQL

def __get_list(sid):
    final = []
    slist = MySQL.get_list_of_shopping_items(sid)
    for s in slist:
        k = [MySQL.get_group_name_from_group_id(s[2]), s[3]]
        final.append(list(k))
    return list(final)


def __create_shopping_list(userid):
    final = []
    slist = MySQL.get_shopping_lists(userid)
    for s in slist:
        k = [s[0], s[1], __get_list(s[0]), s[2], str(s[3])]
        final.append(list(k))
    return list(final)

def get_shopping_lists(session_key):
    userid =  __get_userid_from_key(session_key)

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    else:
        return __create_shopping_list(userid)
