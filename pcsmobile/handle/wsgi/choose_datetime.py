from pcsmobile.handle.wsgi._chooser import _BaseChooseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring

class ChooseDateTimeHandler (_BaseChooseHandler):
    def __init__(self, constants = Constants(), fetcher = Fetcher(), renderer = Renderer()):
        super(ChooseDateTimeHandler, self).__init__()
        self.__const = constants
        self.__render = renderer.render
    
    def _get_rendered_response(self):
        values = self._build_chooser_values()
        
        headers = {}
        
        current_iso = self._get_param('current_value')
        current_dt = from_isostring(current_iso)
        
        values['current_year'] = '%d' % current_dt.year
        values['current_month'] = current_dt.month
        values['current_day'] = '%d' % current_dt.day
        values['current_hour'] = '%02d' % (current_dt.hour%12 or 12)
        values['current_minute'] = '%02d' % current_dt.minute
        values['current_midi'] = 'AM' if current_dt.hour < 12 else 'PM'
        
        values['years'] = ['%d' % year for year in xrange(current_dt.year, current_dt.year+3)]
        values['months'] = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        values['days'] = ['%d' % (day+1) for day in xrange(31)]
        values['hours'] = ['%02d' % (hour+1) for hour in xrange(12)]
        values['minutes'] = ['%02d' % minute for minute in xrange(0,60,15)]
        values['midis'] = ['AM', 'PM']
        
        values.update(self._get_params())
        
        content = self.__render('choose_datetime.html', values)
        
        return content, headers
    
    def get(self):
        self._handle()


