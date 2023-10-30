import csv
import re
import datetime
import logging
from decimal import Decimal
from pathlib import Path
from typing import Generator

from tinkoff.invest import Candle
from tinkoff.invest.utils import decimal_to_quotation

__all__ = ("CSVDataStorageReader")

logger = logging.getLogger(__name__)


class CSVDataStorageReader:
    def __init__(self, root_path: str) -> None:
        self.__root_path = root_path

        if not self.__root_path:
            logger.error(f"Storage reader init failed: root path is empty!")

            raise Exception(f"CSVDataStorageReader: root path is empty!")

    def read_candles(self, figi: str, from_days: int) -> Generator[Candle, None, None]:
        """
        Headers in candle csv file:
        guid, datetime (utc), open, close, high, low, volume
        """

        logger.info(f"Start read candles from root folder:{self.__root_path}, figi:{figi}, from_days:{from_days}")

        try:
            for row in self.__read_history_files(
                    from_days
            ):
                yield Candle(
                    figi=figi,
                    open=decimal_to_quotation(Decimal(row[2])),
                    high=decimal_to_quotation(Decimal(row[4])),
                    low=decimal_to_quotation(Decimal(row[5])),
                    close=decimal_to_quotation(Decimal(row[3])),
                    volume=int(row[6]),
                    time=datetime.datetime.strptime(row[1], '%Y-%m-%dT%H:%M:%S%z')  # 2023-01-03T07:00:00Z
                )
        except Exception as ex:
            logger.error(f"Error while read candle data from files: {repr(ex)}")

    def __read_history_files(self, from_days: int) -> Generator[str, None, None]:
        for data_file_path in self.__get_market_data_file_paths(
                from_days
        ):
            try:
                for row in CSVDataStorageReader.__read_data_file(data_file_path):
                    yield row
            except Exception as ex:
                logger.error(f"Error while read data from file {data_file_path}. "
                             f"File has been skipped: {repr(ex)}")

    def __get_market_data_file_paths(self, from_days: int) -> Generator[str, None, None]:
        root_dir = Path(self.__root_path)

        if root_dir.exists():
            from_ = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) - datetime.timedelta(days=from_days) \
                if from_days > 0 else datetime.datetime.min

            for file in sorted(root_dir.iterdir(), key=lambda x: str(x.name)):
                if file.is_dir():
                    continue

                if not file.match('*.csv'):
                    continue

                try:
                    m = re.search('_(.+?).csv', str(file.name))
                    if m:
                        found = m.group(1)

                        if from_ <= datetime.datetime.strptime(found, '%Y%m%d').replace(tzinfo=datetime.timezone.utc):
                            yield str(Path(self.__root_path, file.name))
                        else:
                            logger.info(f"File {file.name} was skipped by date filter.")
                except Exception as ex:
                    logger.error(f"File {file.name} doesn't match find pattern: {ex}.")
        else:
            logger.info(f"Root directory doesn't exist: {root_dir}.")

    @staticmethod
    def __read_data_file(file_name: str) -> Generator[list[str], None, None]:
        logger.debug(f"Read file: {file_name}")

        with open(file_name, encoding='UTF8', newline="") as file:
            #csv_reader = csv.reader(file)

            dialect = csv.Sniffer().sniff(file.read(1024))
            file.seek(0)
            csv_reader = csv.reader(file, dialect)

            for row in csv_reader:
                logger.debug(f"Read row: {row}")

                yield row
