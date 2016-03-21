from packages.Log import kwlog
from packages.Items.addItem import __get_userid_from_key
from packages.Database import MySQL


def update_recipe(name, dis, image, prepT, cookT, items, itemAction, sessionkey):
    userid =  __get_userid_from_key(session_key)

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    else:
        if len(itemAction) == 0 and len(item) > 0:
            return "INVAILD_FORMAT"
        elif not (itemAction == "ADD" or itemAction == "REMOVE" or itemAction == "UPDATE"):
            return "INVAILD_FORMAT"
        else:
            if len(name) > 0:
                print("Stuff")
            if len(dis) > 0:
                print("Stuff")
            if len(image) > 0:
                print("Stuff")
            if len(prepT) > 0:
                print("Stuff")
            if len(cookT) > 0:
                print("stuff")
            if len(items) > 0:
                print("stuff")
