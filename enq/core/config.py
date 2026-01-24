import tomllib
import logging
import os

from pathlib import Path
from importlib import resources
from platformdirs import user_config_dir

from enq.core.constants import DEFAULT_CONFIG_NAME, CONFIG_TEMPLATE_NAME

logger = logging.getLogger(__name__)

IS_DEBUG = os.getenv("DEBUG") == "1"


class Config:
    def __init__(self, user_provided_path: str):
        dev_path = Path(__file__).parent.parent / DEFAULT_CONFIG_NAME
        proper_path = Path(user_config_dir("enq")) / DEFAULT_CONFIG_NAME

        default_path = dev_path if IS_DEBUG else proper_path

        self.config_file = self._resolve_config_path(user_provided_path, default_path)

        logger.debug(f"Using config file: {str(self.config_file)}")
        self.data = self._load_config()
        self.settings = self.data["settings"]
        self.paths = self.data["paths"]

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

        if not default_path.exists():
            logger.debug(f"Could not find config file {str(self.config_file)}")
            self._create_default_config()

        return default_path

    def _load_config(self):
        self.config_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.config_file, "rb") as f:
            return tomllib.load(f)

    def _create_default_config(self):
        template = resources.files("enq.assets").joinpath(CONFIG_TEMPLATE_NAME)

        self.config_file.write_bytes(template.read_bytes())

        logger.debug(f"Created default config at {self.config_file}")
