from pcsmobile.handle.wsgi._chooser import _BaseChooseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring

class ChooseLocationHandler (_BaseChooseHandler):
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(ChooseLocationHandler, self).__init__()
        self.__const = constants
        self.__fetch = fetcher.fetch_json
        self.__render = renderer.render
    
    def _get_rendered_response(self):
        values = self._build_chooser_values()
        
        locations_json, headers = self.__fetch(
            ''.join(['http://', self.__const.API_HOST, '/locations.json']),
            'GET', 
            {},
            self._package_cookies()
        );
        values.update(locations_json)
        
        content = self.__render('choose_location.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


