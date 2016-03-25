import threading
import re
import urllib
from packages.Log import kwlog
from packages.Job.util import value_from_header, replace_commas_with_semicolons, replace_commas_with_semicolons_for_groups, parse_ingredients
from packages.Login.createAccount import add_new_user
from packages.Login.updateAccount import update_account_activation_stats
from packages.Login.checkLogin import login_to_account
from packages.Listen.reply import send
from packages.Items.addItem import add_new_item
from packages.Items.addItem import add_new_item_man
from packages.Items.getItemList import get_item_list
from packages.Items.removeItem import remove_item
from packages.Items.updateItem import update_inventory_item, update_group_of_item
from packages.Recipes.addRecipe import add_recipe
from packages.Recipes.removeRecipe import remove_recipe
from packages.Recipes.getRecipeList import get_list_of_recipes, get_list_of_ingredients
from packages.Recipes.updateRecipe import update_recipe
from packages.Groups.getList import get_list_of_generic_items
worker_cap = 7
job_queue = []
job_queue_blocked = False

def start_job(connection):
	data = urllib.parse.unquote(connection.recv(4096).decode("utf-8"))
	data = data.split('\r\n')
	thread =threading.Thread(target=service_request, args=(data,connection))
	add_job(thread)

def add_job(thread):
	global job_queue
	global job_queue_blocked
	kwlog.log("Starting thread: " + str(thread))
	while True:
		if job_queue_blocked is True:
			continue
		else:
			if len(job_queue) == worker_cap:
				kwlog.log("Error Job queue filled")
			job_queue_blocked = True
			kwlog.log("Job added to queue")
			thread.start()
			job_queue.append(thread)
			job_queue_blocked = False
			break


def remove_job(thread):
	global job_queue
	global job_queue_blocked
	while True:
                if job_queue_blocked is True:
                        continue
                else:
                        job_queue_blocked = True
                        job_queue.remove(thread)
                        job_queue_blocked = False
                        break
	kwlog.log("Job removed from queue")

def monitor_jobs():
	global job_queue
	while True:
		for thread in job_queue:
			if not thread.is_alive():
				remove_job(thread)

def service_request(data, connection):
	result = None
	command = value_from_header(data, 'command')
	if command == "Error":
		print(str(data))
		connection.close()
		return
	if command == 'register':
		username = value_from_header(data, 'username')
		fname = value_from_header(data, 'fname')
		lname = value_from_header(data, 'lname')
		email = value_from_header(data, 'email')
		password = value_from_header(data, 'password')
		result = add_new_user(username, fname, lname, email, password.encode("utf-8"))

	if command == "activate":
		code = value_from_header(data, "code")
		result = update_account_activation_stats( code)

	if command == "login":
		username = value_from_header(data, 'username')
		password = value_from_header(data, 'password')
		kwlog.log(str(username + ":"+ password))
		result = login_to_account(username, password.encode("utf-8"))

	if command == "additem":
		barcode = value_from_header(data, 'barcode')
		sessionkey = value_from_header(data, 'sessionkey')
		result = replace_commas_with_semicolons(add_new_item(barcode, sessionkey))
	if command == "getitems":
		sessionkey = value_from_header(data, 'sessionkey')
		result = get_item_list(sessionkey)
		result = replace_commas_with_semicolons(result)

	if command == "removeitem":
		product_id = value_from_header(data, 'id')
		sessionkey = value_from_header(data, 'sessionkey')
		result = remove_item(product_id, sessionkey)

	if command == "getrecipes":
                sessionkey = value_from_header(data, 'sessionkey')
                result = replace_commas_with_semicolons(get_list_of_recipes(sessionkey))

	if command == "getingredients":
		sessionkey = value_from_header(data, 'sessionkey')
		recipeid = value_from_header(data, 'recipeid')
		result = get_list_of_ingredients(sessionkey, recipeid)
	if command == "removerecipe":
		recipe_id = value_from_header(data, 'recipeid')
		sessionkey = value_from_header(data, 'sessionkey')
		result = remove_recipe(recipe_id, sessionkey)

	if command == "updaterecipe":
		sessionkey = value_from_header(data, 'sessionkey')
		name = value_from_header(data, 'name')
                recipeid = value_from_header(data, 'recipeid')
		description = value_from_header(data, 'description')
		image = ''
		preptime = value_from_header(data, 'preptime')
		cooktime = value_from_header(data, 'cooktime')
		itemaction = value_from_header(data, 'itemaction')
		groupid = value_from_header(data, 'groupid')
		quantity = value_from_header(data, 'quantity')

                if sessionkey == None:
			sessionkey = ""
		if name == None:
			name = ""
		if recipeid == None:
			recipeid = ""
                if description == None:
			description = ""
                if preptime == None:
			preptime = ""
                if cooktime == None:
			cooktime = ""
                if itemaction == None:
			itemaction = ""
                if groupid == None:
			groupid = ""
		if quantity == None:
			quantity = ""
		result = update_recipe(recipeid, name, description, image, preptime, cooktime, [groupid, quantity], itemaction, sessionkey)
	if command == "getgrouplist":
		result = replace_commas_with_semicolons_for_groups(get_list_of_generic_items())

	if command == "updateitem":
		sessionkey = value_from_header(data, 'sessionkey')
		expiration = value_from_header(data, 'expiration')
		if expiration == "Error":
			expiration = ""
		percentused = value_from_header(data, 'percentused')
		if percentused == "Error":
			percentused = ""
		product_id = value_from_header(data, 'id')
		addit_arr = [expiration, percentused]
		result = update_inventory_item(addit_arr, product_id, sessionkey)
	if command == "updategroup":
		groupid = value_from_header(data, 'groupid')
		barcode = value_from_header(data, 'barcode')
		sessionkey = value_from_header(data, 'sessionkey')
		result = update_group_of_item(groupid, barcode, sessionkey)
	if command == "test":
		result = "success"
	if command == "manualadd":
		barcode = value_from_header(data, 'barcode')
		name = value_from_header(data, 'name')
		des = value_from_header(data, 'description')
		man = value_from_header(data, 'manufacturer')
		amount = value_from_header(data, 'amount')
		gid = value_from_header(data, 'group')
		exper_date = value_from_header(data, 'expiration')
		session_key = value_from_header(data, 'sessionkey')
		if gid == "na":
			gid = ""
		if exper_date == "na":
			exper_date = ""
		result = add_new_item_man(barcode, name, des, man, amount, gid, exper_date, session_key)
	if command == "addrecipe":
		session_key = value_from_header(data, 'sessionkey')
		name = value_from_header(data, 'name')
		des = value_from_header(data, 'description')
		preptime = value_from_header(data, 'preptime')
		if preptime == "Error":
			preptime = -1
		cooktime = value_from_header(data, 'cooktime')
		if cooktime == "Error":
                        cooktime = -1
		ingredients = value_from_header(data, 'ingredients')
		image = ''
		ingredients = parse_ingredients(ingredients)
		recipe = [name,des,ingredients,image,int(preptime),int(cooktime)]
		kwlog.log(str(recipe))
		result = add_recipe(session_key, recipe)

	kwlog.log("Result: " + str(result))
	send(result, connection)
	kwlog.log("Result sent")
	connection.close()
	kwlog.log("Connection closing")
	return
