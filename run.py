from autobahn.twisted.wamp import ApplicationRunner
from twisted.internet import reactor

from wamp.sample import SamplePublish
from websocket.sample import SampleRemoteProcedure

import settings

from time import sleep

# Wait for crossbar to startup
sleep(10)

# Pass data to the publish sample
publish_extra = {'interval': 10}

# noinspection PyTypeChecker
publish_runner = ApplicationRunner(url=settings.CROSSBAR_URI, realm='realm1', extra=publish_extra)
publish_runner.run(SamplePublish, start_reactor=False)

# Pass data to the RPC sample
rpc_extra = {'rpc': 'sampleRPC'}

# noinspection PyTypeChecker
rpc_runner = ApplicationRunner(url=settings.CROSSBAR_URI, realm='realm1', extra=rpc_extra)
rpc_runner.run(SampleRemoteProcedure, start_reactor=False)

# noinspection PyUnresolvedReferences
reactor.run()
