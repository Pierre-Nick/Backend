from packages.Items.addItem import __get_userid_from_key
from packages.Database.MySQL import get_recipes_for_user, get_ingredients_for_recipe, get_group_name_from_group_id
from packages.Log import kwlog

def get_list_of_recipes(session_key):

    try:
        userid =  __get_userid_from_key(session_key)
        if userid == "BAD_KEY":
            kwlog.log("bad key")
            raise
        recipes = get_recipes_for_user(userid)
        recipe_arr = []
        for recipe in recipes:
                recipe = list(recipe)
                recipe[7] = str(recipe[7])
                recipe_arr.append(recipe)
        return recipe_arr
		
    except:
        if kwlog.debug:
            raise
        return "Problem processing request"

def get_list_of_ingredients(session_key, recipeid):
    try:
        userid =  __get_userid_from_key(session_key)
        if userid == "BAD_KEY":
            kwlog.log("bad key")
            raise

        ingredients = get_ingredients_for_recipe(userid, recipeid)
        result = ""
        if ingredients is None:
            return ""
        for ingredient in ingredients:
            result += str(get_group_name_from_group_id(ingredient[0])[0])+ " " + str(ingredient[1])+"\n"
        return result
    except:
        if kwlog.debug:
            raise
        return "Problem processing request"
