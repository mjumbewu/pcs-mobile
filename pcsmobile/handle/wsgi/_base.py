from google.appengine.ext import webapp

class _BaseHandler (webapp.RequestHandler):
    def _is_error(self, json_doc):
        return 'error' in json_doc
    
    def _not_error(self, json_doc):
        return 'error' not in json_doc
    
    def _get_param(self, param):
        value = self.request.get(param, None)
        return value
    
    def _get_cookie(self, cookie):
        value = self.request.cookies.get(cookie, None)
        return value
    
    def _get_params(self):
        """Get a dictionary of all the parameters sent to the site."""
        params = {}
        for param in self.request.arguments():
            params[param] = self.request.get(param)
        return params
    
    def _package_cookies(self):
        """Prepare the cookies for sending to another location.  Useful for
        forwarding the cookies to the API."""
        cookies = '; '.join([
            '%s=%s' % (name,value)
            for name, value in self.request.cookies.items()])
        return {'Cookie':cookies}
    
    def _get_headers(self):
        """Get a dictionary of all the headers sent to the site."""
        headers = self.request.headers
        return headers
    
    def _set_response_cookies(self, cookies, expires=None):
        if expires is None:
            import datetime as dt
            expire_dt = dt.datetime.now() + dt.timedelta(minutes=15)
            expires = expire_dt.strftime('%a, %d-%b-%Y %H:%M:%S GMT')
        
        for (cookie, value) in cookies.items():
            cookies_str = '%s=%s; expires=%s;' % (cookie, value, expires)
            self._set_response_headers({'Set-Cookie':cookies_str})
    
    def _set_response_headers(self, headers):
        for (header, value) in headers.items():
            self.response.headers.add_header(header, value)
    
    def _set_response_content(self, content):
        self.response.out.write(content);
        self.response.set_status(200);
    
    def _construct_reflect_path(self):
        """Create a return path that you can pass to other screens."""
        reflect_path = '?'.join([self.request.path, self.request.query_string])
        return reflect_path
    
    def _construct_chooser_query(self, return_arg, current_value=None, reflect_params = {}):
        """Create a query string for sending to a chooser (e.g., the location
        or datetime chooser)."""
        import urllib
        
        reflect_path = self._construct_reflect_path()
        #reflect_query = urllib.urlencode(reflect_params)
        query = {
            'current_value' : current_value,
            'return_param' : return_arg,
            'return_url' : reflect_path
        }
        
        for arg, value in reflect_params.items():
            query['reflect_%s' % arg] = value
        
        return urllib.urlencode(query)
    
    def _get_rendered_response(self):
        raise NotImplementedError()
    
    def _handle(self):
        content, headers = self._get_rendered_response()
        
        self._set_response_headers(headers)
        self._set_response_content(content)

