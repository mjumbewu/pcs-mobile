from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring

class ConfirmCancellationHandler (_BaseHandler):
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(ConfirmCancellationHandler, self).__init__()
        self.__const = constants
        self.__fetch = fetcher.fetch_json
        self.__render = renderer.render
    
    def _get_rendered_response(self):
        params = self._get_params()
        resid = self._get_param(reservation)
        
        values, headers = self.__fetch(
            ''.join(['http://', self.__const.API_HOST, '/reservation/', resid, '.json']),
            'DELETE', 
            self._get_params(),
            self._get_headers()
        );
        
        content = self.__render('confirm_cancel.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


