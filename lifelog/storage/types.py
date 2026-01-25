from enum import Enum, auto


class StorageType(Enum):
    DATABASE = auto()
    FILE = auto()


def resolve_storage_type_from_string(storage_type):
    match storage_type:
        case "database":
            return StorageType.DATABASE

        case "file":
            return StorageType.FILE
