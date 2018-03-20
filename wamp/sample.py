from base import BasePublish

from source import MultiTable

import helper


class SamplePublish(BasePublish):
    """
    Publish multiplication table for a given multiplicand
    """

    def __init__(self, config=None):
        super(SamplePublish, self).__init__(config)

        self.sources = {}

    def onEvent(self, multiplicand):
        """
        On completion of interval, fetch next value in the multiplication table
        :param multiplicand: Multiplicand (unicode)
        :return: Response, Data (str, object)
        """

        if not helper.is_num(multiplicand):
            return {'response': 'error', 'data': 'Expected multiplicand to be a number'}

        # Register topic (multiplicand) if not already registered
        self.sources.setdefault(multiplicand, MultiTable(float(multiplicand)))

        return self.sources[multiplicand].fetch()

    def onDeleteSubscription(self, _, sub):
        super(SamplePublish, self).onDeleteSubscription(_, sub)
