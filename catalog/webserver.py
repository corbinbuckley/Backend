import sys

from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi

from database_setup import Restaurant, Base, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:

            if self.path.endswith("/restaurant"):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Local Restaurants: </br>"
                for restaurant in restaurants:
                    output += "<html><body>"
                    output += "<h2>"
                    output += restaurant.name
                    output += "</h2>"
                    output += "<a hfref = '/edit'>Edit</a></br>"
                    output += "<a hfref = '/delete'>Delete</a>"
                    output += "</br>"
                    output += "</body></html>"
                output += "</body></html>"
                self.wfile.write(output)
                return
            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161Hola <a href = '/hello'> Back to Hello</a>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return  #exits the if statment

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.end_headers()

            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            # parses a html form header such as content type into a main value and dictionary
            # of paramaters
            if ctype == 'multipart/form-data': # check if this if form data being received
                fields=cgi.parse_multipart(self.rfile, pdict) # then make variable fields, and use parse.multipart which will collect all the fields in a form
                messagecontent = fields.get('message') # to get out the value of a specfic field or set of fields and store them in an anrray
                # call this field 'message' here and when create html form.

                #So now that I've received a post request I can decide what to tell the client with the new information I've received.
            output = ""
            output += "<html><body>"
            output += "<h2> Okay, how about this: </h2>"
            output += "<h1> %s</h1>" % messagecontent[0] #return the first value of the array when submited the form
            output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
            output += "</body></html>"
            self.wfile.write(output)
            print output

        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webserverHandler)
        print "Web server running on port %s" % port
        server.serve_forever()


    except KeyboardInterrupt:
        print "^C entered, stopping web server..."
        server.socket.close()


if __name__ == '__main__':
    main()