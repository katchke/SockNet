from __future__ import unicode_literals

import abc

from autobahn.twisted.wamp import ApplicationSession
from autobahn.twisted.util import sleep
from twisted.internet.defer import inlineCallbacks

import helper


# noinspection PyPep8Naming
class BasePublish(ApplicationSession):
    """
    Base class for publish components.
    The component starts publishing events to topics only on
    the subscription of atleast one client (subscriber).
    It stops publishing events to that topic in case the topic
    is deleted (i.e there are no subscribers to the topic).
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, config=None):
        """
        Initialize publish component.
        Keep a record of active topics (topics that are streaming events) and
        active subs (mainly to map subscription ids and topic names).
        :param config: Session configuration
        """
        super(BasePublish, self).__init__(config)

        helper.logger.info('Creating publish component: {name}..'.format(name=self.__class__.__name__))

        self.active_subs = []  # Subscriptions IDs of active subscriptions (subscriptions that are publishing events)

        self.interval = config.extra.get('interval')  # Time interval (in seconds) between events

        if not isinstance(self.interval, (int, float)):
            raise TypeError('interval <int, float>')

    @inlineCallbacks
    def onJoin(self, _):
        # Print subscriptions that may have carried over from previous iterations. Events are not
        # published to such topics
        subs = yield self.call('wamp.subscription.list')
        subs = subs['exact']
        helper.logger.warning('Existing subscriptions: {}. Events cannot be published to these topics.'.format(
            ', '.join([str(sub) for sub in subs]))) if subs else None

        # Subscribe to meta events that may be fired
        yield self.subscribe(self.onCreateSubscription, 'wamp.subscription.on_create')
        yield self.subscribe(self.onDeleteSubscription, 'wamp.subscription.on_delete')

    @inlineCallbacks
    def onCreateSubscription(self, _, subscription):
        """
        Do something on subscription creation
        :param _: Placeholder (_)
        :param subscription: Data about the subscription (dict)
        """
        topic = subscription['uri']

        # Keep records of active subscription ids
        sub = yield self.call('wamp.subscription.lookup', topic)
        self.active_subs.append(sub)

        helper.logger.debug('Created subscription with ID {sub}'.format(sub=sub))

        # Publish events to topic
        yield self._pub(sub, topic)

    @inlineCallbacks
    def _pub(self, sub, topic):
        """
        Publish events to topic
        :param sub: Subscription ID (unicode)
        :param topic: Topic name (unicode)
        """
        assert isinstance(topic, unicode), 'Expected type: topic <unicode>'

        # Start publishing events to topics every <interval> seconds
        helper.logger.debug('Publishing events to topic {topic}'.format(topic=topic))

        while True:
            resp = self.onEvent(topic)  # Fetch latest data

            assert isinstance(resp, dict), 'Response needs to be a dict'

            # Stop publishing events if the subscription is deleted (i.e there are
            # no more subscribers to that topic)
            if sub not in self.active_subs or resp.get('response') == 'error':
                helper.logger.debug('Stopping events being published to topic {topic}'.format(topic=topic))
                break

            self.publish(topic, response=resp.get('response'), data=resp.get('data'))

            yield sleep(self.interval)

    def onDeleteSubscription(self, _, sub):
        """
        Do something on subscription deletion
        :param _: Placeholder (_)
        :param sub: Subscription ID (unicode)
        """
        # Remove topic name and subscriptions ids from records once there
        # are no more subscribers to the topic
        self.active_subs.remove(sub)
        helper.logger.debug('Deleted subscription with ID {sub}'.format(sub=sub))

    @abc.abstractmethod
    def onEvent(self, topic):
        """
        Do something on event occurrence.
        :param topic: Topic name (unicode)
        :return: Response in the form {'response': <response>, 'data': <data>} (dict)
        """
        return {'response': '<response>', 'data': '<data>'}


# noinspection PyPep8Naming
class BaseRemoteProcedure(ApplicationSession):
    """
    Base class for all RPC components.
    Pass RPC name as extra in config and implement the procedure in the call method.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, config=None):
        super(BaseRemoteProcedure, self).__init__(config)

        helper.logger.info('Creating RPC component: {name}..'.format(name=self.__class__.__name__))

        self.rpc = config.extra.get('rpc')

        if not isinstance(self.rpc, (str, unicode)):
            raise TypeError('Expected type: rpc <str, unicode>')

    @inlineCallbacks
    def onJoin(self, _):
        helper.logger.info('Registering RPC: {rpc}'.format(rpc=self.rpc))
        yield self.register(self.onCall, self.rpc)

    @abc.abstractmethod
    def onCall(self, *args, **kwargs):
        """
        Remote Procedure
        Validate arguments and call _onCall()
        :return: Response in the form {'response': <response>, 'data': <data>} (dict)
         """
        # Validate arguments

        return self._onCall(*args, **kwargs)

    @abc.abstractmethod
    def _onCall(self, *args, **kwargs):
        """
        Do something when remote procedure is called
        :return: Response in the form {'response': <response>, 'data': <data>} (dict)
        """
        return {'response': '<response>', 'data': '<data>'}
