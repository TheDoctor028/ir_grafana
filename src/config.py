import os
import yaml

CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.yaml')


class Config:
    _config: dict

    def __init__(self):
        self.load()

    def __getitem__(self, item):
        if item not in self._config:
            return None
        return self._config[item]

    def load(self):
        with open(CONFIG_FILE, 'r') as file:
            self._config = yaml.safe_load(file)
        pass

    def job_name(self):
        return 'iracing_telemetry_client_' + self._config['client_id']
