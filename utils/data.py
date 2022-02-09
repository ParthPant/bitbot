import time
from database import H5Client
from exchanges import Binance, Exchange
from logger import Logger
try:
    from time_utils import ms_to_dt
except ModuleNotFoundError:
    from .time_utils import ms_to_dt


def collect_historical_data(symbol: str, exchange: Exchange):
    Logger().info("collecting data from %s from %s", symbol, exchange)
    h5 = H5Client(str(exchange))
    h5.create_dataset(symbol)

    most_recent_time, oldest_time = h5.get_time_boundaries(symbol)
    get_data = True

    data_bank = []

    if not most_recent_time or not oldest_time:
        Logger().debug("fetching initial recent data")
        try:
            data = exchange.get_symbol_klines(symbol, interval='1m', endtime=int(time.time() * 1000) - 60000)
            oldest_time = data[0][0]
            most_recent_time = data[-1][0]
            data_bank.extend(data)
            Logger().debug("fetched %s from %s to %s", len(data), ms_to_dt(oldest_time), ms_to_dt(most_recent_time))
        finally:
            pass

    while get_data:
        try:
            Logger().debug("fetching older data")
            data = exchange.get_symbol_klines(symbol, interval='1m', endtime=oldest_time - 60000)
            if len(data) == 0:
                h5.write_data(symbol, data_bank)
                get_data = False
                break

            oldest_time = data[0][0]
            data_bank.extend(data)
            Logger().debug("fetched %s from %s to %s", len(data), ms_to_dt(oldest_time), ms_to_dt(data[-1][0]))
        finally:
            if len(data_bank) > 120000:
                h5.write_data(symbol, data_bank)
                data_bank = []

        time.sleep(1.2)

    Logger().info("Completed fetching data")


def main():
    binance = Binance()
    symbol = 'SOLUSDT'
    collect_historical_data(symbol, binance)


if __name__ == "__main__":
    main()