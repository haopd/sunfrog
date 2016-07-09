# -*- coding: utf-8 -*-
import logging
import random
import string

import webapp2
import app
import formencode
from formencode import validators
from controller import db
from controller import url as urlz
from google.appengine.api import search
from google.appengine.ext import ndb
import re
from webapp2_extras import jinja2

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class AddUrlForm(formencode.Schema):
    allow_extra_fields = True

    url_input = validators.UnicodeString(not_empty=True)
    url_output = validators.URL()


class ViewUrlHandler(app.BaseRequestHandler):
    def get(self):
        search_results = []
        keyword_search = self.request.GET.get('search')
        offset = self.request.GET.get('offset', 0)
        index = search.Index(name='url_fulltextsearch')
        if keyword_search:
            input = re.sub(r'[^a-zA-Z0-9\n_&]', ' ', keyword_search)
            query_string = 'url_input_search = %s OR url_output_search = %s' % \
                           (input, input)
            search_results = index.search(search.Query(
                query_string=query_string,
                options=search.QueryOptions(
                    limit=10
                )
            ))
        list_ids = []
        list_url = []
        for result in search_results:
            list_ids.append(result.doc_id)
        if list_ids:
            list_url = ndb.get_multi([ndb.Key(db.Url, int(k)) for k in list_ids])
        else:
            list_url = db.Url.query().order(- db.Url.time_created).fetch(1000)
        return self.render_template('frontend/view.j2', list_url=list_url)


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
            if urlz.is_url_existed(obj.url_output):
                self.session.add_flash(u'Url này đã tồn tại', 'error')
                return self.redirect_to('url/add')
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


class UrlRedirect(webapp2.RequestHandler):
    def get(self, web_url):
        if web_url:
            page_obj = db.Url.query(db.Url.url_input == web_url).fetch(1)
            if page_obj:
                self.redirect(str(page_obj[0].url_output))
            else:
                self.abort(404)
        else:
            self.abort(404)

class DetailUrlHandler(app.BaseRequestHandler):
    def get(self, url_id):
        url = db.Url.get_by_id(int(url_id))
        self.render_template('/frontend/detail.j2', url=url)


class EditUrlHandler(app.BaseRequestHandler):
    def get(self, url_id):
        url = db.Url.get_by_id(int(url_id))
        self.render_template('/frontend/edit.j2', url=url, form_data=None,
                             form_errors=None)

    def post(self, url_id):
        url = db.Url.get_by_id(int(url_id))
        form_validate = AddUrlForm()
        form_errors = {}
        try:
            data = form_validate.to_python(self.request.POST)
            obj = db.Url.get_by_id(int(url_id))
            obj.url_input = data.get('url_input')
            obj.url_output = data.get('url_output')
            obj.status = True
            obj.put()
            self.session.add_flash('Success')
            return self.redirect_to('url/view', url_id=url_id)
        except formencode.Invalid as e:
            form_errors = e.error_dict
        self.render_template('frontend/add.j2',
                             form_data=self.request.POST.mixed(),
                             form_errors=form_errors, url=url)


class DeleteUrlHandler(app.BaseRequestHandler):
    def get(self, url_id):
        url = db.Url.get_by_id(int(url_id))
        url.key.delete()
        return self.redirect_to('url')


class LoginHandler(webapp2.RequestHandler):
    @webapp2.cached_property
    def jinja2(self):
        """
        Returns:
            jinja2.Jinja2
        """
        return jinja2.get_jinja2(app=self.app)

    def randomword(self, length):
        s = string.lowercase + string.digits
        return ''.join(random.sample(s, length))

    def get(self):
        rv = self.jinja2.render_template('/frontend/login.j2')
        self.response.write(rv)

    def post(self):
        email = self.request.get('email')
        password = self.request.get('password')
        if email and password:
            if (email == 'danghao.cntt@gmail.com' and password == '123!@#hao'):
                self.response.set_cookie('credentials', self.randomword(20),
                                         60 * 60)
                self.redirect_to('home')
        else:
            self.redirect_to('login')


webapp2_routes = [

    webapp2.Route('/admin', handler=MainHandler, name='home'),
    webapp2.Route('/admin', handler=MainHandler, name='home'),
    webapp2.Route(r'/url', name='url', handler=ViewUrlHandler),
    webapp2.Route(r'/url/add', name='url/add', handler=AddUrlHandler),
    webapp2.Route(r'/url/edit/<url_id>', name='url/edit',
                  handler=EditUrlHandler),
    webapp2.Route(r'/url/delete/<url_id>', name='url/delete',
                  handler=DeleteUrlHandler),
    webapp2.Route(r'/url/<url_id>', name='url/view', handler=DetailUrlHandler),
    webapp2.Route(r'/signin', name='login', handler=LoginHandler),
    webapp2.Route('/<web_url>', handler=UrlRedirect),
]