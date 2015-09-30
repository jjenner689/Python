from tkinter import *
from functools import partial
from imaplib import IMAP4_SSL
import email
from io import StringIO
import pickle
import collections

USER = ''
PASSWD = ''

class guimail(object):

	def __init__(self):
		self.top = Tk()
		self.top.title('My Mail Application')
		self.top.geometry('1280x720')
		self.create_frames()
		self.connect()
		self.create_widgets()

	def connect(self):

		self.s = IMAP4_SSL('imap.gmail.com', 993)
		self.s.login(USER, PASSWD)
		self.s.select('INBOX', True)

	def create_frames(self):
		self.top_frame = Frame(self.top, height = 50, bg = 'red')
		self.top_frame.pack(fill = X)

		self.bottom_frame = Frame(self.top)
		self.bottom_frame.pack(fill = BOTH, expand = True)

		self.list_frame = Frame(self.bottom_frame, width = 250, bg = 'white')
		self.list_frame.pack(side = LEFT, fill = Y)

		self.action_frame = Frame(self.bottom_frame)
		self.action_frame.pack(side = LEFT, fill = BOTH, expand = True, padx = 10, pady = 10)


	def create_mailbox_frame(self):

		self.canvas = Canvas(self.action_frame)
		self.canvas.pack(side = RIGHT, fill = BOTH, expand = True)

		self.mailbox_frame = Frame(self.canvas)
		
		self.canvas_frame = self.canvas.create_window((0,0),
			window=self.mailbox_frame, anchor = NW)

		self.scroll = Scrollbar(self.canvas, orient = "vertical", 
			command = self.canvas.yview)
		self.scroll.pack(side = RIGHT, fill = Y)

		self.canvas.config(yscrollcommand = self.scroll.set)

		self.mailbox_frame.bind("<Configure>", self.configure_canvas_scroll)
		self.canvas.bind('<Configure>', self.configure_frame_width)

	def create_message_frame(self):

		self.message_frame = Frame(self.action_frame, bg = 'purple')
		self.message_frame.pack(side=LEFT, fill = BOTH, expand = True)

		self.message_box = Text(self.message_frame)
		self.message_box.pack(side=LEFT, fill = BOTH, expand = True)

		self.scroll = Scrollbar(self.message_frame, orient = "vertical", 
			command = self.message_box.yview)
		self.scroll.pack(side = RIGHT, fill = Y)

		self.message_box.config(yscrollcommand = self.scroll.set)


	def clear_canvas(self, canvas):
		canvas.destroy()

	def clear_frame(self, frame):
		frame.destroy()

		
	def configure_frame_width(self, event):
		canvas_width = event.width
		self.canvas.itemconfig(self.canvas_frame, width = canvas_width)

	def configure_canvas_scroll(self, event):
		self.canvas.configure(scrollregion=self.canvas.bbox("all"))
		
	def create_buttons(self):
		self.compose_button = Button(self.top_frame, text = 'COMPOSE', bg = 'blue', width = 15,
			fg = 'white', command = self.create_compose_window)
		self.compose_button.pack(side = LEFT, padx=22, pady=10)

		self.page_label = Label(self.top_frame, text = '1-50 of 72', bg = 'red') #Needs to be made to only load 50 pages at a time
		self.page_label.pack(side = RIGHT, padx = 10)

		self.older_button = Button(self.top_frame, text = '>')
		self.older_button.pack(side = RIGHT)

		self.newer_button = Button(self.top_frame, text = '<')
		self.newer_button.pack(side = RIGHT)

	def create_listbox(self):
		self.listbox = Listbox(self.list_frame)
		self.listbox.pack(fill = X, padx = 10, pady = 10)

		files = ('Inbox', 'Sent', 'Spam', 'Drafts')

		for i in files:
			self.listbox.insert(END, i)

		self.listbox.bind('<Double-1>', self.list_click)

	def list_click(self, event):
		select = self.listbox.get(self.listbox.curselection())
		if select == 'Inbox':
			self.clear_frame(self.message_frame) #maybe make frame a variable so always delete what's in middle
			self.load_inbox()

	def load_inbox(self):

		self.create_mailbox_frame()
		self.show_mail()


	def down_mail(self):

		self.load_mail()

		print('Downloading mail......')
			
		retcode, msg_ids = self.s.uid('search', None, '(UNSEEN)')
		msg_ids = msg_ids[0].decode('utf-8').split()

		for i in msg_ids:

			if i in self.mail_dic:
				continue

			else:

				rsp, data = self.s.uid('fetch', i, '(BODY.PEEK[HEADER])')
				raw_header = data[0][1].decode('utf-8')
				header_ = email.message_from_string(raw_header)

				from_ = header_['From']
				subject = header_['Subject'].replace('\n', '').replace('\r', '')

				short_from = re.match('[^<]+', from_)
				from_ = short_from.group()

				self.mail_dic[i] = (from_, subject, raw_header)

		f = open('mail_dic.dat', 'wb')
		pickle.dump(self.mail_dic, f)
		f.close()

	def load_mail(self):

		try:
			f = open('mail_dic.dat', 'rb')
			self.mail_dic = pickle.load(f)
			f.close()
		except: # will need to create exception for eof error
			self.mail_dic = collections.OrderedDict()


	def show_mail(self):
	
		Grid.columnconfigure(self.mailbox_frame, 2, weight=1)
		num = 0
		for i in reversed(self.mail_dic):

			check = Checkbutton(self.mailbox_frame)
			check.grid(row = num, column = 0)
			
			label = Label(self.mailbox_frame, text = self.mail_dic[i][0],
				anchor = W)
			label.grid(row = num, column = 1, sticky = W + E + N + S)

			label = Label(self.mailbox_frame, text = self.mail_dic[i][1],
				anchor = W, bg = 'gray')
			label.grid(row = num, column = 2, sticky = W + E + N + S)

			label.bind('<Button-1>', partial(self.click, i))
			label.bind('<Enter>', partial(self.change_background, 'yellow', label))
			label.bind('<Leave>', partial(self.change_background, 'gray', label))

			num += 1

	def change_background(self, color, widget, event):
		widget.config(bg = color)

	def click(self, uid, event):
		self.clear_canvas(self.canvas)
		self.create_message_frame()
		self.open_mail(uid)

	def delete_contents(self, widget, event):
		widget.delete(0, END)

	def open_mail(self, uid):
		raw_header = self.mail_dic[uid][2]
		header_ = email.message_from_string(raw_header)
		body = self.fetch_decode(uid)
		body = email.message_from_string(body)
		self.message_box.insert(END, body)

	def fetch_decode(self, uid):
		body = None
		rsp, data = self.s.uid('fetch', uid, '(RFC822)')
		email_msg = email.message_from_bytes(data[0][1]) 
		if email_msg.is_multipart():
			for part in email_msg.walk():       
				if part.get_content_type() == "text/plain":
					body = part.get_payload(decode=True) 
					body = body.decode()

				elif part.get_content_type() == "text/html":
					continue
		if body:
			return body
		else:
			return 'Could not fetch body of this email'

	def create_widgets(self):
		self.create_buttons()
		self.create_listbox()
		self.down_mail()
		self.load_inbox()

	def create_compose_window(self):
		self.compose_window = Toplevel(self.top)
		self.compose_window.title('New Message')
		self.compose_frame = Frame(self.compose_window)
		self.compose_frame.pack(fill = BOTH, expand = True)

		to_field = Entry(self.compose_frame, font = ('', 10,'italic'))
		to_field.insert(END, 'To')
		to_field.bind('<Button-1>', partial(self.delete_contents, to_field))
		to_field.pack(fill = X)

		subject_field = Entry(self.compose_frame, font = ('', 10,'italic'))
		subject_field.insert(END, 'Subject')
		subject_field.bind('<Button-1>', partial(self.delete_contents, subject_field))
		subject_field.pack(fill = X)

		content_field = Text(self.compose_frame)
		content_field.pack(fill = BOTH, expand = True)

		button_frame = Frame(self.compose_frame)
		button_frame.pack(fill = X)

		send_button = Button(button_frame, text = 'Send', bg = 'blue', fg = 'white')
		send_button.pack(side = LEFT)





def main():
	app = guimail()
	mainloop()

if __name__ == '__main__':
	main()

