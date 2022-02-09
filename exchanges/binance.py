from typing import Optional, List, Tuple

import requests

from logger import Logger
from .exchange import Exchange


class Binance(Exchange):
    def __init__(self):
        self.base_url = "https://api.binance.com/api/v3/"
        self.__symbols = []
        self.fetch_symbols()

    def fetch_symbols(self, update: bool = False):
        r = requests.get(self.base_url + 'exchangeInfo')
        if len(self.__symbols) == 0 or update:
            symbols_res = r.json()['symbols']
            self.__symbols = [s['symbol'] for s in symbols_res]
        else:
            Logger().info("Binance: Symbols are already updated")

    def get_symbols(self):
        return self.__symbols

    def get_symbol_klines(self,
                          symbol: str,
                          interval: str,
                          starttime: Optional[int] = None,
                          endtime: Optional[int] = None,
                          limit: Optional[int] = 1000) -> List[Tuple[int, float, float, float, float, float, int]]:

        url = self.base_url + 'klines'

        if symbol not in self.__symbols:
            Logger().error("Binance: %s is not a valid symbol", symbol)
            raise ValueError

        payload: dict[str, str | int] = {"symbol": symbol, "interval": interval}

        if starttime:
            payload["startTime"] = int(starttime)
        if endtime:
            payload["endTime"] = int(endtime)
        if limit:
            payload["limit"] = str(limit)

        r = requests.get(url, payload)
        if r.status_code == 400:
            Logger().debug(r.json())
            raise ValueError

        ret = [(int(x[0]), float(x[1]), float(x[2]), float(x[3]), float(x[4]), float(x[5]), int(x[6])) for x in
               r.json()]
        return ret

    def __str__(self):
        return "Binance"
