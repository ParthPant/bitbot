from engine import Engine
from exchanges import Binance
from strategies import OBVStrategy, SMACrossover
from streams import HFStream


def main():
    binance = Binance()
    symbol = 'BTCUSDT'
    stream = HFStream(str(binance), symbol, "4h")
    strategy = SMACrossover()

    engine = Engine(binance, symbol, strategy, stream)
    engine.churn()


if __name__ == "__main__":
    main()
