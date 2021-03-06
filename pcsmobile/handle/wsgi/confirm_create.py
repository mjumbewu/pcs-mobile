from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring
from util.TimeZone import to_isostring

class ConfirmReservationHandler (_BaseHandler):
    
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(ConfirmReservationHandler, self).__init__()
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
        
        conf = json_data['confirmation']
        
        # convert all iso to datetime
        res_start = conf['reservation']['start_time']
        res_end   = conf['reservation']['end_time']
        conf['reservation']['start_time'] = from_isostring(res_start)
        conf['reservation']['end_time']   = from_isostring(res_end)
        
        return json_data
    
    def _get_rendered_response(self):
        # initialize parameters to send to api
        vehid = self._get_param('vehicle') or \
            None
        start_iso = self._get_param('start_time') or \
            None
        end_iso = self._get_param('end_time') or \
            None
        memo = self._get_param('memo') or \
            None
        
        params = {}
        params['start_time'] = start_iso
        params['end_time'] = end_iso
        params['vehicle'] = vehid
        params['memo'] = memo
        
        res_confirmation_json, headers = self.__fetch(
            ''.join(['http://', self.__const.API_HOST, '/reservations.json']),
            'POST', 
            params,
            self._package_cookies()
        );
        
        res_confirmation_json = \
            self._clean_fetched_data(res_confirmation_json, None)
        
        values = res_confirmation_json
        
        if not self._is_error(res_confirmation_json):
            content = self._redirect_to('reservation_info', {
                'reservation': res_confirmation_json['confirmation']['reservation']['liveid'],
                'event': 'created'
            })
        else:
            content = self.__render('error_catcher.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


