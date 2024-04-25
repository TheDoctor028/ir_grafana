import os
import yaml

CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.yaml')


class Config:
    config: dict

    def __init__(self):
        self.load()

    def load(self):
        with open(CONFIG_FILE, 'r') as file:
            self.config = yaml.safe_load(file)
        pass

    def job_name(self):
        return 'iracing_telemetry_client_' + self.config['client_id']
