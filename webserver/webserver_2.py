'''

Phase two: Routing + Controllers

On older websites, the url was just a reference to a file, so the url would be about.html.

On modern what we now call webapps, instead of asking for /about.html which is a reference to a file on disk, we use just /about 

This is because in modern webapps there is usually some code that runs before just returning the html. In our
case we want some python code to run first, maybe to apply some logic or read from the database, before html is returned.

In your browser a user would request <your site.com> + 

/ 
/about
/blog
/blog/1

In this section we are going to extend the work we do in the previous section, by creating a link in code
that for each url we call a python function. That function is then resposible for returning html.

Take code from Webserver1 for the next part of the exercise.

**** Test your code after each step ****

1) Add two new functions index_page() and about_page()

2) Create a hash called urls that maps between a http request like:
 "/" ====> calls index_page(), 
 "/about" =====>calls about_page()

3) Move your file reading code into both of those functions:
	index_page() ====> reads index.html, returns that data.
	about_page() ====>  about.html filereturns that data. 


So now when the webserver asks for the /about the webserver parses or sees that the request is for about. Then using the hash created calls about_page() which returns the html
that is given back to the browser.

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
	return html

def index_page():
	html = open_file('./templates/index.html')
	return html

def load_binary():
	with open("./templates/dream.png", 'rb') as f:
		return f.read().encode('utf-8')

def run_server():

	urls = {'/about.html': about_page,
		   '/': index_page}

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

		html = urls[site]()

		img = load_binary()
	
		http_response = """\
	HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n
	%s\n%s""" % (html, img)

		client_connection.sendall(http_response)
		client_connection.close()

run_server()

