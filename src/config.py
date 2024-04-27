import os
import yaml

CONFIG_FILE = os.getenv('CONFIG_FILE', f'{os.getcwd()}//config.yaml')


class Config:
    _config: dict

    def __init__(self):
        self.load()

    def __getitem__(self, item):
        if item not in self._config:
            return None
        return self._config[item]

    def load(self):
        try:
            with open(CONFIG_FILE, 'r') as file:
                self._config = yaml.safe_load(file)
        except Exception as e:
            print(f"Error loading config: {e}\n" +
                  f"Make sure you have a config.yaml file in the working directory ({os.getcwd()})." +
                  f"Or set the CONFIG_FILE environment variable to the path of the config file."
                  )
            exit(1)

    def job_name(self):
        return 'iracing_telemetry_client_' + self._config['client_id']
