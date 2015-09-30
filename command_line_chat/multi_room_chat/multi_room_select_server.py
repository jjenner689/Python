from socket import *
from time import ctime
from select import select
from queue import Queue

HOST = 'localhost'
PORT = 5000
ADDR = (HOST, PORT)
BUF = 1024

def main():

	try:

		server = socket(AF_INET, SOCK_STREAM)
		server.setblocking(0)
		server.bind(ADDR)
		server.listen(5)

		inputs = [server]
		outputs = []
		clients = {}

		messages = {}

		while True:

			i, o, e = select(inputs, outputs, inputs)

			#inputs
			for s in i:
				if s is server:
					conn, addr = s.accept()
					print('connection made on %s' % str(addr))
					conn.setblocking(0)
					inputs.append(conn)
					num = len(clients) + 1
					name = 'client ' + str(num)
					conn.send(bytes(name, 'utf-8'))
					while True:
						try:
							room = conn.recv(BUF).decode('utf-8')
						except:
							pass
						else:
							break
					clients[conn] = (name, room)
					messages[conn] = Queue()

				else:
					data = s.recv(BUF).decode('utf-8').strip()
					if data:
						name = clients[s][0]
						room = clients[s][1]
						if data[0:3] == '#me':
							message = '[%s] %s' % (name, data[3:])
							full_message = (room, message)
							for cl in clients:
								messages[cl].put(full_message)
								outputs.append(cl)
						elif data[0:3] == '#co':
							room = data[3:]
							clients[s] = (name, room)
					else:
						#close connection
						if s in outputs:
							outputs.remove(s)
						inputs.remove(s)
						del clients[s]
						del messages[s]
						print('connection at %s lost' % str(s.getsockname()))
						s.close()
			#outputs
			for s in o:
				try:
					response = messages[s].get(0)
				except: #empty queue so no response for it
					outputs.remove(s)
				else:
					sender_room = response[0]
					receiver_room = clients[s][1]
					if sender_room is receiver_room:
						s.send(bytes(response[1], 'utf-8'))

			#broken connection
			for s in e:
				if s in outputs:
					outputs.remove(s)
				inputs.remove(s)
				del messages[s]
				print('connection at %s lost' % str(s.getsockname()))
				s.close()

	except KeyboardInterrupt:
		server.close()

if __name__ == '__main__':
	main()

