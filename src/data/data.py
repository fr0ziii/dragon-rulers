import datetime

class Data:
    """
    Represents market data.

    Attributes:
        timestamp (datetime): The timestamp of the data point.
        price (float): The price at the given timestamp.
    """

    def __init__(self, timestamp: datetime.datetime, price: float):
        """
        Initializes the Data object.
        """
        self.timestamp = timestamp
        self.price = price