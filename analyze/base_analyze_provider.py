import abc

__all__ = ("IAnalyzeProvider")


class IAnalyzeProvider(abc.ABC):
    """Interface for different analyze providers"""
    @abc.abstractmethod
    def start(self, figi: str, from_days: int) -> None:
        pass
