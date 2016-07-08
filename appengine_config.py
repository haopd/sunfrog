__author__ = 'datpt'

"""
`appengine_config.py` gets loaded every time a new instance is started.

Use this file to configure app engine modules as defined here:
https://developers.google.com/appengine/docs/python/tools/appengineconfig
"""

import os
import logging.config

GAE_MODE = None
DEVELOPMENT_MODE = None
PYTEST_MODE = None


def _detect_running_mode():
    global GAE_MODE, DEVELOPMENT_MODE, PYTEST_MODE
    ss = os.environ.get('SERVER_SOFTWARE', '').strip().lower()
    GAE_MODE = ss.startswith('google app engine')
    if not GAE_MODE:
        PYTEST_MODE = ss.startswith('pytest')
        if not PYTEST_MODE:
            DEVELOPMENT_MODE = True
_detect_running_mode()


ROOT_DIR = os.path.dirname(__file__)
if GAE_MODE:
    logging.config.fileConfig(os.path.join(ROOT_DIR, 'logging.ini'),
                              disable_existing_loggers=False)
else:
    logging.config.fileConfig(os.path.join(ROOT_DIR, 'logging-dev.ini'),
                              disable_existing_loggers=False)


from google.appengine.ext import vendor
vendor.add('lib')
vendor.add('lib/vendor-packages')