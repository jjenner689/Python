'''

Phase three: Templating

Templating allows a program to replace data dynamically in an html file. 

Ex: A blog pag:, we wouldn't write a whole new html file for every blog page. We want to write the html part and styling just once, then just inject the different blog text into that page. 

In the last exercise, we added a piece of python code that got called when an request came in.  Ex: a request for / would call a function to handle that request and return html. 

By doing this, it allows us to change the html on the fly, and return a blog post with updated values.

Ex: When a request comes in for index (/), our index_page() function gets called and does the following:
   
   - read the file data for index.html 

   - change the ###Title### string to the string "This is templating"
  
   - return the changed html string 

Steps:

1) Add the following line to index.html in the body

<h2>###Title###</h2>

2) Write a function render_template to take an html template, and a hash called context. 

   render_template takes the html data as a string from the file and returns that string so that you can swap it out for the http_response variable.

   Ex: render_template("<html>...",{"Title":"This is templating"})

   - Render will the try to replace all the fields in that hash

   Ex: context = {"Title":"This is the title","BlogText":"this is blog data"}

   In the html template replace ###Title### and ###BlogText### with corresponding key values.

   - Test by using this context {"Title":"This is the title","BlogText":"this is blog data"}

3) Add render_template to index_page with the sample context above

'''

import socket
import re


HOST, PORT = '', 8888
VIEWS_DIR = "./templates"


def open_file(name):
	with open(name, 'r') as f:
		data = f.read()
	return data

def about_page():
	html = open_file('./templates/about.html')
	return html, "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

def index_page():
	html = open_file('./templates/index.html')
	return html, "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

def read_bear():
	with open('./templates/bear.jpg', 'rb') as f:
		return f.read(), "HTTP/1.1 200 OK\r\nContent-Type: image/jpeg\r\n\r\n"

def render_template(html, dic):
	for i in dic:
		html = html.replace('###%s###' % i,  dic[i])
	return html


def run_server():
	urls = {'/about.html': about_page,
		   '/': index_page,
		   '/bear.jpg': read_bear}

	listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	listen_socket.bind((HOST, PORT))
	listen_socket.listen(1)

	print 'Serving HTTP on port %s ...' % PORT
	while True:
		client_connection, client_address = listen_socket.accept()
		request = client_connection.recv(4096)
		if not request:
			continue
		data = request.split('\r\n')

		site = re.search('(/[A-Za-z]*\.*[a-z]*)', data[0]).groups()[0]

		if site == '/favicon.ico':
			continue

		html, header = urls[site]()

		html = render_template(html, {'Title': 'This is templating'})
	
		http_response = "%s%s" % (header, html) #This hould work!!!

		client_connection.sendall(http_response) #We are not putting header as works fine
		client_connection.close()

run_server()




