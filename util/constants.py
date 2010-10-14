import os

class Constants (object):
    HTML_DIR = os.sep.join([os.path.abspath(os.path.dirname(__file__)), '../pcsmobile/render/html/']);
    API_HOST = 'localhost:8080'
