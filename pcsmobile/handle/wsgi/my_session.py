import httplib
import urllib
import Cookie as cookielib
import HTMLParser as htmlparserlib
import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext.webapp.util import run_wsgi_app

from util.constants import Constants
from util.fetch import Fetcher

class MySessionHandler (webapp.RequestHandler):
    def __init__(self, constants = Constants(), fetcher = Fetcher()):
        super(MySessionHandler, self).__init__()
        
        self.__const = constants
        self.__fetch = fetcher.fetch_json
    
    def __get_param(self, param):
        value = self.request.get(param)
        return value
    
    def __get_userid(self):
        userid = self.__get_param('user')
        return userid
    
    def __get_password(self):
        password = self.__get_param('password')
        return password
    
    def post(self):
        userid = self.__get_userid()
        password = self.__get_password()
        
        values, headers = self.__fetch(
            ''.join(['http://', self.__const.API_HOST, '/session.json']),
            'POST', 
            {
              'user' : userid,
              'password' : password
            }
        );
        
#        self.response.out.write(repr(values));
#        self.response.out.write(userid + ' ');
#        self.response.out.write(password + ' ');
#        self.response.out.write(os.path.join(self.__const.HTML_DIR, 'my_session.html'))
        
        path = os.path.join(self.__const.HTML_DIR, 'my_session.html')
        response_body = template.render(path, values)
        
        self.response.out.write(response_body);
        self.response.set_status(200);


application = webapp.WSGIApplication(
        [('/my_session', MySessionHandler)],
        debug=True)

def main():
    run_wsgi_app(application)

if __name__ == '__main__':
    main()
