from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

class MySessionHandler (_BaseHandler):
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(MySessionHandler, self).__init__()
        self.__const = constants
        self.__fetch = fetcher.fetch_json
        self.__render = renderer.render
    
    def _get_params(self):
        params = {}
        for param in self.request.arguments():
            params[param] = self.request.get(param)
        return params
    
    def _get_rendered_response(self):
        values, headers = self.__fetch(
            ''.join(['http://', self.__const.API_HOST, '/session.json']),
            self.__method, 
            self._get_params(),
            self._get_headers()
        );
        
        content = self.__render('my_session.html', values)
        
        return content, headers
    
    def get(self):
        self.__method = 'GET'
        self._handle()
    
    def post(self):
        self.__method = 'POST'
        self._handle()


