import json
from pathlib import Path


_singleton = None


def get_instance():
    """
    Getter of singleton class.

    Returns
    -------
    class
        instance of AppSettings class.
    """
    global _singleton
    if _singleton is None:
        _singleton = AppSettings()
    return _singleton


class AppSettings:
    """
    Singleton class. Do not instantiate.
    """
    def __init__(self):
        self.settings_path = "./settings.json"
        if not Path(self.settings_path).is_file():
            # TODO implement creation of settings dictionary
            pass
        with open(self.settings_path) as f:
            self.settings = json.load(f)
