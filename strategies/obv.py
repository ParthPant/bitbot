from .strategy import Strategy
from exchanges import Exchange
from talib import stream
import numpy as np


class OBVStrategy(Strategy):
    def __init__(self):
        Strategy.__init__(self)

    def crunch(self, data):
        obv = stream.OBV(np.array(self.cache['close']), np.array(self.cache['vol']))
        pass

    def send_signal(self):
        pass
