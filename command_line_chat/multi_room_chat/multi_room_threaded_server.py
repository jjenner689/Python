from socket import *
from threading import Thread
from queue import Queue
import sys

HOST = 'localhost'
PORT = 5000
BUFSIZE = 1024
ADDR = (HOST, PORT)

qclient = Queue()
qmessage = Queue()
clientlist = {}

s = socket(AF_INET, SOCK_STREAM)
s.bind(ADDR)
s.listen(5)

def listen():
	while True:
		conn, addr = s.accept()
		name = 'client 1'
		num = 1
		if clientlist == {}:
			pass
		else:
			while name in clientlist:
				num +=1 
				name = 'client ' + str(num)
		conn.send(bytes(name, 'utf-8'))
		room = conn.recv(BUFSIZE).decode('utf-8')
		client = (conn, addr, room, name)
		clientlist[name] = (conn, room)
		qclient.put(client)
		treader = Thread(target = reader)
		treader.start()

def reader():
	client = qclient.get()
	conn = client[0]
	addr = client[1]
	room = client[2]
	name = client[3]
	while True:
		data = conn.recv(1024).decode('utf-8').strip()
		if data[0:3] == '#me': #message tag so treat as message
			message = (data[3:], name, room)
			qmessage.put(message)
		elif data[0:3] == '#co': #command tag so treat as command
			room = data[3:]
			clientlist[name] = (conn, room)

def sender():
	while True:
		message = qmessage.get()
		room = message[2]
		message = '[%s] %s' % (message[1] , message[0])
		for i in clientlist:
			if clientlist[i][1] == room:
				clientlist[i][0].send(bytes(message, 'utf-8'))
			else:
				pass

def main():
	try:

		tlisten = Thread(target = listen)

		tsender = Thread(target = sender)

		tlisten.start()

		tsender.start()

	except KeyboardInterrupt:
		s.close() 


if __name__ == '__main__':
	main()


