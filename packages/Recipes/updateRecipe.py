from packages.Log import kwlog
from packages.Items.addItem import __get_userid_from_key
from packages.Database import MySQL

def update_recipe(rec_id, name, dis, image, prepT, cookT, items, itemAction, sessionkey):
    print("rec: %s\nname: %s\ndis: %s\nimage:%s\nprep:%s\ncook:%s\nitems:%s\naction:%s\nkey:%s" % (str(rec_id), str(name), str(dis), str(image), str(prepT), str(cookT), str(items), str(itemAction), str(sessionkey)))
    userid =  __get_userid_from_key(sessionkey)

    if userid == 'BAD_KEY':
        kwlog.log("Invaild session key")
        return "BAD_KEY"
    else:
        if len(itemAction) == 0 and len(items) > 0:
            return "INVAILD_FORMAT"
        elif not (itemAction == "ADD" or itemAction == "REMOVE" or itemAction == "UPDATE" or itemAction == ""):
            return "INVAILD_FORMAT"
        else:
            if MySQL.owned_by_user(userid, rec_id):
                if len(name) > 0:
                    if not MySQL.update_recipe_name(name, rec_id):
                        kwlog.log("Update recipe name failed")
                        return "UPDATE_FAILED"
                if len(dis) > 0:
                    if not MySQL.update_recipe_dis(dis, rec_id):
                        kwlog.log("Update recipe name failed")
                        return "UPDATE_FAILED"
                if len(image) > 0:
                    if not MySQL.update_recipe_image(image, rec_id):
                        kwlog.log("Update recipe name failed")
                        return "UPDATE_FAILED"
                if len(prepT) > 0:
                    if not MySQL.update_recipe_prep(prepT, rec_id):
                        kwlog.log("Update recipe name failed")
                        return "UPDATE_FAILED"
                if len(cookT) > 0:
                    if not MySQL.update_recipe_cook(cookT, rec_id):
                        kwlog.log("Update recipe name failed")
                        return "UPDATE_FAILED"
                if len(itemAction) > 0:
                    if itemAction == "ADD":
                        if not MySQL.update_recipe_add_item(items, rec_id):
                            kwlog.log("Add item to recipe failed")
                            return "UPDATE_FAILED"
                    elif itemAction == "REMOVE":
                        if not MySQL.update_recipe_remove_item(items, rec_id):
                            kwlog.log("Update recipe name failed")
                            return "UPDATE_FAILED"
                    else:
                        if not MySQL.update_recipe_update_item(items, rec_id):
                            kwlog.log("Update recipe name failed")
                            return "UPDATE_FAILED"
                return "UPDATE_COMPLETE"
            else:
                return "BAD_REC_ID"
