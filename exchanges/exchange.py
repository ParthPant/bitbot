from abc import ABC, abstractmethod
from typing import Optional, List, Tuple


class Exchange(ABC):
    @abstractmethod
    def get_symbols(self):
        pass

    @abstractmethod
    def get_symbol_klines(self,
                          symbol: str,
                          interval: str,
                          starttime: Optional[int] = None,
                          endtime: Optional[int] = None,
                          limit: Optional[int] = None) -> List[Tuple]:
        pass

    @abstractmethod
    def fetch_symbols(self, update: bool = False):
        pass

    @abstractmethod
    def __str__(self):
        pass
