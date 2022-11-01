from configparser import ConfigParser
from typing import ValuesView

from configuration.settings import DataProviderSettings, AnalyzeSettings

__all__ = ("ProgramConfiguration")


class ProgramConfiguration:
    """
    Represent program configuration
    """
    def __init__(self, file_name: str) -> None:
        # classic ini file
        config = ConfigParser()
        config.read(file_name)

        self.__data_provider_settings = DataProviderSettings(
            root_path=config["DATA_PROVIDER"]["ROOT_PATH"]
        )

        self.__analyze_settings = AnalyzeSettings(
            from_days=int(config["ANALYZE"]["FROM_DAYS"]),
            figi=config["ANALYZE"]["FIGI"],
            provider_name=config["ANALYZE"]["PROVIDER_NAME"]
        )

        # values are used as *arg in init method of provider class
        self.__analyze_provider_settings = config[self.__analyze_settings.provider_name].values()

    @property
    def data_provider_settings(self) -> DataProviderSettings:
        return self.__data_provider_settings

    @property
    def analyze_settings(self) -> AnalyzeSettings:
        return self.__analyze_settings

    @property
    def analyze_provider_settings(self) -> ValuesView[str]:
        return self.__analyze_provider_settings
