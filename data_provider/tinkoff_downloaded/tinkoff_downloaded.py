import logging
from typing import Generator

from tinkoff.invest import HistoricCandle, Trade

from data_provider.base_data_provider import IDataProvider
from data_provider.tinkoff_downloaded.csv_data_storage import CSVDataStorageReader

__all__ = ("TinkoffDownloaded")

logger = logging.getLogger(__name__)


class TinkoffDownloaded(IDataProvider):
    """Data provider for downloaded market data by (data_collectors\tinkoff_stream_py) project"""
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
        for trade in self.__data_reader.read_trade(figi, from_days):
            yield trade
