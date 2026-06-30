import shutil
import subprocess
import tempfile

from pathlib import Path

from lifelog.cli.interface import ui, State


class Editor:
    def __init__(self, editor_name):
        self.editor = editor_name
        self._verify_editor()

    def _verify_editor(self):
        if shutil.which(self.editor) is None:
            raise FileNotFoundError(f"Editor '{self.editor}' not found in your system.")

    def open(self, file_path: Path):
        try:
            ui.state = State.IN_EDITOR
            subprocess.run([self.editor, str(file_path)], check=True)
            ui.reset_state()
        except subprocess.CalledProcessError as e:
            print(f"Editor exited with an error: {e}")

    def edit_text(self, initial_content: str) -> str:
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".tmp") as tf:
                temp_path = Path(tf.name)
                tf.write(initial_content)
            
            self.open(temp_path)

            return temp_path.read_text(encoding="utf-8")

        finally:
            if temp_path and temp_path.exists():
                temp_path.unlink()
