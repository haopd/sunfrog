# -*- coding: utf-8 -*-
import logging
import webapp2
import webapp2_extras
from webapp2_extras import auth
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
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

    def dispatch(self):
        try:
            ret = super(BaseRequestHandler, self).dispatch()
            if not self.request.cookies.get('credentials'):
                self.redirect_to('login')
            return ret
        except:
            raise
        finally:
            self.session_store.save_sessions(self.response)


def _handle_404(request, response, exception):
    _logger.exception(exception)
    html = jinja2.get_jinja2().render_template('404.j2')
    response.status = 404
    response.write(html)


def _handle_500(request, response, exception):
    _logger.exception(exception)
    html = jinja2.get_jinja2().render_template('404.j2')
    response.status = 500
    response.write(html)


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
APP.error_handlers[404] = _handle_404
APP.error_handlers[500] = _handle_500