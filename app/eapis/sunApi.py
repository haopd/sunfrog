# -*- coding: utf-8 -*-
import json
import urllib
from bs4 import BeautifulSoup
import logging
import endpoints
from protorpc import messages, message_types, remote
from google.appengine.api import taskqueue
from google.appengine.ext import ndb

__author__ = 'haopd'
_logger = logging.getLogger(__name__)


class DataSheets(ndb.Model):
    data = ndb.TextProperty()
    time_create = ndb.DateTimeProperty(auto_now=True)


class DataRequest(messages.Message):
    data = messages.StringField(1)


@endpoints.api(name='change_url', version='v1')
class SunApi(remote.Service):
    """ URL API
    """
    @endpoints.method(
        DataRequest,
        message_types.VoidMessage,
        name='sunapi',)
    def receive_data(self, request):
        obj_ndb = DataSheets()
        obj_ndb.data = request.data
        obj_ndb.put()
        taskqueue.add(url='/taskqueue/upload-sheets', queue_name='upload-data-sheets', method='POST',
                      params={'id': obj_ndb.key.id() })
        return message_types.VoidMessage()
