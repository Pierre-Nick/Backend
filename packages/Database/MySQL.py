###################################################################
#####   `             MySQL Manger Script                     #####
###################################################################
##### Version: 0.5                                            #####
##### Author:  Marcus R                                       #####
##### Tested:  --                                             #####
#####                                                         #####
##### Purpose: The primary purpose of this mod is to perform  #####
#####          the SQL queries to the database in one         #####
#####          location, this will help cut down on           #####
#####          duplications of mods                           #####
###################################################################

import pymysql as MySQLdb
from datetime import *
from packages.Log import kwlog
db = None
cursor = None

def init():
    global db
    global cursor
    db = MySQLdb.connect("localhost","kitchenWizard","","KitchenWizard")
    cursor = db.cursor()
    kwlog.log("Connected to DB")


def close():
    db.close()
    kwlog.log("DB connection closed")


def get_generic_item_list():
    sql = "SELECT GroupName FROM Grouping"
    cursor.execute(sql)
    return cursor.fetchall()


def get_session_key_expire_data(key):
    kwlog.log("Get exp date for key")
    sql = "SELECT AgeOffDate FROM Session_Key WHERE SessionKey = %s" % (str(key))
    cursor.execute(sql)
    data = cursor.fetchone()
    return str(data[0])

def get_userid_from_session_key(key):
    kwlog.log("Get userid from session key")
    sql = "SELECT UserID FROM Session_Key WHERE SessionKey = %s;"
    cursor.execute(sql, key)
    data = cursor.fetchone()
    return str(data[0])


def get_product_by_barcode(barcode):
    kwlog.log("Get product by barcode")
    sql = "SELECT * FROM ProductInformation WHERE ProductID = %s;"
    cursor.execute(sql, str(barcode))
    return cursor.fetchone()


def get_group_by_name(name):
    kwlog.log("Get category by name")
    sql = "SELECT * FROM Grouping WHERE GroupName = %s;"
    cursor.execute(sql, name)
    return cursor.fetchone()


def get_inventory_list_for_user(userid):
    kwlog.log("Get items for user from DB")
    sql = "SELECT InventoryID, ProductID, ExperationDate, PercentUsed FROM Inventory WHERE UserID = %s;"
    cursor.execute(sql, userid)
    data = cursor.fetchall()
    return data


def get_password_hash_for_usr(userid):
    sql = "SELECT PasswordHash FROM Password WHERE User_id = %s;"
    cursor.execute(sql, userid)
    data = cursor.fetchone()
    return data


def is_item_in_inventory(item_id, userid):
    sql = "SELECT * FROM Inventory WHERE UserID = '%s' AND InventoryID = %s;"
    cursor.execute(sql, (str(userid), str(item_id)))
    data = cursor.fetchone()
    return data


def is_email_in_database(email):
    sql = "SELECT * FROM User_Information WHERE Email = %s;"
    cursor.execute(sql, email)
    data = cursor.fetchone()
    return data


def is_userid_in_DB(usr):
    sql = "SELECT UserID FROM User_Information WHERE UserID = %s;"
    cursor.execute(sql, usr)
    data = cursor.fetchone()
    return data


def put_group(name):
    kwlog.log("Put group")
    sql = "INSERT INTO `KitchenWizard`.`Grouping` (`GroupName`, `DateAdded`) VALUES (%s, %s);"
    try:
        cursor.execute(sql, (str(name), str(datetime.now())))
        db.commit()
        return True
    except:
        db.rollback()
        kwlog.log("Error adding new group")
        return False


def put_new_product(item):
    kwlog.log("Put new product")
    sql = "INSERT INTO `KitchenWizard`.`ProductInformation` (`ProductID`, `ProductName`, `ProductDiscription`, `Manufacturer`, `Quantity`) VALUES (%s, %s, %s, %s, %s);"
    try:
        cursor.execute(sql,(str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4])))
        db.commit()
        return True
    except:
        db.rollback()
        kwlog.log("Error adding new product")
        return False


def put_item_in_inventory(barcode, userid):
    kwlog.log("Put item in inventory")
    sql = "INSERT INTO `KitchenWizard`.`Inventory` (`UserID`, `ProductID`, `DateAdded`) VALUES (%s, %s, %s);"
    try:
        cursor.execute(sql, (str(userid), str(barcode), str(datetime.now())))
        db.commit()
        return True
    except:
        db.rollback()
        kwlog.log("Error adding item to inventory")
        return False


def put_confirmation_code_in_database(code, username):
    sql = "INSERT INTO Activation_Key (Code, UserID) VALUES (%s, %s);"
    try:
        cursor.execute(sql, (str(code), str(username)))
        db.commit()
        return True
    except:
        db.rollback()
        kwlog.log("Error adding confirmation code to DB")
        return False


def put_new_account(username, fname, lname, email, hash):
    d = str(datetime.now())
    date = datetime.today()
    date = date + timedelta(6 * 30)
    hash = encrypt_password(hash)
    f_sql = "INSERT INTO User_Information (UserID, FirstName, LastName, Email, CreationDate) VALUES ('%s', '%s', '%s', '%s', '%s');" % (username, fname, lname, email, d)
    p_sql = "INSERT INTO Password (PasswordHash, User_id, UpdatedOn) VALUES ('%s', '%s', '%s');" % (hash, username, d)
    s_sql = "INSERT INTO Session_Key (UserID, SessionKey, AgeOffDate) VALUES ('%s', '%s', '%s');" % (username, '0000000', date)

    try:
        cursor.execute(f_sql)
        kwlog.log("User_Information SQL completed")
        cursor.execute(p_sql)
        kwlog.log("Password SQL completed")
        cursor.execute(s_sql)
        kwlog.log("Session SQL completed")
        db.commit()
        return True
    except:
        #db.rollback()
        return False


def remove_item_from_inventory(item_id):
    sql = "DELETE FROM Inventory WHERE InventoryID = %s;"
    try:
        cursor.execute(sql, (item_id))
        db.commit()
        return True
    except:
        db.rollback()
        return False


def get_group_image_by_id(group_id):
    sql = "SELECT GroupImage FROM Grouping WHERE GroupID = '%s';" % (group_id)
    cursor.execute(sql)
    data = cursor.fetchone()
    return str(data[0])


def get_active_status(username):
    sql = "SELECT IsActivated FROM User_Information WHERE UserID = %s;"
    cursor.execute(sql, username)
    return cursor.fetchone()


def update_session_key_for_usr(userid, ses):
    date = datetime.today()
    date = date + timedelta(6 * 30)
    sql = "UPDATE `KitchenWizard`.`Session_Key` SET `SessionKey`=%d, `AgeOffDate`=%s WHERE `USERID`=%s;"
    try:
        cursor.execute(sql, (ses, date, username))
        db.commit()
        return True
    except:
        db.rollback()
        return False

def get_act_code(userid):
    sql = "SELECT Code FROM Activation_Key WHERE UserID = %s;"
    cursor.execute(sql, userid)
    data = cursor.fetchone()
    return str(data[0])


def update_activation_status_for_user(userid):
    kwlog.log("Update activation status")
    sql = "UPDATE User_Information SET IsActivated = '1' WHERE UserID = %s;"
    try:
        cursor.execute(sql, userid)
        db.commit()
        return True
    except:
        db.rollback()
        return False


def get_group_name_from_group_id(gid):
    sql = "SELECT GroupName FROM Grouping WHERE GroupID = %s;"
    cursor.execute(sql, gid)
    return cursor.fetchone()


def is_item_owned_by_user(userid, uid):
    sql "SELECT InventoryID FROM Inventory WHERE UserID = %s AND InventoryID = %s;"
    cursor.execute(sql, (userid, uid))
    if cursor.fetchone():
        return True
    else:
        return False


def update_inventory_item(uid, info):
    sql = "UPDATE Inventory SET ExperationDate = %s, PercentUsed = %s WHERE InventoryID = %s;"
    try:
        cursor.execute(sql, (info[0], info[1], uid))
        db.commit()
        return True
    except:
        db.rollback()
        return False

def get_groups():
    sql = "SELECT GroupID, GroupName FROM Grouping;"
    cursor.execute(sql)
    return cursor.fetchall()
