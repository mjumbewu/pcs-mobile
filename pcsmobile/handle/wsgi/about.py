from pcsmobile.handle.wsgi._chooser import _BaseChooseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

class AboutHandler (_BaseChooseHandler):
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(AboutHandler, self).__init__()
        self.__const = constants
        self.__render = renderer.render
    
    def _get_rendered_response(self):
        values = {}
        headers = {}
        
        values.update(self._get_params())
        
        content = self.__render('about.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


