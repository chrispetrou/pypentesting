#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from twisted.words.protocols import irc
from twisted.internet import reactor,protocol

class IRCBot(irc.IRCClient):
    nickname = "..." # bot nickname

    def signedOn(self):
        self.join(self.factory.channel)

    def action(self, *args, **kwargs):
        # IRC-bot's goal...
        pass

class IRCBotFactory(protocol.ClientFactory):
    def __init__(self, channel):
        self.channel = channel

    def buildProtocol(self, addr):
        proto = IRCBot()
        proto.factory = self
        return proto

    def clientConnectionLost(self, connector, reason):
        connector.connect()

    def clientConnectionFailed(self, connector, reason):
        reactor.stop()

# CHANGE THOSE ACCORDINGLY...
network = "..."
port    = None
channel = "#..."
try:
    reactor.connectTCP(network, port, IRCBotFactory(channel))
    reactor.run()
except Exception, error:
    raise(error)
# -EOF