import socket

def send(data, connection):
	connection.send(("HTTP/1.1 200 OK\n\n"+ str(data)).encode("utf-8"))
