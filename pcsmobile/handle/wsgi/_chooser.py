from pcsmobile.handle.wsgi._base import _BaseHandler
from util.constants import Constants
from util.fetch import Fetcher
from util.render import Renderer

from util.TimeZone import current_time
from util.TimeZone import from_isostring

class _BaseChooseHandler (_BaseHandler):
    def __init__(self):
        super(_BaseChooseHandler, self).__init__()
    
    def _build_chooser_values(self):
        """Get a dictionary of values that every chooser uses."""
        values = {}
        
        values['return_url'] = self._get_param('return_url')
        values['return_param'] = self._get_param('return_param')
        values['current_value'] = self._get_param('current_value')
        
        reflect_params = [
            [arg[8:], value]
            for arg, value in self._get_params().items()
            if arg.startswith('reflect_')]
        values['reflect_params'] = reflect_params
        
        return values

