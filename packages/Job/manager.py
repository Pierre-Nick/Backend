import threading
import re
import urllib
from packages.Log import kwlog
from packages.Job.util import value_from_header
from packages.Login.createAccount import add_new_user
from packages.Login.updateAccount import update_account_activation_stats
from packages.Login.checkLogin import login_to_account
from packages.Listen.reply import send
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
		userid = value_from_header(data, "userid")
		result = update_account_activation_stats( userid, code)
	
	if command == "login":
		username = value_from_header(data, 'username')
		password = value_from_header(data, 'password')
		kwlog.log(str(username + ":"+ password))
		result = login_to_account(username, password.encode("utf-8"))
	if command == "test":
		result = "success"
	kwlog.log("Result: " + str(result))
	send(result, connection)
	kwlog.log("Result sent")
	connection.close()
	kwlog.log("Connection closing")
	return
