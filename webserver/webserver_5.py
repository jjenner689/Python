'''

Phase Five: DB Support

1) Using "sqlite3 blog.db"
   
    - create a table called posts, which has an id, post_name, post_text
    - add a row to this table, with a post name and post text

2) add the line below - your file must be named blogmodel.py

import blogmodel 

3) Update blog.html template to have two template tags for ###post_name###, ###post_text###

4) Update blog_page(id) to use BlogModel to read, getting back post_name and post_text for a given primary key id

5) Using the data, render blog.html with the right text

Once completed, you should be able to add rows through sqlite3 then go to your webserver:

localhost:8888/blog/1 -> returns a blog post with the data from the first row in the db
localhost:8888/blog/2 -> next row
localhost:8888/blog/... 

   


'''

import sqlite3
import blogmodel
import socket
import re
HOST, PORT = '', 8888

def blog_page(id_):
	bp = blogmodel.BlogModel('blog.db')
	posts = bp.read(id_)
	return posts[0], posts[1]

def blog_index():
	bp = blogmodel.BlogModel('blog.db')
	posts = bp.readall()
	return posts

def return_url(request):
	data = request.split('\r\n')
	url = re.search('(/[A-Za-z\./1-9]*) ', data[0]).groups()[0]
	return url

def open_file(name):
  with open(name, 'r') as f:
	data = f.read()
  return data

def urlpatterns(url):
	urlpatterns = [(r'^/blog/(\d+)',blog_html),
					(r'^/blog$',blog_index_html)]

	for i in urlpatterns:
		rm = re.match(i[0],url)
		if rm:
			if len(rm.groups()):
				return i[1](rm.groups()[0])
			else:
				return i[1]()

def blog_html(id_):
	dic = {}
	html = open_file('blog.html')
	post_name, post_text = blog_page(id_)
	dic['post_name'] = post_name
	dic['post_text'] = post_text
	html = render_template(html, dic)
	return html, "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

def blog_index_html():
	html = ''
	posts = blog_index()
	print posts
	for i in posts:
		html += "<a href='http://localhost:8888/blog/%s'><p>%s</p></a>\n" % (i[0],i[1])
	return html, "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"

def render_template(html, dic):
  for i in dic:
	html = html.replace('###%s###' % i,  dic[i])
  return html

def run_server():

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

	url = return_url(request)

	if url == '/favicon.ico':
	  continue

	html, header = urlpatterns(url)
  
	http_response = "%s%s" % (header, html) #This hould work!!!

	client_connection.sendall(http_response) #We are not putting header as works fine
	client_connection.close()

run_server()


