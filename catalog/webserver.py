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
                    output += "<h2>"
                    output += restaurant.name
                    output += "</h2>"
                    output += "<a href = '/restaurant/%s/edit'>Edit</a>" % restaurant.id
                    output += "</br>"
                    output += "<a href = '/delete'>Delete</a>"
                    output += "</br>"
                output += "</br><a href = '/restaurant/new'>Make a New Restaurant Here</a>"
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

            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                #output += "<h2>Make a New Restaurant</h2>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurant/new'><h2>Make a New Restaurant</h2><input name="newRestaurant" type="text" ><input type="submit" value="Create"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return  #exits the if statment

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                restaurantEdit = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if restaurantEdit != [] :
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body><h2>"
                    output += restaurantEdit.name
                    output += "</h2>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/edit'>" %restaurantIDPath
                    output += '''<input name="newRestaurant" type="text" ><input type="submit" value="Rename"> </form>'''
                    output += "</body></html>"
                    self.wfile.write(output)
                    print output
                    return  #exits the if statment

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                restaurantDelete = session.query(Restaurant).filter_by(id = restaurantIDPath).one()
                if restaurantEdit != [] :
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()

                    output = ""
                    output += "<html><body><h2>"
                    output += "Are you sure you want to delete "
                    output += restaurantDelete.name
                    output += "</h2>"
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurant/%s/delete'>" %restaurantIDPath
                    output += '''<input name="deleteRestaurant" type="button" ><input type="submit" value="Delete"> </form>'''
                    output += "</body></html>"
                    self.wfile.write(output)
                    return


        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurant')
                    restaurantIDPath = self.path.split("/")[2]

                    restaurantEdit = session.query(Restaurant).filter_by(
                        id=restaurantIDPath).one()
                    if restaurantEdit != []:
                        restaurantEdit.name = messagecontent[0]
                        session.add(restaurantEdit)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurant')
                        self.end_headers()

            if self.path.endswith("/restaurant/new"):

                ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
                # parses a html form header such as content type into a main value and dictionary
                # of paramaters
                if ctype == 'multipart/form-data': # check if this if form data being received
                    fields=cgi.parse_multipart(self.rfile, pdict) # then make variable fields, and use parse.multipart which will collect all the fields in a form
                    #messagecontent = fields.get('message') # to get out the value of a specfic field or set of fields and store them in an anrray
                    newRestaurant = fields.get('newRestaurant')
                    # call this field 'message' here and when create html form.

                    #So now that I've received a post request I can decide what to tell the client with the new information I've received.
                    restaurant1 = Restaurant(name= newRestaurant[0])

                    session.add(restaurant1)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()

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