from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring

class CancelReservationHandler (_BaseHandler):
    def __init__(self, constants = Constants(), renderer = Renderer()):
        super(CancelReservationHandler, self).__init__()
        self.__const = constants
        self.__render = renderer.render
    
    def _get_rendered_response(self):
        values, headers = self._get_params(), {}
        
        content = self.__render('cancel_reservation.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


