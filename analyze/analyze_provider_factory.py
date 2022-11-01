from typing import Optional

from analyze.base_analyze_provider import IAnalyzeProvider
from analyze.rsi_calculation.rsi_calculation_analyze import RsiCalculation

__all__ = ("AnalyzeProviderFactory")


class AnalyzeProviderFactory:
    """
    Fabric for analyze providers. Put here a new analysis provider.
    """
    @staticmethod
    def new_factory(provider_name: str, *args, **kwargs) -> Optional[IAnalyzeProvider]:
        match provider_name:
            case "RSI_CALCULATION":
                return RsiCalculation(*args, **kwargs)
            case _:
                return None
