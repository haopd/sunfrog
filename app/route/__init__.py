# -*- coding: utf-8 -*-
import logging
import webapp2
import app

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class ViewUrlHandler(app.BaseRequestHandler):
    def get(self):
        return self.render_template('frontend/view.j2')


class AddUrlHandler(app.BaseRequestHandler):
    def get(self):
        return self.render_template('frontend/add.j2')


class MainHandler(app.BaseRequestHandler):
    def get(self):
        self.render_template('/frontend/index.j2')


webapp2_routes = [
    webapp2.Route('/', handler=MainHandler, name='home'),
    webapp2.Route(r'/url', name='url/view', handler=ViewUrlHandler),
    webapp2.Route(r'/url/add', name='url/add', handler=AddUrlHandler),
]