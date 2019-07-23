import sys
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)
    sys.path.append(os.path.join(BASE_DIR, 'crawler'))
from WebCrawler import settings
from lxml import etree
import requests
import json

log = settings.log


class Web:
    def __init__(self, url):
        pass
