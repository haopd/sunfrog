# -*- coding: utf-8 -*-
import logging
from google.appengine.ext import ndb
from google.appengine.api import search
from controller import utils

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class Password(ndb.Model):
    hash = ndb.StringProperty()
    salt = ndb.StringProperty()

    @classmethod
    def create_password(cls, password):
        """ Ghi nhận password mới vào instance hiện tại
        Args:
            password (str|None): password mới
        """
        if not password:
            salt, hash = None, None
        else:
            salt = utils.sure_unicode(utils.random_string(6))
            hash = utils.hash_password(password, salt)
        entity = cls(hash=hash, salt=salt)
        entity.put()
        return entity


class Account(ndb.Model):
    username = ndb.StringProperty(required=True)
    email = ndb.StringProperty()
    phone = ndb.StringProperty()
    password = ndb.StructuredProperty(Password)
    name = ndb.StringProperty(indexed=False)
    status = ndb.BooleanProperty(default=True)
    time_created = ndb.DateTimeProperty(auto_now_add=True)
    time_modify = ndb.DateTimeProperty(auto_now=True)


class Url(ndb.Model):
    def _post_put_hook(self, future):
        rs = super(Url, self)._post_put_hook(future)
        item_obj = Url.get_by_id(((future.get_result().id())))
        if item_obj:
            url_input = ','.join(tokenize_autocomplete(item_obj.url_input))
            url_output = ','.join(tokenize_autocomplete(item_obj.url_output))
            my_document = search.Document(
                doc_id=str(future.get_result().id()),
                fields=[
                    search.TextField(name='url_input_search',
                                     value=url_input),
                    search.TextField(name='url_output_search',
                                     value=url_output)
                ])
            index = search.Index(name="url_fulltextsearch")
            index.put(my_document)
        return rs

    @classmethod
    def _post_delete_hook(cls, key, future):
        super(Url, cls)._post_delete_hook(key, future)
        index = search.Index(name="url_fulltextsearch")
        index.delete([str(key.id())])

    url_input = ndb.StringProperty(required=True)
    url_output = ndb.StringProperty(required=True)
    status = ndb.BooleanProperty(default=True)
    time_created = ndb.DateTimeProperty(auto_now_add=True)
    time_modify = ndb.DateTimeProperty(auto_now=True)


def tokenize_autocomplete(phrase):
    a = []
    for word in phrase.split():
        j = 5
        while True:
            for i in range(len(word) - j + 1):
                a.append(word[i:i + j])
            if j == len(word):
                break
            j += 1
    return a