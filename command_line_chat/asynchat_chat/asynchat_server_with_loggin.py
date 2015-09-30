import asyncore
import asynchat
from socket import *
import logging

HOST = 'localhost'
PORT = 4000
ADDR = (HOST, PORT)

class ChatServer(asyncore.dispatcher):
	channels = []

	def __init__(self, address):
		self.logger = logging.getLogger('ChatServer')
		self.logger.setLevel(logging.DEBUG)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		self.logger.addHandler(ch)
		asyncore.dispatcher.__init__(self)
		self.address = address
		self.create_socket(AF_INET, SOCK_STREAM)
		self.bind(address)
		self.logger.debug('bind to %s' % str(address))
		self.listen(5)

	def handle_accept(self):
		self.logger.debug('handle_accept()')
		conn, client_addr = self.accept()
		self.logger.debug('accepted request on %s' % str(client_addr))
		handler = ChatHandler(conn, client_addr)
		self.channels.append(handler)

	def handle_close(self):
		self.logger.debug('handle_close')
		for channel in self.channels:
			channel.handle_close()
		self.logger.debug('closed client sockets')
		self.logger.debug('closing server socket....')
		self.close()

class ChatHandler(asynchat.async_chat):

	def __init__(self, conn, client_addr):
		self.logger = logging.getLogger('ChatHandler')
		self.logger.setLevel(logging.DEBUG)
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		self.logger.addHandler(ch)
		asynchat.async_chat.__init__(self, conn)
		self.client_addr = client_addr
		self.logger.debug('handling request on %s' % str(client_addr))
		self.conn = conn
		self.buffer = []
		self.set_terminator(b'\r\n')

	def collect_incoming_data(self, data):
		data = data.decode('utf-8')
		self.logger.debug('collect_incoming_data():\n%d bytes\ndata: %s' % (len(data), data.strip()))
		self.buffer.append(data)

	def found_terminator(self):
		self.logger.debug('found_terminator()')
		msg = ''.join(self.buffer)
		self.buffer = []
		msg = '[%s] %s' % (self.client_addr[1], msg.strip())
		msg = bytes(msg, 'utf-8')
		for channel in ChatServer.channels:
			channel.push(msg)
		self.logger.debug('pushing data:\n%d bytes\ndata: %s' % (len(msg), msg))

	def handle_close(self):
		self.logger.debug('closing channel....')
		ChatServer.channels.remove(self)
		self.close()

def main():

	try:
		server = ChatServer(ADDR)
		asyncore.loop()
	except KeyboardInterrupt:
		server.handle_close() #Close sockets if keyboard interupt

if __name__ == '__main__':
	
	main()

