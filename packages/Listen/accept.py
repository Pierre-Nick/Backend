import socket
from packages.Log import kwlog
from packages.Job import manager

def listen():
	try:
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		serversocket.bind(('', 8080))
		serversocket.listen(5)
		kwlog.log("Server is listening")
	except:
		kwlog.log("There was a problem while starting the server socket")

	while True:
		try:
			(clientsocket, address) = serversocket.accept()
			kwlog.log("Connection from: "+ str(address))
			manager.start_job(clientsocket)
		except:
			kwlog.log("Connection failed:")
			raise

	kwlog.log("Server has stopped listening")
