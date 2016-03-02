import threading
from packages.Log import kwlog
from packages.Job.util import strip_headers
worker_cap = 7
job_queue = []
job_queue_blocked = False

def start_job(connection):
	data = connection.recv(4096).decode("utf-8")
	data = data.split('\r\n')
	data = strip_headers(data)
	thread = interpret_request(data)
	add_job(thread)
	connection.close()

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
			
def interpret_request(data):
	thread = None
	
	thread =threading.Thread(target=kwlog.log, args=("sample thread arg",))
	return thread
