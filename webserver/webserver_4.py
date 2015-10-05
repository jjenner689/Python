'''

Phase four: Refactor urls

We want to move away from exact string matching, or having to write a special parser for each url. Changing it to use regex allows us to add complex url handling and pull out data to pass along easily.


1) Add this,


urlpatterns = [(r'^/$',index_page),
			   (r'^/about$',about_page),
			   (r'^/blog$',blog_index_page),
			   (r'^/blog/(\d+)',blog_page)]

def blog_index_page():
	pass

def blog_page(id):
	pass

   - create a blog_index.html with some basic html
  
   - create a blog.html with basic html

2) Write a function url_dispatch(url) where url is the http file name request

   - this function loops through urlpatterns using re.match and urlpatterns[0]

   - if a match if found it calls the matching function

   - if a pattern has a grouping like /blog/(\d+) you pass the first group item to the function

   Ex: a request for /blog comes in the regular expressions matches the third url patter, so blog_index_page is called

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

def blog_index_page():
	html = open_file('./templates/blog.html')
	return html, "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

def blog_page(id_):
	html = open_file('./templates/blog%s.html' % id_)
	return html, "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

def urlpatterns(url):
	urlpatterns = [(r'^/$',index_page),
			   (r'^/about$',about_page),
			   (r'^/blog$',blog_index_page),
			   (r'^/blog/(\d+)',blog_page),
			   (r'^/bear.jpg', read_bear)]

	for i in urlpatterns:
		rm = re.match(i[0],url)
		if rm:
			if len(rm.groups()):
				return i[1](rm.groups()[0])
			else:
				return i[1]()


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

	site = re.search('(/[A-Za-z\./1-9]*) ', data[0]).groups()[0]

	if site == '/favicon.ico':
	  continue

	html, header = urlpatterns(site)

	html = render_template(html, {'Title': 'This is templating'})
  
	http_response = "%s%s" % (header, html) #This hould work!!!

	client_connection.sendall(http_response) #We are not putting header as works fine
	client_connection.close()

run_server()

