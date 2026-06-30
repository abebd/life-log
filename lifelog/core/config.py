import tomllib
import logging
import os

from pathlib import Path
from importlib import resources
from platformdirs import user_config_dir

from lifelog.core.constants import DEFAULT_CONFIG_NAME, REL_PATH_TO_DEFAULT_CONFIG

logger = logging.getLogger(__name__)

DEBUG_MODE = os.getenv("DEBUG_MODE") == "1"


class Config:

    def __init__(self, user_provided_path: str):
        if DEBUG_MODE:
            default_path = (
                Path(__file__).parent.parent.parent / f"dev_{DEFAULT_CONFIG_NAME}"
            )
        else:
            default_path = Path(user_config_dir("lifelog")) / DEFAULT_CONFIG_NAME

        self.default_config = Path(__file__).parent.parent/ REL_PATH_TO_DEFAULT_CONFIG
        self.user_config = self._resolve_config_path(user_provided_path, default_path)

        self.data = self._load_config()
        self.flush_to_logger()

        self.settings = self.data["settings"]
        self.paths = self.data["paths"]
        self.storage = self.data["storage"]
        self.menu = self.data["menu"]

    def _resolve_config_path(self, user_provided_path: str, default_path: Path):
        if user_provided_path:
            user_path = Path(user_provided_path)
            if user_path.exists():
                return user_path
            else:
                logger.error(
                    f"Explicitly provided config file not found: {user_provided_path}"
                )
                raise FileNotFoundError(
                    f"Could not find config file {user_provided_path}"
                )

        return default_path

    def _load_config(self):
        self.user_config.parent.mkdir(parents=True, exist_ok=True)

        config_data = tomllib.load(
            open(self.default_config, "rb")
        )

        if self.user_config.exists():
            config_data = config_data | tomllib.load(
                open(self.user_config, "rb")
            )

        return config_data

    def _create_default_config(self, default_path):
        template = Path(REL_PATH_TO_DEFAULT_CONFIG)

        default_path.parent.mkdir(parents=True, exist_ok=True)
        default_path.write_bytes(template.read_bytes())

        logger.info(f"Created default config at {default_path}")


    def flush_to_logger(self):
        logger.info(f"Using config file: {self.user_config}")
        logger.info("-" * 40)

        for key, value in self.data.items():
            logger.info(f"    {key:<20} : {value}")

        logger.info("-" * 40)
