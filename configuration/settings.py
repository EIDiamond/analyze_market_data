from dataclasses import dataclass

__all__ = ("AnalyzeSettings")


@dataclass(eq=False, repr=True)
class AnalyzeSettings:
    from_days: int = 7
    figi: str = ""
    provider_name: str = ""
