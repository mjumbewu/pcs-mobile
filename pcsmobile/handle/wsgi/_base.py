from google.appengine.ext import webapp

class _BaseHandler (webapp.RequestHandler):
    def _get_param(self, param):
        value = self.request.get(param)
        return value
    
    def _get_headers(self):
        headers = self.request.headers
        return headers
    
    def _set_response_headers(self, headers):
        for (header, value) in headers.items():
            self.response.headers.add_header(header, value)
    
    def _set_response_content(self, content):
        self.response.out.write(content);
        self.response.set_status(200);
    
    def _get_rendered_response(self):
        raise NotImplementedError()
    
    def _handle(self):
        content, headers = self._get_rendered_response()
        
        self._set_response_headers(headers)
        self._set_response_content(content)

