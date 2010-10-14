import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

class IndexHandler (webapp.RequestHandler):
    def get(self):
        values = {}
        path = os.path.join(os.path.dirname(__file__), '../../render/html/index.html')
        response_body = template.render(path, values)
        
        self.response.out.write(response_body);
        self.response.set_status(200);


application = webapp.WSGIApplication(
        [('/login.html', IndexHandler),
         ('/index.html', IndexHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
