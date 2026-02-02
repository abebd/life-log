import logging
from pathlib import Path


def setup_logging(verbose: bool):
    # 1. Determine the path: ~/git/repo-name/logs/app.log
    # Path(__file__) gets the location of logger.py
    project_root = Path(__file__).parent.parent
    log_dir = project_root / "logs"

    # Create the directory if it doesn't exist
    log_dir.mkdir(parents=True, exist_ok=True)
    log_filepath = log_dir / "app.log"

    # 2. Define Formats
    file_format = logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    shell_format = logging.Formatter("%(levelname)s: %(message)s")

    # 3. Setup the Root Logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)  # Catch everything

    # 4. File Handler (Always DEBUG)
    f_handler = logging.FileHandler(log_filepath, mode="w")
    f_handler.setLevel(logging.DEBUG)
    f_handler.setFormatter(file_format)
    root_logger.addHandler(f_handler)

    # 5. Console Handler (Level based on --verbose)
    c_handler = logging.StreamHandler()
    c_handler.setLevel(logging.ERROR)
    c_handler.setFormatter(shell_format)
    root_logger.addHandler(c_handler)
