from pcsmobile.handle.wsgi._times import _BaseTimeHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring
from util.TimeZone import to_isostring

class NewReservationHandler (_BaseTimeHandler):
    """Despite its name, the ChooseVehicleHandler is not a chooser.
    (i.e., _chooser._BaseChooseHandler)"""
    
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(NewReservationHandler, self).__init__()
        self.__const = constants
        self.__fetch = fetcher.fetch_json
        self.__render = renderer.render
    
    def _clean_fetched_data(self, vehicle_availability_json, vehid, vehmodel, vehpod, start_iso, end_iso):
        if self._is_error(vehicle_availability_json):
#            # There are a couple of errors that we'll let through...
#            if vehicle_availability_json['error']['code'] in (
#                'start_time_in_past', 'end_time_earlier_than_start'):
#                
#                lajson = {'location_availability':{
#                    'start_time': start_iso,
#                    'end_time': end_iso,
#                    'location': {
#                        'name': locname,
#                        'id': locid
#                    },
#                    'vehicle_availabilities': []
#                },
#                'alert':
#                    location_availability_json['error']['msg']
#                }
#                
#                location_availability_json = lajson
#            
#            # All other errors should just be sent to the default handler.
#            else:
                return vehicle_availability_json
        
        veh_avail = vehicle_availability_json['vehicle_availability']
        
        # convert all iso to datetime
        avail_start = veh_avail['start_time']
        avail_end   = veh_avail['end_time']
        veh_avail['start_time'] = from_isostring(avail_start)
        veh_avail['end_time']   = from_isostring(avail_end)
        
        return vehicle_availability_json
    
#    def _build_chooser_queries(self, vehicle_availability_json):
#        veh_avail = vehicle_availability_json['location_availability']
#        
#        cur_start = to_isostring(veh_avail['start_time'])
#        cur_end = to_isostring(veh_avail['end_time'])
#        
#        queries = {}
#        queries['choose_location_query'] = \
#            self._construct_chooser_query('location',
#                loc_avail['location']['id'],
#                { 'start_time' : cur_start,
#                  'end_time' : cur_end })
#        
#        queries['choose_start_time_query'] = \
#            self._construct_chooser_query('start_time',
#                cur_start,
#                { 'location' : loc_avail['location']['id'],
#                  'location_name' : loc_avail['location']['name'],
#                  'end_time' : cur_end })
#        
#        queries['choose_end_time_query'] = \
#            self._construct_chooser_query('end_time',
#                cur_end,
#                { 'start_time' : cur_start,
#                  'location_name' : loc_avail['location']['name'],
#                  'location' : loc_avail['location']['id'] })
#        
#        return queries
    
    def _get_rendered_response(self):
        # initialize parameters to send to api
        vehid = self._get_param('vehicle') or \
            '[Vehicle ID]'
        vehmodel = self._get_param('vehicle_model') or \
            '[Vehicle Model]'
        vehpod = self._get_param('vehicle_pod') or \
            '[Vehicle Pod]'
        start_iso = self._get_param('start_time') or \
            self._build_time_param('start_time') or \
            None
        end_iso = self._get_param('end_time') or \
            self._build_time_param('end_time') or \
            None
        
        # Only send start and end time if they are not None.  If we leave them 
        # out, the server will just use the default time.
        params = {}
        if start_iso: params['start_time'] = start_iso
        if end_iso: params['end_time'] = end_iso
        
        vehicle_availability_json, headers = self.__fetch(
            ''.join(['http://', self.__const.API_HOST, '/vehicles/', vehid, '/availability.json']),
            'GET', 
            params,
            self._package_cookies()
        );
        
        vehicle_availability_json = \
            self._clean_fetched_data(vehicle_availability_json,
                vehid, vehmodel, vehpod, start_iso, end_iso)
        
        values = vehicle_availability_json
        values['return_url'] = self._get_param('return_url')
#        if not self._is_error(vehicle_availability_json):
#            values.update(
#                self._build_chooser_queries(vehicle_availability_json))
        
        content = self.__render('new_reservation.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


