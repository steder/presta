#-*- test-case-name: presta.test.test_settings -*-
"""
The settings.py module loads a yaml/json document
which is used as a configuration file
for the presta service.

Between the ---- markers is an example
of a valid yaml file:

-----------------------------------

# this is a comment
host: localhost
port: 8483

databases:
  default:
    ENGINE: 'sqlite3'
    NAME: 'test.db'
-----------------------------------

"""

import exceptions
import os

from twisted.python import filepath
import yaml

# Twisted settings for Presta project
HOST = "localhost"
PORT = 8080
DEFER_DEBUG = False # deferred debugging can be chatty and memory intensive
PRESTA_ROOT = filepath.FilePath(__file__).parent().parent()

TEMPLATE_DIR = PRESTA_ROOT.child("presta").child("templates").path

# Django settings for Presta project.

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME': PRESTA_ROOT.child("test.db").path,  # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

FRONTEND_STATIC_PATH = PRESTA_ROOT.child("frontend").child("static").path
FRONTEND_TEMPLATE_PATH = PRESTA_ROOT.child("frontend").child("templates").path


class PrestaSettingsError(exceptions.Exception):
    """Configuration file missing or unable to load all required settings"""


def load(path=None):
    if not path:
        path = os.path.join(os.curdir, "presta.conf")

    if not os.path.exists(path):
        raise PrestaSettingsError("Missing config file: %s"%(path,))

    config_file = open(path, "r")
    config = yaml.safe_load(config_file.read())

    settings = {}
    for key,value in config.iteritems():
        setting = key.upper()
        settings[setting] = value

    g = globals()
    # let's only load config that we've got variables defined in this namespace
    for key in g:
        if key in settings:
            g[key] = settings[key]
    return settings


load()
