from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring
from util.TimeZone import to_isostring

RetryErrors = ()
try:
    # Try importing DownloadError.  Since the reservation change was in all 
    # likelihood successful before he download error, we want to add this to
    # the OK errors.
    from google.appengine.api.urlfetch import DownloadError
    RetryErrors += (DownloadError,)
except:
    pass

class ConfirmModificationHandler (_BaseHandler):
    
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(ConfirmModificationHandler, self).__init__()
        self.__const = constants
        self.__fetch = fetcher.fetch_json
        self.__render = renderer.render
    
    def _clean_fetched_data(self, json_data, **defaults):
        allowed_error_codes = ('no_change_requested',)
        
        if self._is_error(json_data):
            if json_data['error']['code'] in allowed_error_codes:
                json_data = {'confirmation' : {
                    'reservation' : {
                        'start_time' : to_isostring(defaults['start_time']),
                        'end_time' : to_isostring(defaults['end_time']),
                        'liveid' : defaults['liveid'] }
                }}
            
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
        resid = self._get_param('reservation') or \
            None
        vehid = self._get_param('vehicle') or \
            None
        start_iso = self._get_param('start_time') or \
            None
        end_iso = self._get_param('end_time') or \
            None
        old_start_iso = self._get_param('old_start_time') or \
            None
        old_end_iso = self._get_param('old_end_time') or \
            None
        memo = self._get_param('memo') or \
            None
        
        params = {}
        params['start_time'] = start_iso
        params['end_time'] = end_iso
        params['vehicle'] = vehid
        if memo is not None:
            params['memo'] = memo
        
        start_time = from_isostring(start_iso)
        end_time = from_isostring(end_iso)
        old_start_time = from_isostring(old_start_iso)
        old_end_time = from_isostring(old_end_iso)
        
        if current_time() > start_time:
            if old_end_time > end_time:
                params['action'] = 'early'
            else:
                params['action'] = 'extend'
        else:
            params['action'] = 'edit'
        
#        if start_time != old_start_time or end_time != old_end_time:
        try:
            res_confirmation_json, headers = self.__fetch(
                ''.join(['http://', self.__const.API_HOST, '/reservations/', resid, '.json']),
                'PUT', 
                params,
                self._package_cookies()
            );
        except RetryErrors:
            reservation_json, headers = self.__fetch(
                ''.join(['http://', self.__const.API_HOST, '/reservations/', resid, '.json']),
                'GET',
                params,
                self._package_cookies()
            );
            res_confirmation_json = {'confirmation':reservation_json};
            res_confirmation_json['confirmation'].update({'event':'modify'});
#        else:
#            res_confirmation_json = {'confirmation' : {
#                'reservation' : {
#                    'start_time' : to_isostring(start_time),
#                    'end_time' : to_isostring(end_time),
#                    'liveid' : resid }}}
#            headers = {}
        
        res_confirmation_json = \
            self._clean_fetched_data(res_confirmation_json, 
                start_time=start_time, 
                end_time=end_time, 
                liveid=resid)
        
        values = res_confirmation_json
        
        if not self._is_error(res_confirmation_json):
            content = self._redirect_to('reservation_info', {
                'reservation': res_confirmation_json['confirmation']['reservation']['liveid'],
                'event': 'updated'
            })
        else:
            content = self.__render('error_catcher.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


