from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring

class ChooseVehicleHandler (_BaseHandler):
    """Despite its name, the ChooseVehicleHandler is not a chooser.
    (i.e., _chooser._BaseChooseHandler)"""
    
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(ChooseVehicleHandler, self).__init__()
        self.__const = constants
        self.__fetch = fetcher.fetch_json
        self.__render = renderer.render
    
    def _build_time_param(self, param):
        """Get an ISO 8601 time string from the choose datetime interface."""
        year = self._get_param('%s_year' % param)
        month = self._get_param('%s_month' % param)
        day = self._get_param('%s_day' % param)
        hour = self._get_param('%s_hour' % param)
        minute = self._get_param('%s_minute' % param)
        midi = self._get_param('%s_midi' % param)
        
        if None in (year, month, day, hour, minute, midi):
            return None
        
        year = int(year)
        month = int(month)
        day = int(day)
        hour = int(hour)
        minute = int(minute)
        
        hour = (0 if hour == 12 else hour)
        hour += (12 if midi == 'PM' else 0)
        
        iso_time = '%d-%02d-%02dT%02d:%02d' % (year, month, day, hour, minute)
        return iso_time
    
    def _clean_fetched_data(self, location_availability_json, locname, locid, start_iso, end_iso):
        if self._is_error(location_availability_json):
            # There are a couple of errors that we'll let through...
            if location_availability_json['error']['code'] in (
                'start_time_in_past', 'end_time_earlier_than_start'):
                
                lajson = {'location_availability':{
                    'start_time': start_iso,
                    'end_time': end_iso,
                    'location': {
                        'name': locname,
                        'id': locid
                    },
                    'vehicle_availabilities': []
                },
                'alert':
                    location_availability_json['error']['msg']
                }
                
                location_availability_json = lajson
            
            # All other errors should just be sent to the default handler.
            else:
                return location_availability_json
        
        loc_avail = location_availability_json['location_availability']
        
        # convert all iso to datetime
        avail_start = loc_avail['start_time']
        avail_end   = loc_avail['end_time']
        loc_avail['start_time'] = from_isostring(avail_start)
        loc_avail['end_time']   = from_isostring(avail_end)
        
        for veh_avail in loc_avail['vehicle_availabilities']:
            earliest = veh_avail.get('earliest', None)
            latest = veh_avail.get('latest', None)
            if earliest: veh_avail['earliest'] = from_isostring(earliest)
            if latest:   veh_avail['latest']   = from_isostring(latest)
        
        return location_availability_json
    
    def _build_chooser_queries(self, location_availability_json):
        loc_avail = location_availability_json['location_availability']
        
        cur_start = loc_avail['start_time'].strftime('%Y-%m-%dT%H:%M')
        cur_end = loc_avail['end_time'].strftime('%Y-%m-%dT%H:%M')
        
        queries = {}
        queries['choose_location_query'] = \
            self._construct_chooser_query('location',
                loc_avail['location']['id'],
                { 'start_time' : cur_start,
                  'end_time' : cur_end })
        
        queries['choose_start_time_query'] = \
            self._construct_chooser_query('start_time',
                cur_start,
                { 'location' : loc_avail['location']['id'],
                  'location_name' : loc_avail['location']['name'],
                  'end_time' : cur_end })
        
        queries['choose_end_time_query'] = \
            self._construct_chooser_query('end_time',
                cur_end,
                { 'start_time' : cur_start,
                  'location_name' : loc_avail['location']['name'],
                  'location' : loc_avail['location']['id'] })
        
        return queries
    
    def _get_rendered_response(self):
        # initialize parameters to send to api
        locid = self._get_param('location') or \
            '_default'
        locname = self._get_param('location_name') or \
            'Default'
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
        
        location_availability_json, headers = self.__fetch(
            ''.join(['http://', self.__const.API_HOST, '/locations/', locid, '/availability.json']),
            'GET', 
            params,
            self._package_cookies()
        );
        
        location_availability_json = \
            self._clean_fetched_data(location_availability_json,
                locname, locid, start_iso, end_iso)
        
        values = location_availability_json
        if not self._is_error(location_availability_json):
            values.update(
                self._build_chooser_queries(location_availability_json))
        values['reflect_url'] = self._construct_reflect_path()
        
        content = self.__render('choose_vehicle.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


