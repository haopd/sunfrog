# -*- coding: utf-8 -*-
import logging
import webapp2
import app
import formencode
from formencode import validators
from controller import db

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class AddUrlForm(formencode.Schema):
    allow_extra_fields = True

    url_input = validators.URL()
    url_output = validators.URL()


class ViewUrlHandler(app.BaseRequestHandler):
    def get(self):
        return self.render_template('frontend/view.j2')


class AddUrlHandler(app.BaseRequestHandler):
    def get(self):
        return self.render_template('frontend/add.j2', form_data=None, form_errors=None)

    def post(self):
        form_validate = AddUrlForm()
        form_errors = {}
        try:
            data = form_validate.to_python(self.request.POST)
            obj = db.Url()
            obj.url_input = data.get('url_input')
            obj.url_output = data.get('url_output')
            obj.status = True
            obj.put()
            self.session.add_flash('Success')
            return self.redirect_to('url/add')
        except formencode.Invalid as e:
            form_errors = e.error_dict
        self.render_template('frontend/add.j2',
                             form_data=self.request.POST.mixed(),
                             form_errors=form_errors)


class MainHandler(app.BaseRequestHandler):
    def get(self):
        self.render_template('/frontend/index.j2')


webapp2_routes = [
    webapp2.Route('/', handler=MainHandler, name='home'),
    webapp2.Route(r'/url', name='url/view', handler=ViewUrlHandler),
    webapp2.Route(r'/url/add', name='url/add', handler=AddUrlHandler),
]