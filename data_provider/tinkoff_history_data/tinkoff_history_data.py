import logging
from typing import Generator

from tinkoff.invest import HistoricCandle, Trade

from data_provider.base_data_provider import IDataProvider
from data_provider.tinkoff_history_data.csv_data_storage import CSVDataStorageReader

logger = logging.getLogger(__name__)

__all__ = ("TinkoffHistoryData")


class TinkoffHistoryData(IDataProvider):
    def __init__(self, root_path: str) -> None:
        self.__data_reader = CSVDataStorageReader(root_path)

    def provide_candles(self, figi: str, from_days: int) -> Generator[HistoricCandle, None, None]:
        for candle in self.__data_reader.read_candles(figi, from_days):
            yield HistoricCandle(
                open=candle.open,
                high=candle.high,
                low=candle.low,
                close=candle.close,
                volume=candle.volume,
                time=candle.time,
                is_complete=True
            )

    def provide_trades(self, figi: str, from_days: int) -> Generator[Trade, None, None]:
        yield None
