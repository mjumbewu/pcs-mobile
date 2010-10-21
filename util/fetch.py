import urllib
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from google.appengine.api import urlfetch

class Fetcher (object):
    def fetch(self, url, method='GET', params={}, headers={}):
        method_map = {
            'GET' : urlfetch.GET,
            'POST' : urlfetch.POST,
            'PUT' : urlfetch.PUT,
            'DELETE' : urlfetch.DELETE,
            'HEAD' : urlfetch.HEAD
        }
        method = method_map.get(method);
        
        query = urllib.urlencode(params)
        if method == urlfetch.GET:
            connector = '&' if '?' in url else '?'
            url = connector.join([url, query])
            query = ''
        
        result = urlfetch.fetch(
            url=url,
            method=method,
            payload=query,
            headers=headers,
            deadline=10);
        
        return (result.content, result.headers)
    
    def fetch_json(self, url, method='GET', params={}, headers={}):
        content, head = self.fetch(url, method, params, headers)
        
        try:
            data = json.loads(content)
        except ValueError, ve:
            raise ValueError('%s from %r' % (ve.message, content))
        return (data, head)
