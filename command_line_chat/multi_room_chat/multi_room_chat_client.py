
from socket import *
from threading import Thread
from tkinter import *



HOST = 'localhost'
PORT = 5000
BUFSIZE = 1024
ADDR = (HOST, PORT)



class client(object):
	
	def __init__(self):
		self.top = Tk()
		self.top.geometry('600x500')
		menubar = Menu(self.top)
		roommenu = Menu(menubar, tearoff = 0)
		roommenu.add_command(label = "Room 1", command = lambda: self.change_room('1'))
		roommenu.add_command(label = "Room 2", command = lambda: self.change_room('2'))
		roommenu.add_command(label = "Room 3", command = lambda: self.change_room('3'))
		menubar.add_cascade(label = "Change Room", menu = roommenu)
		self.top.config(menu = menubar)
		self.frame0 = Frame(self.top)
		self.frame1 = Frame(self.top)
		self.frame2 = Frame(self.top)
		self.frame0.pack(fill = X, expand = True)
		self.frame1.pack(fill = BOTH, expand = True)
		self.frame2.pack()
		self.room = StringVar()
		self.room.set('1')
		self.client_no = StringVar()
		self.client_no.set("<None>")
		self.create_widgets()
		self.start()

	def create_widgets(self):

		Label(self.frame0, text = "Name:", anchor = W).pack(side = LEFT)
		Label(self.frame0, textvariable = self.client_no, anchor = W).pack(side = LEFT)
		Label(self.frame0, textvariable = self.room, anchor = W).pack(side = RIGHT)
		Label(self.frame0, text = "Room:", anchor = W).pack(side = RIGHT)
		
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
		message = '#me' + self.entrybox.get('1.0', END) #Add message tag (not command)
		self.entrybox.delete('1.0', END)
		self.s.send(bytes(message, 'utf-8'))

	def receive(self):
		while True:
			message = self.s.recv(BUFSIZE).decode('utf-8')
			self.display(message)

	def display(self, text):

		message = "%s\n" % text
		self.chatbox.config(state = 'normal')
		self.chatbox.insert(END, message)
		self.chatbox.config(state = 'disabled')

	def start(self):
		self.s = socket(AF_INET, SOCK_STREAM)	
		self.s.connect(ADDR)
		name = self.s.recv(BUFSIZE).decode('utf-8')
		self.s.send(bytes(self.room.get(), 'utf-8'))
		self.client_no.set(name)
		Thread(target = self.receive, daemon = True).start()

	def change_room(self, room):
		self.room.set(room)
		self.clear_chatbox()
		command = '#co' + room #Add command tag
		self.s.send(bytes(command, 'utf-8'))

	def clear_chatbox(self):
		self.chatbox.config(state = 'normal')
		self.chatbox.delete('1.0', END)
		self.chatbox.config(state = 'disabled')
		







client = client()
mainloop()





