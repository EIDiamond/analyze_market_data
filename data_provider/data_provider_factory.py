from data_provider.base_data_provider import IDataProvider
from data_provider.tinkoff_downloaded.tinkoff_downloaded import TinkoffDownloaded
from data_provider.tinkoff_history_data.tinkoff_history_data import TinkoffHistoryData


__all__ = ("DataProviderFactory")


class DataProviderFactory:
    """
    Fabric for data providers. Put here a new data provider.
    """
    @staticmethod
    def new_factory(provider_name: str, *args, **kwargs) -> IDataProvider:
        match provider_name:
            case "TinkoffDownloaded":
                return TinkoffDownloaded(*args, **kwargs)
            case "TinkoffHistoryData":
                return TinkoffHistoryData(*args, **kwargs)
            case _:
                return TinkoffDownloaded(*args, **kwargs)
