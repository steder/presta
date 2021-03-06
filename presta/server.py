#-*- test-case-name: presta.tests.test_server -*-
"""
Defines the Presta Service

"""

from twisted.application import internet, service
from twisted.internet import defer, reactor
from twisted.python import log
from twisted.python import logfile
from twisted.web import server

from presta import settings
from presta.resources import Root

defer.setDebugging(settings.DEFER_DEBUG)


class PrestaServer(service.MultiService):
    """This is the main service which listens
    on settings.PORT for incoming HTTP requests.

    Any other top level services are setup here.

    Attributes:
      started: boolean indicating whether we've started listening on our port(s)
               or if we're still starting up.

    Configuration:
      settings.MODE: controls which dispatcher is used by the pool
      settings.READY: controls how we know the processes in the pool are started

    """

    def __init__(self, port):
        """
        Initialze PrestaServer instance.

          port: port on which the HTTP server should run

        """
        self.system = "PrestaServer"
        self.started = False
        self._initializeLogging()
        service.MultiService.__init__(self)
        webServerFactory = server.Site(Root(self))
        webServer = internet.TCPServer(port, webServerFactory)
        webServer.setName("Presta")
        webServer.setServiceParent(self)

    def _initializeLogging(self):
        self.daily = False
        self.logFile = "twisted.log"
        self.logDirectory = "."

    def setServiceParent(self, application):
        """Set the service parent.

        Overridden here so that we can hold onto the application
        object being constructed by Twistd.

        """
        self.application = application
        self._customizeLogging()
        service.Service.setServiceParent(self, application)

    def _cbStartup(self, result):
        """This callback really starts the service
        listening on settings.PORT

        """
        self.started = True
        if self.daily:
            log.msg("Logging rotation set to daily.")
        else:
            log.msg("Logging rotation set to default(size: ~1MB).")
        log.msg("Presta is ready for eBusiness", system=self.system)
        service.MultiService.startService(self)
        return result

    def _ebStartup(self, failure):
        """This errback shuts us down if an error occured
        in process pool startup.

        """
        log.msg("failure starting service: %s"%(str(failure)), system=self.system)
        log.err("stopping reactor due to failure...", system=self.system)
        reactor.stop()

    def _customizeLogging(self):
        """Configure the twisted logging system based on twistd options.

        PrestaServer.daily (bool): controls whether or not
          we override logging settings
        PrestaServer.logFile (str): specifies name of log file
        PrestaServer.logDirectory (str): specifies path of directory
          that we will use for logging.

        """
        # TODO: move to twistd commandline logging configuration?
        if self.daily:
            lf = logfile.DailyLogFile(self.logFile, self.logDirectory)
            observer = log.FileLogObserver(lf).emit
            self.application.setComponent(log.ILogObserver, observer)

    def startService(self):
        """Perform startup tasks before we start listening
        on the external port (settings.PORT).

        returns None (no deferred processing in startService)
        """
        log.msg("starting services:", system=self.system)
        d = self.startDeferred = defer.Deferred()
        d.addCallback(self._cbStartup)
        d.addErrback(self._ebStartup)
        reactor.callWhenRunning(self.startupHook, d)

    def startupHook(self, startServiceDeferred):
        """Perform additional startup tasks.

        This is a placeholder for future extension.

        This function *MUST* callback / errback
        the startServiceDeferred.

        Returns None
        """
        startServiceDeferred.callback(True)

    def shutdownHook(self):
        """Perform additional shutdown tasks.

        For now this is just a placeholder for future extension.

        Returns a deferred.
        """
        d = defer.Deferred()
        return d

    def stopService(self):
        """Perform service shutdown processes.

        returns: deferred

        1. stops listening on the external port
        2. runs ``self.shutdownHook``

        Any additional shutdown processing can be
        added as callbacks to the returned deferred.
        """
        log.msg("Shutting down service ...", system=self.system)
        d = service.MultiService.stopService(self)
        if self.started:
            d.chainDeferred(self.shutdownHook())
        d.addCallback(log.msg, **{"system":self.system})
        d.addErrback(log.err, **{"system":self.system})
        return d
