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


def create_json_format(shoping_list):
    string = "<Shopping>"
    for s in shoping_list:
        string = string + "<List><ID>" + str(s[0]) + "</ID>"
        string = string + "<Name>" + str(s[1]) + "</Name>"
        sting = string + "<Items>"
        for k in s[2]:
            string = string + "<Name>" + str(k[0]) + "</Name>"
            string = string + "<Amount>" + str(s[1]) + "</Amount>"

        string = string + "</Items>"
        string = string + "<UserID>" + str(s[3]) + "</UserID>"
        string = string + "<Date>" + str(s[4]) + "</Date></List>"
    string = string + "</Shopping>"
    #string = string + shoping_list[]
    return str(string)

def get_shopping_lists(session_key):
    userid =  __get_userid_from_key(session_key)

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    else:
        return create_json_format(__create_shopping_list(userid))
