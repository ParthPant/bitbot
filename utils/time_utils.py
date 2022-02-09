import datetime
import pandas as pd

TF = {'1m': '1Min', '5m': '5Min', '15m': '15Min', '30m': '30Min', '1h': '1H', '4h': '4H', '12h': '12H', '1d': 'D'}


def resample_data(data: pd.DataFrame, tf: str):
    return data.resample(TF[tf]).aggregate(
            {'open': 'first', 'high': 'max', 'low': 'min', 'close': 'last', 'volume': 'sum'}
            )


def ms_to_dt(t: int):
    return datetime.datetime.utcfromtimestamp(t / 1000)
