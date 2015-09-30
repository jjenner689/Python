from socket import *
from threading import Thread
from tkinter import *


HOST = 'localhost'
PORT = 4000
BUFSIZE = 1024
ADDR = (HOST, PORT)
NAME = 'me'


class clientgui(object):
	
	def __init__(self):
		self.top = Tk()

		self.top.geometry('600x500')
		self.frame1 = Frame(self.top)
		self.frame2 = Frame(self.top)
		self.frame1.pack(fill = BOTH, expand = True)
		self.frame2.pack()
		menubar = Menu(self.top)
		quitmenu = Menu(menubar)
		quitmenu.add_command(label = 'Quit', command = self.exit)
		menubar.add_cascade(label = 'File', menu = quitmenu)
		self.top.config(menu = menubar)
		self.create_widgets()
		self.start()

	def create_widgets(self):

		self.chatbox = Text(self.frame1)
		self.chatbox.pack(side = LEFT, fill = BOTH, expand = True)
		self.chatbox.config(state = 'disabled')

		self.scroll = Scrollbar(self.frame1, command = self.chatbox.yview, orient = 'vertical')
		self.scroll.pack( side = RIGHT, fill = Y)

		self.chatbox.config(yscrollcommand = self.scroll.set)

		self.entrybox = Text(self.frame2, height = 4)

		self.send_button = Button(self.frame2, text = "Send", width = 7, font = 16, command = self.send)
		self.send_button.pack(side = RIGHT, fill = Y)
		self.entrybox.pack(side = LEFT, fill = X, expand = True)

		self.top.bind('<Return>', self.send)

	def send(self, ev = None):
		message = self.entrybox.get('1.0', END) + '\r\n'
		self.entrybox.delete('1.0', END)
		self.s.send(bytes(message, 'utf-8'))

	def receive(self):
		while True:
			message = self.s.recv(BUFSIZE).decode('utf-8').strip()
			self.display(message)

	def display(self, text):

		message = "%s\n" % text
		self.chatbox.config(state = 'normal')
		self.chatbox.insert(END, message)
		self.chatbox.config(state = 'disabled')

	def start(self):
		self.s = socket(AF_INET, SOCK_STREAM)	
		self.s.connect(ADDR)
		t = Thread(target = self.receive)
		t.daemon = True
		t.start()

	def exit(self):
		self.s.close()
		self.top.quit()






def main():

	client = clientgui()
	mainloop()
	client.exit()

if __name__ == '__main__':
	main()





