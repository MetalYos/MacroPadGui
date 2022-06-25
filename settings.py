import json
from dataclasses import dataclass, field


@dataclass
class Settings:
    settings: dict = field(default_factory=dict)

    def __post_init__(self):
        self.settings_file_path = "settings.json"

    def load_settings(self):
        with open(self.settings_file_path, 'r') as f:
            self.settings = json.loads(f.read())
    
    def save_settings(self):
        with open(self.settings_file_path, 'w') as f:
            settings_str = json.dumps(self.settings)
            f.write(settings_str)
    
    def __getitem__(self, item):
        return self.settings[item]
