import logging

from datetime import datetime
from pathlib import Path

from mypy_diary.core.config import Config
from mypy_diary.types import StorageType, resolve_type_from_string 

logger = logging.getLogger(__name__)

class MessageHandler:
    
    def __init__(self, config: Config):

        self.config = config
        self.diary_dir_path = Path(
            self.config.paths["diary_foler"]
        ).expanduser()

        self.today = datetime.now()

    def __call__(self, content):
        
        logger.debug("Message: " + content)

        #if do file
        if 1 == 1:
            self._create_diary_dir()
            file = self._get_file()


    def _create_diary_dir(self):

        if self.diary_dir_path.exists() == False:

            logger.debug(str(
                self.diary_dir_path) + " does not exist, creating it"
            )
            self.diary_dir_path.mkdir(parents=True)


    def _get_file(self):

        file_name = self.today.strftime("%Y_%m_%d")
        file_path = self.diary_dir_path / file_name

        #current_time = self.today.strftime("%H:%M")


class EntryHandler:
    
    def __init__(self, config):

        self.config = config
        self.type = resolve_type_from_string(
            type = self.config.settings["storage_mode"]    
        )

        self.entries = self._get_entries() #TODO might become slow in future


    def list_entries(self):

        for entry in self.entries:
            print(entry["name"])

    
    def add_entry(self):
        pass

        

    def _get_entries(self):
 
        match self.type:
            
            case StorageType.FILE:
                return self._get_entries_from_file()

            case StorageType.DATABASE:
                return self._get_entries_from_database()
            

    def _get_entries_from_file(self) -> list:
        
        diary_folder = Path(
            self.config.paths["diary_folder"]
        ).expanduser()

        sorted_files = sorted(
            diary_folder.glob("*.entry")
        )

        return [
            {
                "name": f.name, 
                "path": str(f.absolute())
            }
            for f in sorted_files
        ]
        

    def _get_entries_from_database(self) -> list:
        
        return [] # TODO


