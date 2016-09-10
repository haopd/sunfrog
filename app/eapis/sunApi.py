# -*- coding: utf-8 -*-
import json
import urllib
from bs4 import BeautifulSoup
import logging
import endpoints
from protorpc import messages, message_types, remote
from google.appengine.api import taskqueue

__author__ = 'haopd'
_logger = logging.getLogger(__name__)


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
        logging.info(request.data)
        taskqueue.add(url='/taskqueue/upload-sheets', queue_name='upload-data-sheets', method='POST',
                      params={'data': request.data})
        return message_types.VoidMessage()
