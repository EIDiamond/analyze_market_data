import logging

from analyze.base_analyze_provider import IAnalyzeProvider

logger = logging.getLogger(__name__)


class Runner:
    def __init__(self, analyze_provider: IAnalyzeProvider) -> None:
        self.analyze_provider = analyze_provider

    def run_analyze(self, figi: str, from_days: int) -> None:
        logger.info(f"Start analyze")

        try:
            self.analyze_provider.start(figi, from_days)
        except Exception as ex:
            logger.error(f"Error while analyze: {repr(ex)}")
        else:
            logger.info(f"Analyze has been completed successfully")
