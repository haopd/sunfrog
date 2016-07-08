# -*- coding: utf-8 -*-
import logging
from google.appengine.ext import ndb

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class Url(ndb.Model):
    url_input = ndb.StringProperty(required=True)
    url_output = ndb.StringProperty(required=True)
    status = ndb.BooleanProperty(default=True)
    time_created = ndb.DateTimeProperty(auto_now_add=True)
    time_modify =ndb.DateTimeProperty(auto_now=True)
