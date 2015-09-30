from tkinter import *
import os
import re

class Application(object):
	def __init__(self):
		self.top = Tk()
		self.top.title("Josh's Text Editor")
		self.top.geometry("800x500")
		self.document_name = StringVar()
		self.document_name.set("Untitled Document")
		self.create_menus()
		self.create_widgets()

	def create_menus(self):
		menubar = Menu(self.top)
		filemenu = Menu(menubar, tearoff = 0)
		spellmenu = Menu(menubar, tearoff = 0)

		filemenu.add_command(label = "Open", command = self.open)
		filemenu.add_command(label = "Save", command = self.save)
		filemenu.add_command(label = "Save As....", command = self.save_as)
		filemenu.add_command(label = "Exit", command = self.top.quit)

		menubar.add_cascade(label = "File", menu = filemenu)

		spellmenu.add_command(label = "Correct", command = self.spell_check)

		menubar.add_cascade(label = "Spellcheck", menu = spellmenu)

		self.top.config(menu=menubar)

	def create_widgets(self):
		self.label = Label(self.top, textvariable = self.document_name, anchor = W)
		self.label.pack(fill = X)
		self.text_contents = Text(self.top)
		self.text_contents.pack(expand = YES, fill = BOTH)

	def open(self):
		Open_Window(self)

	def read_file(self, file_name):
		'''Reads text from given file and opens in text editor'''
		try:
			f = open(file_name, 'r')
			contents = f.read()
			f.close()
		except:
			contents = "Error!"
		self.text_contents.delete(1.0, END)
		self.text_contents.insert(END, contents)
		self.document_name.set(file_name)

	def save_as(self):
		Save_Window(self)

	def save(self):
		'''Writes text to file if already has file name, otherwise calls save as'''
		name = self.document_name.get()
		if name == "Untitled Document":
			self.save_as()
		else:
			f = open(name, "w")
			text = self.text_contents.get(1.0, END)
			f.write(text)
			f.close()

	def write_file(self, window, ev = None):
		'''Writes text from text editor to text file'''
		select = window.entry.get()
		f = open(select, "w")
		text = self.text_contents.get(1.0, END)
		f.write(text)
		f.close()
		self.document_name.set(select)
		window.top.destroy()


	def spell_check(self):

		Spell_Window(self)
		

class Open_Window(object):

	def __init__(self, app):

		self.top = Toplevel(app.top)
		self.create_frames()
		self.create_widgets()
		self.app = app

	def create_frames(self):
		self.list_frame = Frame(self.top)
		self.list_frame.grid(row = 0, column = 0, columnspan = 2)
		self.button_frame = Frame(self.top)
		self.button_frame.grid(row = 1, column = 0, sticky = W)

	def create_widgets(self):
		self.create_buttons()
		self.create_listbox()

	def create_listbox(self):
		self.files = Listbox(self.list_frame, height = 20, width = 40)
		self.files.bind("<Double-1>", self.click_file)
		self.files.pack(side = LEFT, fill = BOTH)
		self.populate()

		self.scroll = Scrollbar(self.list_frame, orient="vertical", command=self.files.yview)
		self.scroll.pack(side=RIGHT, fill = Y)
		self.files.config(yscrollcommand = self.scroll.set)
		
		
	def create_buttons(self):
		self.exit = Button(self.button_frame, text = "Exit",
			command = self.top.destroy, width = 5)
		self.open = Button(self.button_frame, text = "Open",
			command = self.click_file, width = 5)
		self.exit.pack(side = LEFT)
		self.open.pack(side = LEFT)

	def populate(self, current = os.curdir):
		'''Populates the open window with files and directories in cwd'''
		self.files.delete(0, END)
		filelist = os.listdir(current)
		self.files.insert(END, "..")
		for eachfile in filelist:
			self.files.insert(END, eachfile)


	def click_file(self, ev = None):
		'''Calls read_file if click file. Calls populate and changes directory if click 
		directory'''
		select = self.files.get(self.files.curselection())
		if not os.path.isdir(select):
			file_name = select
			self.app.read_file(file_name = file_name)
		else:
			self.current = os.chdir(select)
			self.populate(current = self.current)

class Save_Window(Open_Window):

	def create_frames(self):
		self.list_frame = Frame(self.top)
		self.list_frame.grid(row = 0, column = 0, columnspan = 2)

		self.entry_frame = Frame(self.top)
		self.entry_frame.grid(row=1, column =0, sticky = W)

		self.button_frame = Frame(self.top)
		self.button_frame.grid(row = 2, column = 0, sticky = W)

	def create_widgets(self):
		self.create_buttons()
		self.create_listbox()
		self.create_entry()

	def create_entry(self):
		self.entry = Entry(self.entry_frame, text = "*Enter here", width = 40)
		self.entry.pack()

	def create_buttons(self):
		self.exit = Button(self.button_frame, text = "Exit", 
			command = self.top.destroy, width = 5)
		self.save = Button(self.button_frame, text = "Save", 
			command = lambda: self.app.write_file(self), width = 5)
		self.exit.pack(side = LEFT)
		self.save.pack(side = LEFT)

	def click_file(self, ev = None):
		'''Calls populate if click directory. Copys file name to entry
		if click file'''
		select = self.files.get(self.files.curselection())
		if not os.path.isdir(select):
			self.entry.delete(0, END)
			self.entry.insert(END, select)
		else:
			self.current = os.chdir(select)
			self.populate(current = self.current)

class Spell_Window(object):

	def __init__(self, app):

		self.top = Toplevel(app.top)
		self.create_frames()
		self.create_widgets()
		self.app = app
		self.selected_word = None #Remembers word for which suggestions are listed for 
		self.fill_words()
	
	def fill_words(self):
		'''Calls find_errors and fills window with any errors found'''
		self.words.delete(0, END)
		self.corrections.delete(0, END)
		incorrect_words = self.find_errors()
		for i in incorrect_words:
			self.words.insert(END, i)

	def create_frames(self):

		top_frame = Frame(self.top)
		top_frame.pack(side=TOP, fill = X, expand = False)

		self.word_frame = Frame(top_frame)
		self.word_frame.pack(side = LEFT, fill = BOTH, expand= TRUE)

		self.corrections_frame = Frame(top_frame)
		self.corrections_frame.pack(side = RIGHT, fill = X, expand = TRUE)

		self.button_frame = Frame(self.top)
		self.button_frame.pack(side=BOTTOM, fill = X, expand = TRUE)

	def create_widgets(self):

		self.create_words_listbox()
		self.create_corrections_listbox()
		self.create_buttons()

	def create_words_listbox(self):

		self.words = Listbox(self.word_frame, height = 20)
		self.words.pack(side = LEFT, fill = BOTH, expand = True)
		self.words.bind("<Double-1>", self.show_corrections)

		self.words_scroll = Scrollbar(self.word_frame, orient = "vertical", 
			command = self.words.yview)
		self.words_scroll.pack(side = RIGHT, fill = Y)
		self.words.config(yscrollcommand = self.words_scroll.set)

	def create_corrections_listbox(self):

		self.corrections = Listbox(self.corrections_frame, height = 20)
		self.corrections.pack(side = LEFT, fill = BOTH, expand = True)

		self.corrections_scroll = Scrollbar(self.corrections_frame, 
			orient = "vertical", command = self.corrections.yview)
		self.corrections_scroll.pack(side = RIGHT, fill = Y)
		self.corrections.config(yscrollcommand = self.corrections_scroll.set)

	def create_buttons(self):

		exit = Button(self.button_frame, text = "Exit", width = 5, command = self.exit_spell_check)
		replace = Button(self.button_frame, text = "Replace", width = 5, 
			command = self.replace)
		find_corrections = Button(self.button_frame, text = "Find Corrections", width = 10, 
			command = self.show_corrections)

		exit.pack(side=LEFT)
		find_corrections.pack(side = LEFT)
		replace.pack(side=LEFT)


	def show_corrections(self, ev = None):
		word, wordlist = self.shorten_wordlist()
		self.selected_word = word
		suggestions = self.find_suggestions(word, wordlist)
		self.fill_corrections(suggestions)

	def shorten_wordlist(self):
		'''Matches all words in dictionary of similar length to selected word. Returns
		list of all matched words and selected word'''
		word = self.words.get(self.words.curselection())
		length = len(word)
		regex = re.compile("^[a-z]{"+str(length-1) +","+str(length+1)+"}$", re.MULTILINE)
		f = open("dictionary.txt", "r")
		wordlist = re.findall(regex, f.read()) #returns list of words of similar length
		f.close()
		return word, wordlist


	def find_suggestions(self, word, wordlist):
		'''Returns list of suggested corrections to given word'''
		word = word.lower()
		suggestions = []
		if len(word) >5:
			replace_no = 2
		else:
			replace_no = 1
		for j in range(len(word)):
			index = j
			fill = "[a-z]?"*replace_no
			regex=self.replace_index(word, fill, index, replace_no = replace_no)
			for i in wordlist:
				match = re.match(regex, i)
				if match != None:
					suggestions.append(i)
		return suggestions
	
	def fill_corrections(self, suggestions):
		'''Fills the corrections list with imput suggestions'''
		self.corrections.delete(0, END)
		for i in suggestions:
			self.corrections.insert(END, i)

	def replace_index(self, string, replacement, index, replace_no = 1):
		'''Replaces slice of string with input replacement'''
		string = string[:index] + str(replacement) + string[index+replace_no:]
		return string

	def find_errors(self):
		'''Finds spelling errors by matching word with words in a dictionary text file.
		Returns list off all errors'''
		text = self.app.text_contents.get(1.0, END)
		all_words = re.findall("[A-Za-z]+", text)
		incorrect_words = []
		f = open("dictionary.txt", "r")
		for word in all_words:
			found = False
			for dic_word in f:
				if word.lower().strip() == dic_word.lower().strip():
					found = True
					break
			f.seek(0)
			if not found:
				incorrect_words.append(word)
		for word in incorrect_words:
			self.highlight_word(word = word, color = 'red')
		f.close()
		return incorrect_words


	def highlight_word(self, word, color):
		'''Highlights input word in text editor to input color'''
		text = self.app.text_contents
		text.tag_config("flag", background = color)
		start = 1.0
		while True:
			pos = text.search(word, start, stopindex=END)
			if not pos:
				break
			pos_end = '{}+{}c'.format(pos, len(word))
			text.tag_add("flag", pos, pos_end)
			start = pos + "+1c" 

	def replace(self):
		'''Replaces word in text editor to selected correction'''
		try:
			word = self.selected_word
			correct_word = self.corrections.get(self.corrections.curselection())
			text = self.app.text_contents
			start = 1.0
			while True:
				pos = text.search(word, start, stopindex=END)
				if not pos:
					break
				pos_end = '{}+{}c'.format(pos, len(word))
				text.delete(pos, pos_end)
				text.insert(pos, correct_word)
			self.fill_words()
		except:
			pass

	def exit_spell_check(self):
		'''Exits spell check window and removes highlighting'''
		for word in self.words.get(0, END):
			self.highlight_word(word, '')
		self.top.destroy()



def main():

	app = Application()
	mainloop()

if __name__ == '__main__':
	main()
