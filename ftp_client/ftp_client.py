import ftplib
import os
import re



class filedownload(object):
	def __init__(self, file_name, size):
		self.file = file_name
		self.size = size
		self.last_perc = 0
		self.downloaded = 0

	def handle_download(self, block):
		open(self.file, 'wb').write(block)
		self.downloaded += 1024
		perc_down = int((self.downloaded/self.size)*100)
		if perc_down > 100:
			perc_down = 100
		if perc_down != self.last_perc:
			print(perc_down, 'percent downloaded')
			self.last_perc = perc_down

class ftpdirectory(object):

	def __init__(self, dir_name, ftp_object):

		self.name = dir_name
		self.size = 0
		self.f = ftp_object

	def getsize(self):

		return self.size

	def calcsize(self):

		current = self.f.pwd()
		self.f.cwd(self.name)
		file_list = self.f.nlst()

		for FILE in file_list:
			if not self.is_dir(FILE):
				try:
					size = self.f.size(FILE)
					self.size += size
				except:
					continue
			else:
				dirobject = ftpdirectory(FILE, self.f)
				dirobject.calcsize()
				size = dirobject.getsize()
				self.size += size

		self.f.cwd(current)

	def is_dir(self, select):

		try:
			current = self.f.pwd()
			self.f.cwd(select)
			self.f.cwd(current) # Go back to previous directory
			return True
		except:
			return False
		


class fileupload(object):
	def __init__(self, file_name, size):
		self.file = file_name
		self.size = size
		self.last_perc = 0
		self.uploaded = 0

	def handle_upload(self, block):
		self.uploaded += 1024
		perc_up = int((self.uploaded/self.size)*100)
		if perc_up > 100:
			perc_up = 100
		if perc_up != self.last_perc:
			print(perc_up, 'percent uploaded')
			self.last_perc = perc_up


class ftpclient(object):

	def __init__(self):

		self.f = None
		self.command = input("Josh's ftp > ")

		while self.command != "quit":

			if re.match("open", self.command):
				self.open()

			elif self.command == "ls":
				self.ls()

			elif self.command == "pwd":
				self.pwd()

			elif re.match("cd", self.command):
				self.cd()

			elif re.match("bookmark$", self.command):
				self.bookmark()

			elif re.match("bookmarks", self.command):
				self.bookmarks()

			elif re.match("download ", self.command):
				self.download()

			elif re.match("upload", self.command):
				self.upload()

			elif re.match("mkdir", self.command):
				self.mkdir()

			elif re.match("dirsize", self.command):
				self.dirsize()

			self.command = input("Josh's ftp > ")


	def open(self):
		'''Connects to ftp server'''

		self.host = self.handle_command("open")
		if self.host:
			try:
				self.f = ftplib.FTP(self.host)
				print("Connected to '%s'" % self.host)
				self.f.login("anonymous")
				print("Logged in to '%s'" % self.host)
			except:
				print("Could not connect to '%s'" % self.host)

	def ls(self):
		'''Lists contents of current server directory'''

		try:
			self.f.dir()
		except:
			if not self.f:
				print("Can't list..... Not connected to a host")
			else:
				print("Unknown Error")

	def pwd(self):
		'''Prints server working directory'''

		try:
			cwd = self.f.pwd()
			print("'%s'" % cwd)
		except:
			if not self.f:
				print("Can't pwd..... Not connected to a host")
			else:
				print("Unknown Error")

	def cd(self):
		'''Changes working directory on ftp server'''

		if not self.f:
			print("Can't cd..... Not connected to a host")
			return
		path = self.handle_command("cd")
		if path:
			try:
				self.f.cwd(path)
				cwd = self.f.pwd()
				print("Changed working directory to '%s'" % cwd)
			except:
				print("Can't change directory to '%s'" % path)

	def download(self):
		'''Downloads file to current working directory'''

		if not self.f:
				print("Can't download..... Not connected to a host")
				return

		if re.match("download -r ", self.command):
			directory = self.handle_command("download -r")
			self.download_rec(directory = directory)

		else:

			FILE = self.handle_command("download")
			if FILE:
				try:
					size = self.f.size(FILE)
					fileprog = filedownload(FILE, size)
					self.f.retrbinary("RETR %s" % FILE, fileprog.handle_download, 1024)
					print("Downloaded '%s' to cwd" % FILE)
				except:
					if self.is_dir(FILE):
						print("'%s' is a directory and can't be downloaded non-recursively. Try 'download - r'" % FILE)
					else:
						print("Can't download '%s'" % FILE)


	def download_rec(self, directory):
		'''recursively downloads input directory'''

		current = self.f.pwd()

		local_current = os.getcwd()

		self.f.cwd(directory)

		os.mkdir(directory)

		os.chdir(directory)
		
		file_list = self.f.nlst()

		for FILE in file_list:
			if not self.is_dir(FILE):
				try:
					size = self.f.size(FILE)
					#fileprog = filedownload(FILE, size)
					#self.f.retrbinary("RETR %s" % FILE, fileprog.handle_download, 1024)
					self.f.retrbinary("RETR %s" % FILE, open(FILE, 'wb').write)
					print("Downloaded '%s' to cwd" % FILE)
				except:
					continue
			else:
				self.download_rec(FILE)

		self.f.cwd(current)
		os.chdir(local_current)


	def is_dir(self, select):
		'''returns true if select is directory'''
		try:
			current = self.f.pwd()
			self.f.cwd(select)
			self.f.cwd(current) # Go back to previous directory
			return True
		except:
			return False



	def upload(self):
		'''Uploads file to working directory'''
		if not self.f:
			print("Can't upload..... Not connected to a host")
			return
		FILE = self.handle_command("upload")
		if FILE:
			try:
				size = os.path.getsize(FILE)
				path = os.getcwd() + '/'
				mah = path + FILE
				thefile = open(mah, 'rb')
				fileprog = fileupload(FILE, size)
				self.f.storbinary("STOR %s" % FILE, thefile, 1024, fileprog.handle_upload)
				print("Uploaded '%s' to cwd" % FILE)
			except:
				print("Can't upload '%s'" % FILE)

	def mkdir(self):
		'''Creates directory'''
		if not self.f:
			print("Can't cd..... Not connected to a host")
			return

		folder = self.handle_command("mkdir")
		if folder:
			try:
				self.f.mkd(folder)
				print("Created directory '%s'" % folder)
			except:
				print("Can't create directory '%s'" % folder)

	def bookmark(self):
		'''Bookmarks current ftp server'''
		if not self.f:
			print("Can't bookmark.... Not connected to host")
			return
		name = self.host
		f = open('bookmarks.txt', 'a')
		f.write(name + '\n')
		f.close
		print("Bookmarked '%s'" % self.host)

	def bookmarks(self):
		'''Displays bookmarks'''
		no = 1
		try:
			f = open('bookmarks.txt', 'r')
		except:
			print('No bookmarks')
			return
		for line in f:
			print(str(no) + ':' + '\t%s' % line)
			no += 1

	def dirsize(self):
		'''Prints size of given directory'''

		if not self.f:
			print("Can't get size.... Not connected to host")
			return

		print("Please wait this may take awhile")
		directory = self.handle_command("dirsize")
		dirobject = ftpdirectory(directory, self.f)
		dirobject.calcsize()
		size=dirobject.getsize()
		print("Done")
		print("Size:", size, "bytes")



	def handle_command(self, func):
		'''Returns argument when a command is given'''

		if re.match(func + " [\S]+$", self.command):
			a = re.search("[\S]+$", self.command)
			arg = a.group()
			return arg
		else:
			print("Please provide valid argument")
			return None

def main():
	client = ftpclient()

main()