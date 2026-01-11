import tomllib
import logging

from pathlib import Path
from importlib import resources
from platformdirs import user_config_dir
from mypy_diary.extra import get_project_root

logger = logging.getLogger(__name__)

class Config:

    def __init__(self):

        self.config_dir = Path(user_config_dir("mypy-diary"))
        self.config_file = self.config_dir / "config.toml"

        logger.debug("Using config file: " + str(self.config_file))

        self.data = self._load_config()
        self.settings = self.data["settings"]
        self.paths = self.data["paths"]

    def _load_config(self):

        self.config_dir.mkdir(parents=True, exist_ok=True)

        if not self.config_file.exists():
            self._create_default_config()

        with open(self.config_file, "rb") as f:
            return tomllib.load(f)


    def _create_default_config(self):

        template = resources.files("mypy_diary.assets").joinpath("default_config.toml")

        self.config_file.write_bytes(template.read_bytes())

        logger.debug(f"Created default config at {self.config_file}")

