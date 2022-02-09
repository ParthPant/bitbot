from typing import Tuple, List
import h5py
import numpy as np
import pandas as pd
from logger import Logger


class H5Client:
    def __init__(self, name: str):
        self.name = name
        self.filepath = f"data/{name}.hdf"
        self.hf = h5py.File(self.filepath, 'a')
        self.hf.flush()

    def create_dataset(self, symbol: str, num_cols: int = 7):
        if symbol in self.hf.keys():
            Logger().info("H5Client: %s already has dataset for %s", self.name, symbol)
            return

        Logger().info("H5Client: creating dataset for %s in %s", symbol, self.name)
        self.hf.create_dataset(symbol, (0, num_cols), maxshape=(None, num_cols), dtype="float64")
        self.hf.flush()

    def write_data(self, symbol: str, data: List[Tuple]):
        r, o = self.get_time_boundaries(symbol)

        filtered_data = []
        if r is not None:
            for row in data:
                if row[0] > r or row[0] < o:
                    filtered_data.append(row)
        else:
            filtered_data = data

        filtered_array = np.array(filtered_data)
        new_size = self.hf[symbol].shape[0] + filtered_array.shape[0]
        self.hf[symbol].resize(new_size, axis=0)
        self.hf[symbol][-filtered_array.shape[0]:] = filtered_array
        self.hf.flush()

    def append_df(self, symbol: str, data: pd.DataFrame):
        data_array = np.array(data)
        new_size = self.hf[symbol].shape[0] + data_array.shape[0]
        self.hf[symbol].resize(new_size, axis=0)
        self.hf[symbol][-data_array.shape[0]:] = data_array
        self.hf.flush()

    def get_data(self, symbol: str, from_time: int, to_time: int) -> None | pd.DataFrame:
        if symbol not in self.hf.keys():
            return None

        data = self.hf[symbol]
        df = pd.DataFrame(data, columns=['openTime', 'open', 'high', 'low', 'close', 'volume', 'closeTime'])
        df = df[(df['openTime'] >= from_time) & (df['openTime'] <= to_time)]
        df['openTime'] = pd.to_datetime(df['openTime'].values.astype(np.int64), unit='ms')
        df['closeTime'] = pd.to_datetime(df['closeTime'].values.astype(np.int64), unit='ms')
        df.set_index('openTime', drop=True, inplace=True)
        df.sort_index()
        return df

    def get_time_boundaries(self, symbol: str) -> Tuple:
        """
            returns (recent, oldest) sample time
        """
        data = np.array(self.hf[symbol])
        if len(data) == 0:
            return None, None
        else:
            r = max(data[:, 0])
            o = min(data[:, 0])
            return r, o
