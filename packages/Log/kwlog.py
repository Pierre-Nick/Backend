import datetime

lock = 0
debug = False
default_logfile = "/tmp/kitchenwizard.log"
logfile = None
loghandle = None

def init():
	global	logfile
	global loghandle
	if logfile is None:
		logfile =  default_logfile
	loghandle = open(logfile, 'a')

def log( message):
	if message is None:
		return
	message = str(datetime.datetime.now()) +": "+ message + "\n"

	while True:
		if lock != 0:
			continue
		else:
			log = 1
			if debug:
				print(message)
			loghandle.write(message)
			log = 0
			break


def close():
	loghandle.close()