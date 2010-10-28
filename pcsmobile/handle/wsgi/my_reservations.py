from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring

class MyReservationsHandler (_BaseHandler):
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(MyReservationsHandler, self).__init__()
        self.__const = constants
        self.__fetch = fetcher.fetch_json
        self.__render = renderer.render
    
    def _get_params(self):
        params = {}
        for param in self.request.arguments():
            params[param] = self.request.get(param)
        return params
    
    def _get_rendered_response(self):
        values, headers = self.__fetch(
            ''.join(['http://', self.__const.API_HOST, '/reservations.json']),
            'GET', 
            self._get_params(),
            self._get_headers()
        );
        
        period_str = self._get_param('period')
        selected_period = from_isostring(period_str) if period_str else None
        
        NUM_PERIODS = 3
        from datetime import timedelta
        
        current_period = current_time()
        periods = [current_period]
        for x in range(1, NUM_PERIODS):
            current_period = current_period - timedelta(days=28)
            periods.append(current_period)
        
        values['periods'] = periods
        values['selected_period'] = selected_period
        
        STATUS_CURRENT  = 0
        STATUS_UPCOMING = 1
        STATUS_PAST     = 2
        
        res_list = values.get('reservation_list', None)
        if res_list:
            reservations = res_list['reservations']
            for reservation in reservations:
                now = current_time()
                start_time = from_isostring(reservation['start_time'])
                end_time = from_isostring(reservation['end_time'])
                
                reservation['start_time'] = start_time
                reservation['end_time'] = end_time
                if start_time > now:
                    reservation['status'] = STATUS_UPCOMING
                elif end_time > now:
                    reservation['status'] = STATUS_CURRENT
                else:
                    reservation['status'] = STATUS_PAST
            
            if period_str == '':
                reservations.sort(key=lambda r: r['status'])
        
        content = self.__render('my_reservations.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


