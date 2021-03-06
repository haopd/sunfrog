# -*- coding: utf-8 -*-
import logging
import webapp2
import webapp2_extras
from webapp2_extras import auth
from webapp2_extras import jinja2,sessions
import helpers
import os

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class TransactionalRequestHandler(webapp2.RequestHandler):
    """ Quản lý việc commit hay rollback session sau khi xử lý 1 request
    """
    @webapp2.cached_property
    def jinja2(self):
        """
        Returns:
            jinja2.Jinja2
        """
        return jinja2.get_jinja2(app=self.app)

    def render_json(self, data):
        """ Render template rồi lưu kết quả vào Response
        Args:
            data: Dữ liệu trả về, có thể serialize được = json

        """
        self.response.write(helpers.json_encode(data))
        self.response.headers['content-type'] = 'application/json; charset=utf8'


class BaseRequestHandler(TransactionalRequestHandler):

    def initialize(self, request, response):
        super(BaseRequestHandler, self).initialize(request, response)
        self.session_store = webapp2_extras.sessions.get_store(request=self.request)
        """:type: webapp2_extras.sessions.SessionStore"""

    @webapp2.cached_property
    def session(self):
        """Shortcut to access the current session."""
        return self.session_store.get_session(backend="datastore")

    @webapp2.cached_property
    def auth(self):
        return auth.get_auth()

    @webapp2.cached_property
    def acc(self):
        acc_id = self.request.cookies.get('acc_id')
        acc = None
        # if acc_id:
        #     acc = db.Account.get_by_id(int(acc_id))
        return acc

    def render_template(self, _template, **context):
        """ Render template rồi lưu kết quả vào Response
        Args:
            _template (str):
            **context (dict):
        """
        context.setdefault('request', self.request)
        context.setdefault('session', self.session)
        rv = self.jinja2.render_template(_template, **context)
        self.response.write(rv)


import app.route

APP = webapp2.WSGIApplication(app.route.webapp2_routes, debug=True)
APP.config = webapp2.Config({
    'webapp2_extras.sessions': {
        'secret_key': 'YOUR_SECRET_KEY@1900100co',
    },
    'webapp2_extras.jinja2': {
        'template_path': os.path.join(
            os.path.dirname(__file__),
            'templates',
        ),
        'extensions': ['jinja2.ext.autoescape'],
        'globals': {
            'url_for': webapp2.uri_for,
            'uri_for': webapp2.uri_for,
        }
    },
})
