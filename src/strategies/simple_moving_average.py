from .strategy import Strategy

class SimpleMovingAverageStrategy(Strategy):
    """
    A simple moving average trading strategy.
    """

    def __init__(self, name: str, description: str, window_size: int):
        """
        Initializes the strategy with a name, description, and window size.
        """
        super().__init__(name, description)
        self.window_size = window_size

    def execute(self, data):
        """
        Executes the strategy based on a simple moving average.
        Placeholder - actual implementation would calculate SMA and generate signals.
        """
        if len(data) < self.window_size:
            return "Not enough data"

        prices = [d.price for d in data[-self.window_size:]]
        sma = sum(prices) / self.window_size
        if data[-1].price > sma:
            return "Buy"
        elif data[-1].price < sma:
            return "Sell"
        else:
            return "Hold"