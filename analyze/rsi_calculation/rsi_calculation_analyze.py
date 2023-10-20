import logging
from dataclasses import dataclass
from datetime import datetime

import pandas as pd
from tinkoff.invest.utils import quotation_to_decimal

from analyze.base_analyze_provider import IAnalyzeProvider
from data_provider.base_data_provider import IDataProvider

__all__ = ("RsiCalculation")
logger = logging.getLogger(__name__)


@dataclass(eq=False, repr=True)
class FloatCandle:
    """Data class for Pandas calculations.
    float type is a mistake and shame. Using it just for example.
    Do not use it in production code.
    """
    open: float
    high: float
    low: float
    close: float
    volume: int
    time: datetime


class RsiCalculation(IAnalyzeProvider):
    """An EXAMPLE of self-made indicator: RSI indicator as one of most famous indicator worldwide"""
    def __init__(
            self,
            data_provider: IDataProvider,
            # all variables below in passed as *args (str)
            length: str,
            source: str,
            output_file: str
    ) -> None:
        self.__data_provider = data_provider

        self.__length = int(length)
        self.__source = source
        self.__output_file = output_file

    def start(self, figi: str, from_days: int) -> None:
        logger.info(f"RsiCalculation start; figi:{figi}; from_days:{from_days}; length:{self.__length}")

        logger.info(f"Fill candles")
        candles: list[FloatCandle] = []
        for candle in self.__data_provider.provide_candles(figi, from_days):
            candles.append(
                FloatCandle(
                    open=float(quotation_to_decimal(candle.open)),
                    high=float(quotation_to_decimal(candle.high)),
                    low=float(quotation_to_decimal(candle.low)),
                    close=float(quotation_to_decimal(candle.close)),
                    volume=candle.volume,
                    time=candle.time
                )
            )

        if not candles:
            logger.info(f"Stop RSI calculation. Candles weren't found.")
            return

        logger.info(f"Start RSI calculation")
        candles_rsi = self.__calculate_rsi(pd.DataFrame(candles))

        # Save full result to file and log
        try:
            if self.__output_file:
                logger.info(f"Save candles with rsi to file {self.__output_file}")
                candles_rsi.to_csv(self.__output_file)
        except Exception as ex:
            logger.error(f"Error while save candles with rsi {repr(ex)}")

        logger.info(f"Result as Data Frame:")
        logger.info(candles_rsi)

        logger.info(f"RsiCalculation ended")

    def __calculate_rsi(
            self,
            candles: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Wells Wilder's RSI calculation developed via the Pandas library.
        Based on: https://github.com/alphazwest
        """

        # Calculate Price Differences using the column specified as price (self.__source).
        candles['diff'] = candles[self.__source].diff(1)

        # Calculate Avg. Gains/Losses
        candles['gain'] = candles['diff'].clip(lower=0)
        candles['loss'] = candles['diff'].clip(upper=0).abs()

        # Get initial Averages
        candles['avg_gain'] = candles['gain'].rolling(window=self.__length, min_periods=self.__length).mean()[:self.__length + 1]
        candles['avg_loss'] = candles['loss'].rolling(window=self.__length, min_periods=self.__length).mean()[:self.__length + 1]
        candles['avg_loss_no_slice'] = candles['loss'].rolling(window=self.__length, min_periods=self.__length).mean()

        # Calculate Average Gains
        for i, row in enumerate(candles['avg_gain'].iloc[self.__length + 1:]):
            candles['avg_gain'].iloc[i + self.__length + 1] = \
                (candles['avg_gain'].iloc[i + self.__length] *
                 (self.__length - 1) +
                 candles['gain'].iloc[i + self.__length + 1]) \
                / self.__length

        # Calculate Average Losses
        for i, row in enumerate(candles['avg_loss'].iloc[self.__length + 1:]):
            candles['avg_loss'].iloc[i + self.__length + 1] = \
                (candles['avg_loss'].iloc[i + self.__length] *
                 (self.__length - 1) +
                 candles['loss'].iloc[i + self.__length + 1]) \
                / self.__length

        # Calculate RS Values
        candles['rs'] = candles['avg_gain'] / candles['avg_loss']

        # Calculate RSI
        candles['rsi'] = 100 - (100 / (1.0 + candles['rs']))

        return candles
