from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

from pcsmobile.handle.wsgi.index import IndexHandler
from pcsmobile.handle.wsgi.my_session import MySessionHandler
from pcsmobile.handle.wsgi.my_reservations import MyReservationsHandler

application = webapp.WSGIApplication(
        [('/my_reservations', MyReservationsHandler),
         ('/my_session', MySessionHandler),
         ('/login', IndexHandler),
         ('/index.html', IndexHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
