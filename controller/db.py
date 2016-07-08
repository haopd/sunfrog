# -*- coding: utf-8 -*-
import logging
from google.appengine.ext import ndb
from google.appengine.api import search

__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class Url(ndb.Model):
    def _post_put_hook(self, future):
        rs = super(Url, self)._post_put_hook(future)
        item_obj = Url.get_by_id(((future.get_result().id())))
        if item_obj:
            url_input = ','.join(tokenize_autocomplete(item_obj.url_input))
            url_output = ','.join(tokenize_autocomplete(item_obj._input))
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