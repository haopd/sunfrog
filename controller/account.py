# -*- coding: utf-8 -*-
import logging
from controller import db

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


def is_username_existed(username):
    is_existed = db.Account.query().filter(db.Account.username == username).fetch()
    return bool(is_existed)


def create_account(username, password, phone=None, email = None, name = None):
    pwd = db.Password.create_password(password)
    acc = db.Account()
    acc.username = username
    acc.password = pwd
    acc.phone = phone
    acc.email = email
    acc.name = name
    acc.put()