"""test_web.py

Tests for the Presta t.w.Resources
"""
#from datetime import datetime

import mock

from twisted.trial import unittest
from twisted.web import resource
from twisted.web import static
from twisted.web import server
from twisted.web.test.test_web import DummyRequest
#from twisted.web._auth.wrapper import HTTPAuthSessionWrapper

from presta import resources


class TestRootGetChild(unittest.TestCase):
    """getChild just does dynamic lookup of child
    resources.

    """

    def setUp(self):
        testServer = mock.Mock()
        self.r = resources.Root(testServer)

    def test_getRoot(self):
        request = mock.Mock()
        request.prepath.pop.return_value = ""
        r = self.r.getChild("", request)
        self.assertTrue(isinstance(r, resources.Root))

    def test_getStatic(self):
        """Urls including '/static/' should be served by
        the static directory resource

        """
        r = self.r.getChildWithDefault("static", None)
        self.assertEqual(True, isinstance(r, static.File))

    def test_getFavicon(self):
        """The root '/favicon.ico' should be accessible

        """
        r = self.r.getChildWithDefault("favicon.ico", None)
        self.assertEqual(True, isinstance(r, static.File))
