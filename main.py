import logging
import os
from logging.handlers import RotatingFileHandler

from analyze.analyze_provider_factory import AnalyzeProviderFactory
from configuration.configuration import ProgramConfiguration
from data_provider.data_provider_factory import DataProviderFactory
from runner.runner import Runner

# the configuration file name
CONFIG_FILE = "settings.ini"
logger = logging.getLogger(__name__)


def prepare_logs() -> None:
    if not os.path.exists("logs/"):
        os.makedirs("logs/")

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
        handlers=[RotatingFileHandler('logs/analyze.log', maxBytes=100000000, backupCount=10, encoding='utf-8')],
        encoding="utf-8"
    )


if __name__ == "__main__":
    prepare_logs()

    logger.info("Analyze has been started.")

    try:
        config = ProgramConfiguration(CONFIG_FILE)
        logger.info("Configuration has been loaded")
    except Exception as ex:
        logger.critical("Load configuration error: %s", repr(ex))
    else:
        # create data provider
        data_provider = DataProviderFactory.new_factory(
            config.data_provider_settings.name,
            config.data_provider_settings.root_path
        )
        # create analyze provider by provider_name
        analyze_provider = AnalyzeProviderFactory.new_factory(
            config.analyze_settings.provider_name,
            data_provider,
            *config.analyze_provider_settings
        )

        # run analyze
        Runner(analyze_provider).run_analyze(config.analyze_settings.figi, config.analyze_settings.from_days)

    logger.info("Analyze has been ended")
