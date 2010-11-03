from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring

class _BaseTimeHandler (_BaseHandler):
    def __init__(self):
        super(_BaseTimeHandler, self).__init__()
    
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
    

