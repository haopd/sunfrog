# -*- coding: utf-8 -*-
import logging
import endpoints

__author__ = 'haopd'
_logger = logging.getLogger(__name__)


import sunApi

ENDPOINTS_API_SERVER = endpoints.api_server([
    sunApi.SunApi
])
