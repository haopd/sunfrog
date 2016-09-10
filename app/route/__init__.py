# -*- coding: utf-8 -*-
import logging
import webapp2
import app
__author__ = 'datpt'
_logger = logging.getLogger(__name__)


class MainHandler(app.BaseRequestHandler):
    def get(self):
        self.render_template('/layouts/index.j2')

from app.eapis.task_queue import UploadDataToSheet


webapp2_routes = [
    webapp2.Route('/', handler=MainHandler, name='home'),
    webapp2.Route('/taskqueue/upload-sheets', handler=UploadDataToSheet,
                  name='taskqueue/upload-to-sheets')
]