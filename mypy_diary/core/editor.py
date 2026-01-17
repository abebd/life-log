import shutil
import subprocess

from pathlib import Path

from mypy_diary.core.config import Config


class Editor:
    def __init__(self, config: Config):
        self.config = config
        self.editor = self._get_editor()

    def _get_editor(self):
        editor = self.config.settings["editor"]

        if shutil.which(editor) is None:
            raise FileNotFoundError(f"Editor '{editor}' not found in your system.")
        return editor

    def open(self, file_path: Path):
        try:
            subprocess.run([self.editor, str(file_path)], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Editor exited with an error: {e}")
