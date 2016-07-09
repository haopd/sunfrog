# -*- coding: utf-8 -*-
import logging
import formencode
from formencode import validators
import app
from controller import account

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class AddAccountForm(formencode.Schema):
    allow_extra_fields = True

    username = validators.Regex(r'^[0-9a-zA-Z_]+$', messages={
            'invalid': u'Username chỉ được chứa các ký tự a-z,0-9,_',
        })
    password = validators.MinLength(8, not_empty=True)
    password_confirm = validators.ByteString(not_empty=True)
    chained_validators = [validators.FieldsMatch(
        'password', 'password_confirm', not_empty=True, messages={
            'invalidNoMatch': u'Mật khẩu không trùng khớp'
        })]


class MainAccountHandler(app.BaseRequestHandler):
    def get(self):

        self.render_template('/frontend/account/view.j2')


class GrantedAccountHandler(app.BaseRequestHandler):
    def get(self):
        self.render_template('/frontend/account/view.j2')


class ViewDetailAccountHandler(app.BaseRequestHandler):
    def get(self):
        self.render_template('/frontend/account/view.j2')


class AddAccountHandler(app.BaseRequestHandler):
    def get(self):
        self.render_template('/frontend/account/add.j2', form_data = None,
                             form_errors=None)

    def post(self):
        validate_form = AddAccountForm()
        form_errors = {}
        try:
            data = validate_form.to_python(self.request.POST)
            if account.is_username_existed(data.get('username')):
                self.session.add_flash(u'Tên đăng nhập đã tồn tại', 'error')
                self.render_template('/frontend/account/add.j2',
                                     form_data=self.request.POST.mixed(),
                                     form_errors=form_errors)
            account.create_account(data.get('username'),
                                   data.get('password'))
            self.session.add_flash(u'Thêm thành công')
            self.redirect_to('account')
        except formencode.Invalid as e:
            form_errors = e.error_dict
        self.render_template('/frontend/account/add.j2',
                             form_data=self.request.POST.mixed(),
                             form_errors=form_errors)
