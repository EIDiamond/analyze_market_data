import datetime
import logging

from tinkoff.invest import CandleInterval, Client, HistoricCandle

from tinkoff_api.invest_error_decorators import invest_api_retry, invest_error_logging

__all__ = ("ClientService")

logger = logging.getLogger(__name__)


class ClientService:
    """
    The class encapsulate tinkoff client api
    """
    def __init__(self, token: str, app_name: str) -> None:
        self.__token = token
        self.__app_name = app_name

    @invest_api_retry()
    @invest_error_logging
    def download_historic_candle(
            self,
            figi: str,
            from_: datetime,
            to_: datetime,
            interval: CandleInterval
    ) -> list[HistoricCandle]:
        """Download and return all requested historical candles"""
        result: list[HistoricCandle] = []

        logger.info(f"Start download recent candles. Figi: {figi}, from: {from_}, to: {to_}, interval: {interval.name}")

        with Client(self.__token, app_name=self.__app_name) as client:
            for candle in client.get_all_candles(
                    figi=figi,
                    from_=from_,
                    to=to_,
                    interval=interval
            ):
                logger.debug(candle)

                result.append(candle)

        logger.info(f"Download complete: candles count {len(result)}")

        return result
