from dataclasses import dataclass

__all__ = ("DataProviderSettings", "AnalyzeSettings")


@dataclass(eq=False, repr=True)
class DataProviderSettings:
    root_path: str = ""


@dataclass(eq=False, repr=True)
class AnalyzeSettings:
    from_days: int = 7
    figi: str = ""
    provider_name: str = ""
