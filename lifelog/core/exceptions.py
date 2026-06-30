
class EntryNotFoundError(Exception):
    """Raised when a requested entry ID does not exist in the database."""
    def __init__(self, entry_id):
        self.entry_id = entry_id
        self.message = f"Entry with ID '{entry_id}' was not found."
        super().__init__(self.message)
