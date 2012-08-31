#-*- test-case-name: presta.test.test_web -*-
import os

from twisted.internet import defer
from twisted.internet import threads
from twisted.internet import reactor
from twisted.web import http, resource, server, static
from twisted.web import wsgi

#from txtemplate import templates
from presta import settings


staticDirectory = static.File(
    settings.FRONTEND_STATIC_PATH
)


class Root(resource.Resource):
    def __init__(self, server):
        resource.Resource.__init__(self)
        self.server = server
        self.putChild('static', staticDirectory)
        self.putChild("favicon.ico", static.File(
            os.path.join(settings.FRONTEND_STATIC_PATH, "favicon.ico")
            )
        )

    def render_GET(self, request):
        return """<html>
<head><title>Hello World</title></head>
<body><h1>Hello World!</h1>
</body>
</html>"""

    def getChild(self, path, request):
        return self
