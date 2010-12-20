from pcsmobile.handle.wsgi._times import _BaseTimeHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring
from util.TimeZone import to_isostring

class ModifyReservationHandler (_BaseTimeHandler):

    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(ModifyReservationHandler, self).__init__()
        self.__const = constants
        self.__fetch = fetcher.fetch_json
        self.__render = renderer.render
    
    def _clean_fetched_data(self, json_data):
        allowed_error_codes = ()
        
        if self._is_error(json_data):
            if json_data['error']['code'] in allowed_error_codes:
                # Handle the errors
                pass
            
            # All other errors should just be sent to the default handler.
            else:
                return json_data
        
        res = json_data['reservation']
        
        # convert the old times as well, unless the old times don't exist yet;
        # in that case, copy them from the current times.
        old_start = res.get('old_start_time', res['start_time'])
        old_end   = res.get('old_end_time', res['end_time'])
        res['old_start_time'] = from_isostring(old_start)
        res['old_end_time']   = from_isostring(old_end)
        
        # convert all iso to datetime
        res_start = res['start_time']
        res_end   = res['end_time']
        res['start_time'] = from_isostring(res_start)
        res['end_time']   = from_isostring(res_end)
        
        return json_data
    
    def _build_chooser_queries(self, reservation_json, status):
        res = reservation_json['reservation']
        
        cur_start = to_isostring(res['start_time'])
        cur_end = to_isostring(res['end_time'])
        old_start = to_isostring(res['old_start_time'])
        old_end = to_isostring(res['old_end_time'])
        
        queries = {}
        queries['choose_start_time_query'] = \
            self._construct_chooser_query('start_time',
                cur_start,
                { 'reservation' : res['liveid'],
                  'vehicle' : res['vehicle']['id'],
                  'vehicle_model' : res['vehicle']['model']['name'],
                  'vehicle_pod' : res['vehicle']['pod']['name'],
                  'memo' : res['memo'],
                  'end_time' : cur_end,
                  'status' : status,
                  'old_start_time' : old_start,
                  'old_end_time' : old_end })
        
        queries['choose_end_time_query'] = \
            self._construct_chooser_query('end_time',
                cur_end,
                { 'reservation' : res['liveid'],
                  'start_time' : cur_start,
                  'vehicle' : res['vehicle']['id'],
                  'vehicle_model' : res['vehicle']['model']['name'],
                  'vehicle_pod' : res['vehicle']['pod']['name'],
                  'memo' : res['memo'],
                  'status' : status,
                  'old_start_time' : old_start,
                  'old_end_time' : old_end })
        
        return queries
    
    def _get_rendered_response(self):
        # initialize parameters to send to api
        resid = self._get_param('reservation') or \
            None
        vehid = self._get_param('vehicle') or \
            None
        vehmodel = self._get_param('vehicle_model') or \
            None
        vehpod = self._get_param('vehicle_pod') or \
            None
        start_iso = self._get_param('start_time') or \
            self._build_time_param('start_time') or \
            None
        old_start_iso = self._get_param('old_start_time') or \
            None
        end_iso = self._get_param('end_time') or \
            self._build_time_param('end_time') or \
            None
        old_end_iso = self._get_param('old_end_time') or \
            None
        memo = self._get_param('memo') or \
            None
        status = self._get_param('status') or \
            None
        
        if None in (resid, vehid, vehmodel, vehpod, start_iso, old_start_iso, end_iso, old_end_iso, memo):
            # Only send start and end time if they are not None.  If we leave them 
            # out, the server will just use the default time.
            params = {}
            if start_iso: params['start_time'] = start_iso
            if end_iso: params['end_time'] = end_iso
            
            reservation_json, headers = self.__fetch(
                ''.join(['http://', self.__const.API_HOST, '/reservations/', resid, '.json']),
                'GET', 
                params,
                self._package_cookies()
            );
        else:
            reservation_json = {
                'reservation' : {
                    'liveid' : resid,
                    'vehicle' : {
                        'id' : vehid,
                        'model' : {
                            'name' : vehmodel
                        },
                        'pod' : {
                            'name' : vehpod
                        },
                    },
                    'start_time' : start_iso,
                    'end_time' : end_iso,
                    'old_start_time' : old_start_iso,
                    'old_end_time' : old_end_iso,
                    'memo' : memo
                }
            }
            headers = {}
        
        reservation_json = \
            self._clean_fetched_data(reservation_json)
        
        values = reservation_json
        if not self._is_error(reservation_json):
            values.update(
                self._build_chooser_queries(reservation_json, status))
        
        status_map = {'0':'current','1':'upcoming','2':'past'}
        values['status'] = status_map[status]
        def _ceil_time(dt):
            minutes = dt.minute % 15
            delta_minutes = 15 - minutes
            
            if delta_minutes == 15 and dt.second == 0:
                return dt
            else:
                import datetime
                delta = datetime.timedelta(minutes=delta_minutes)
                ceil_time = dt.replace(second=0) + delta
                
                return ceil_time
            
        values['soonest_end_time'] = _ceil_time(current_time())
        content = self.__render('modify_reservation.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


