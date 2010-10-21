import os

from google.appengine.ext.webapp import template

from util.constants import Constants

class Renderer (object):
    def __init__(self, const=Constants()):
        self.__const = const
    
    def render(self, template_name, values):
        path = os.path.join(self.__const.HTML_DIR, template_name)
        content = template.render(path, values)
        return content
