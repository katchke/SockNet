class MultiTable(object):
    """
    Multiplication table for a given multiplicand
    """

    def __init__(self, multiplicand):
        """
        :param multiplicand: Initial value (int)
        """
        if not isinstance(multiplicand, (int, float)):
            raise TypeError('Expected type(s): num <int, float>')

        self.multiplicand = multiplicand
        self.multiplier = 0

    def fetch(self):
        """
        Fetch next value in the table
        :return: Number (float)
        """

        self.multiplier += 1

        return self.multiplicand * self.multiplier
