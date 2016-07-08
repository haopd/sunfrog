# -*- coding: utf-8 -*-
import logging
import webapp2
import app
from webapp2_extras import routes

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class MainHandler(app.BaseRequestHandler):
    def get(self):
        self.render_template('')


webapp2_routes = [
    routes.PathPrefixRoute('/hq', [
        webapp2.Route(r'/', handler=MainHandler, name='log-home'),
    ]),
]