# -*- coding: utf-8 -*-
import logging
import datetime
import json
__author__ = 'datpt'
_logger = logging.getLogger(__name__)


def json_encode(data):

    def _json_encoder_default(o):

        if isinstance(o, datetime.datetime):
            return o.isoformat()

        if isinstance(o, datetime.date):
            return o.isoformat()

        if hasattr(o, '__json__'):
            return o.__json__


        raise TypeError('Can not jsonize "%s"' % type(o))

    return json.dumps(data, default=_json_encoder_default)