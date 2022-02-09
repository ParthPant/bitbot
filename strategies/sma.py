from .strategy import Strategy, Signal
from talib import stream
import numpy as np


class SMACrossover(Strategy):
    def __init__(self):
        Strategy.__init__(self)
        self.set_param('slow_moving_time', 24)
        self.set_param('fast_moving_time', 9)

        self.open = False
        self.tsl = 0

    def crunch_impl(self, data) -> Signal:
        slow = stream.EMA(np.array(self.cache['close'][-self.get_param('slow_moving_time'):]),
                          timeperiod=self.get_param('slow_moving_time'))
        fast = stream.EMA(np.array(self.cache['close'][-self.get_param('fast_moving_time'):]),
                          timeperiod=self.get_param('fast_moving_time'))
        self.tsl = max(self.cache['close'][-1], self.tsl)

        if fast > slow and not self.open:
            self.open = True
            self.tsl = data[-2]

            return Signal.ENTER_SIGNAL
        elif self.open and (fast < slow or data[-2] < 0.01*95*self.tsl):
            self.open = False
            return Signal.EXIT_SIGNAL

        return Signal.NO_SIGNAL
