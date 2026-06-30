import textwrap

class TagHandler():
    def __init__(self, app, config):
        self.app = app
        self.config = config

    def ask_user_for_tags(self):
        pass

    def tag_entry(self, entry):
        pass
    
    def get_tagging_template(self):
        return textwrap.dedent(f"""\
            # Write the tags you wish to add to this entry on the empty line above:
            # Example: 'fitness, healthy, happy, good day'
            ################################################""").strip()

    def apply_tags(self, tags, entry):
        for tag in tags:
            self.app.storage.add_tag(tag, entry)

