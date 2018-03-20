from wamp.base import BaseRemoteProcedure


class SampleRemoteProcedure(BaseRemoteProcedure):
    """
    Echo input value
    """

    def __init__(self, config=None):
        super(SampleRemoteProcedure, self).__init__(config)

    def onCall(self, *args, **kwargs):
        if len(args) or 'value' not in kwargs:
            return {'response': 'error', 'data': 'Expected empty list as args and "value" key in kwargs'}

        return self._onCall(*args, **kwargs)

    def _onCall(self, value):
        """
        RPC with value as argument
        :param value: Input value (unicode)
        :return:
        """

        return value
