from packages.Log import kwlog
from packages.Database import MySQL

def get_group_id(name):
    print(name)
    return MySQL.get_group_by_name(name)
