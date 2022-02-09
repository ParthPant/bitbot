import time
import datetime

import numpy as np

import utils.time_utils

from .stream import Stream
from logger import Logger
from database import H5Client
from utils import resample_data
from typing import Optional


class HFStream(Stream):
    def __init__(self, exchange: str, symbol: str, interval: Optional[str] = None):
        Stream.__init__(self)
        self.hf = H5Client(exchange)
        if interval is not None:
            self.data = resample_data(self.hf.get_data(symbol, 0, int(time.time()*10000)), interval)
        else:
            interval = '1s'

        r, o = self.hf.get_time_boundaries(symbol)
        r = utils.time_utils.ms_to_dt(r)
        o = utils.time_utils.ms_to_dt(o)
        Logger().info("HFStream: %s ready to stream data (%d) of %s from %s to %s, interval: %s", exchange,
                      len(self.data), symbol, r, o, interval)

    def run_forever(self):
        if self.data.shape[0] == 0:
            Logger().info("HFStream: No data in stream")
            return

        Logger().info("HFStream: Starting stream")
        for index, row in self.data.iterrows():
            data = [int(datetime.datetime.timestamp(index)), float(row[0]), float(row[1]), float(row[2]), float(row[3]),
                    float(row[4])]
            self.on_recv(data)

        Logger().info("HFStream: Stream ended")
