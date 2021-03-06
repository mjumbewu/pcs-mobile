from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring
from util.TimeZone import to_isostring

class CancelReservationHandler (_BaseHandler):
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(CancelReservationHandler, self).__init__()
        self.__const = constants
        self.__fetch = fetcher.fetch_json
        self.__render = renderer.render
    
    def _clean_fetched_data(self, json_data, defaults):
        allowed_error_codes = ()
        
        if self._is_error(json_data):
            if json_data['error']['code'] in allowed_error_codes:
                # Handle the errors
                pass
            
            # All other errors should just be sent to the default handler.
            else:
                return json_data
        
        res = json_data['reservation']
        
        # convert all iso to datetime
        res_start = res['start_time']
        res_end   = res['end_time']
        res['start_time'] = from_isostring(res_start)
        res['end_time']   = from_isostring(res_end)
        
        return json_data
    
    def _get_rendered_response(self):
        # initialize parameters to send to api
        res_liveid = self._get_param('reservation') or \
            None
        
        params = {}
        
        reservation_json, headers = self.__fetch(
            ''.join(['http://', self.__const.API_HOST, '/reservations/', res_liveid, '.json']),
            'GET', 
            params,
            self._package_cookies()
        );
        
        reservation_json = \
            self._clean_fetched_data(reservation_json, None)
        
        values = reservation_json
        
        content = self.__render('cancel_reservation.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


