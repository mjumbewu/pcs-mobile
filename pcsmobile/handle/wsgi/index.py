from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.render import Renderer

class IndexHandler (_BaseHandler):
    def __init__(self, constants = Constants(), renderer = Renderer()):
        super(IndexHandler, self).__init__()
        self.__const = constants
        self.__render = renderer.render
    
    def _get_rendered_response(self):
        values = {}
        values['reflect_url'] = self._construct_reflect_path()
        content = self.__render('index.html', values)
        headers = {}
        
        return content, headers
    
    def get(self):
        self._handle()
