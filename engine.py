from exchanges import Exchange
from strategies import Strategy, Signal
from streams import Stream
from logger import Logger
import time
import numpy


class Engine:
    def __init__(self, exchange: Exchange, symbol: str, strategy: Strategy, stream: Stream):
        # stream can be optional here and exchange should provide a wsstream itself
        self.exchange = exchange
        self.symbol = symbol
        self.strategy = strategy
        self.stream = stream
        self.balance = 100
        self.stream.on_recv = self.__on_data
        self.trades = []
        self.cp = 0
        self.sp = 0

    def __on_data(self, data):
        signal = self.strategy.crunch(data)
        match signal:
            case Signal.ENTER_SIGNAL:
                self.buy(data)
            case Signal.EXIT_SIGNAL:
                self.sell(data)
            case Signal.NO_SIGNAL:
                pass

    def buy(self, data):
        self.cp = data[-2]

    def sell(self, data):
        self.sp = data[-2]
        self.trades.append((self.sp-self.cp)/self.cp)

    def churn(self):
        start = time.time()
        self.stream.run_forever()
        delta = time.time() - start

        Logger().info("Number of trades: %d", len(self.trades))
        Logger().info("total P&L: %f%%", 100 * numpy.sum(self.trades))
        Logger().info("average P&L: %f%%", 100 * numpy.average(self.trades))
        Logger().info("standard dev: %f", numpy.std(self.trades))

        for profit in self.trades:
            self.balance = self.balance + self.balance*profit

        Logger().info("balance: %f", self.balance)
        Logger().info("Time taken: %s", delta)
