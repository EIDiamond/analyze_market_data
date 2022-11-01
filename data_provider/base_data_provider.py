import abc
from typing import Generator

from tinkoff.invest import HistoricCandle, Trade

__all__ = ("IDataProvider")


class IDataProvider(abc.ABC):
    """Interface for different data providers: files, db, api etc."""
    @abc.abstractmethod
    def provide_candles(self, figi: str, from_days: int) -> Generator[HistoricCandle, None, None]:
        pass

    @abc.abstractmethod
    def provide_trades(self, figi: str, from_days: int) -> Generator[Trade, None, None]:
        pass
