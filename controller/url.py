# -*- coding: utf-8 -*-
import logging
from controller import db

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


def is_url_existed(str_url):
    is_existed = db.Url.query().filter(db.Url.url_output == str_url).fetch()
    return bool(is_existed)