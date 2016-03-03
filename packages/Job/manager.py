import threading
import re
import urllib
from packages.Log import kwlog
from packages.Job.util import strip_headers
from packages.Login.createAccount import add_new_user
worker_cap = 7
job_queue = []
job_queue_blocked = False

def start_job(connection):
	data = connection.recv(4096).decode("utf-8")
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
			thread.start()
			job_queue.append(thread)
			job_queue_blocked = False
			break
	kwlog.log("Job added to queue")
	
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
	kwlog.log("job removed from queue")

def monitor_jobs():
	global job_queue
	while True:
		for thread in job_queue:
			if not thread.is_alive():
				remove_job(thread)
			
def service_request(data, connection):
	result = None
	print(data[0])
	if "command=register" in data[0]:
		username = re.search("username=[^&]*&", data[0]).group(0).split("=")[1].split('&')[0]
		print(username)
		fname = re.search("fname=[^&]*&", data[0]).group(0).split("=")[1].split('&')[0]
		print(fname)
		lname = re.search("lname=[^&]*&", data[0]).group(0).split("=")[1].split('&')[0]
		print(lname)
		email = re.search("email=[^&]*&", data[0]).group(0).split("=")[1].split('&')[0].replace("%40","@")
		print(email)
		password = re.search("password=[^&]*&", data[0]).group(0).split("=")[1].split('&')[0]
		print(password)
	
	connection.send("HTTP/1.1 200 OK\n\nHello".encode("utf-8"))
	add_new_user(username, fname, lname, email, password.encode("utf-8"))
	connection.close()
	return
