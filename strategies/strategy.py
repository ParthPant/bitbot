from exchanges import Exchange
from typing import Optional, Dict, Any, List
from enum import Enum, unique


@unique
class Signal(Enum):
    ENTER_SIGNAL = 1
    EXIT_SIGNAL = 2
    NO_SIGNAL = 3


class Strategy:
    def __init__(self):
        self.cache = {'open': [], 'high': [], 'low': [], 'close': [], 'vol': []}
        self.cache_len = 0
        self.__parameters: Dict = {}

    def crunch(self, data) -> Signal:
        self.cache['open'].append(data[1])
        self.cache['high'].append(data[2])
        self.cache['low'].append(data[3])
        self.cache['close'].append(data[4])
        self.cache['vol'].append(data[5])
        self.cache_len = self.cache_len + 1

        signal = self.crunch_impl(data)

        if self.cache_len > 100:
            self.clear_cache()

        return signal

    def crunch_impl(self, data) -> Signal:
        ...

    def get_param(self, key: str):
        if key in self.__parameters.keys():
            return self.__parameters[key]
        else:
            raise ValueError

    def set_param(self, key: str, val: Any):
        self.__parameters[key] = val

    def clear_cache(self):
        self.cache['open'] = self.cache['open'][-60:]
        self.cache['high'] = self.cache['high'][-60:]
        self.cache['low'] = self.cache['low'][-60:]
        self.cache['close'] = self.cache['close'][-60:]
        self.cache['vol'] = self.cache['vol'][-60:]
        self.cache_len = len(self.cache['open'])
