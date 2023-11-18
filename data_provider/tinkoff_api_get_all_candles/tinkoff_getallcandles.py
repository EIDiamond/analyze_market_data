import datetime
import logging
from typing import Generator

from tinkoff.invest import HistoricCandle, Trade, CandleInterval

from data_provider.base_data_provider import IDataProvider
from tinkoff_api.services.client_service import ClientService

logger = logging.getLogger(__name__)

__all__ = ("TinkoffAPIGetAllCandles")


class TinkoffAPIGetAllCandles(IDataProvider):
    def __init__(
            self,
            token: str
    ) -> None:
        self.__client_service = ClientService(
            token,
            "EIDiamond.analyze_market_data"
        )

    def provide_candles(self, figi: str, from_days: int) -> Generator[HistoricCandle, None, None]:
        today = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
        today_morning = datetime.datetime(year=today.year, month=today.month, day=today.day,
                                          hour=6, minute=0, second=0, tzinfo=datetime.timezone.utc)

        for day_number in range(from_days, -1, -1):
            from_date = today_morning - datetime.timedelta(days=day_number)
            to_date = from_date + datetime.timedelta(days=1)

            if from_date.weekday() in [5, 6]:
                logger.info(f"Weekend collection was skipped: from date is {from_date}")
                continue

            for candle in self.__client_service.download_historic_candle(
                    figi=figi,
                    from_=from_date,
                    to_=to_date,
                    interval=CandleInterval.CANDLE_INTERVAL_1_MIN
            ):
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
