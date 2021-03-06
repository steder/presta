"""
Plugs presta into twistd utility for daemonization, chroot,
logging configuration, etc.
"""
from twisted.application.service import IServiceMaker
from twisted.plugin import IPlugin
from twisted.python import usage

from zope.interface import implements

from presta import server


class Options(usage.Options):
    optFlags = [
        ["rotate", "r", "use daily log rotation instead of the default"]
    ]

    optParameters = [["port", "p", None, "port number to listen on."],
                     ["logfile", "l", "twistd.log", "file name to log to (ignored without --rotate)"],
                     ["logdirectory", "d", ".", "path to directory for log files (ignored without --rotate"]
                     ]


class PrestaServiceMaker(object):
    implements(IPlugin, IServiceMaker)
    tapname = "presta"
    description = "Presta Service"
    options = Options

    def makeService(self, options):
        """
        Construct a TCPServer from a factory defined in myproject.
        """
        from presta import settings
        port = options["port"]
        if port is None:
            port = settings.PORT
        port = int(port)
        rotate = options["rotate"]
        logFile = options["logfile"]
        logDirectory = options["logdirectory"]
        madeServer = server.PrestaServer(port)
        madeServer.daily = bool(rotate)
        madeServer.logFile = logFile
        madeServer.logDirectory = logDirectory
        return madeServer


presta = PrestaServiceMaker()
