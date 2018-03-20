import abc
import json

from autobahn.twisted.websocket import WebSocketServerProtocol
from autobahn.twisted.websocket import WebSocketServerFactory

import helper


# noinspection PyPep8Naming,PyMethodMayBeStatic,PyMethodMayBeStatic,PyMethodMayBeStatic
class BaseProtocol(WebSocketServerProtocol):
    """
    Base class for web socket protocols
    """
    __metaclass__ = abc.ABCMeta

    def onConnect(self, request):
        helper.logger.info('Client connecting: {}'.format(request.peer))

    def onOpen(self):
        helper.logger.info('WebSocket connection open.')

    def onMessage(self, payload, isBinary):
        # If message is a text (unicode encoded), print message and send confirmation
        if not isBinary:
            self.send('info', 'Text message received', isBinary=False)
            helper.logger.info(payload.decode('utf8'))
            return

        msg = json.loads(payload)
        self.processMessage(msg) if msg['request'] and msg['data'] else self.sendData('error', 'Wrong message format')

    @abc.abstractmethod
    def processMessage(self, msg):
        """
        Do something on receiving a message over web socket
        :param msg: Message in the form {'request': <str>, 'data': <object>}
        """
        self.send('info', msg)

    def send(self, response, data, isBinary=True):
        """
        Send message over web socket
        :param response: Response code ['error', 'data', 'info'] (str)
        :param data: Actual data (object)
        :param isBinary: Whether message to be sent as bytes or unicode (bool)
        """
        self.sendMessage(json.dumps({'response': response, 'data': data}), isBinary=isBinary)

    def onClose(self, wasClean, _, reason):
        reason = 'Closed cleanly' if wasClean else reason
        helper.logger.info('WebSocket connection closed: {}'.format(reason))


class BaseFactory(WebSocketServerFactory):
    """
    Base class for web socket factories
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, name, uri, protocol):
        """
        Initialize factory
        :param name: Name of factory (str)
        :param uri: URI of web socket in the form "ws://<host>:<port>" (str)
        :param protocol: Protocol object (object derived from BaseProtocol)
        """
        super(BaseFactory, self).__init__(uri)

        self.uri = uri
        self.name = name
        self.protocol = protocol
