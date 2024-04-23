import os
import yaml

CONFIG_FILE = os.getenv('CONFIG_FILE', 'config.yaml')


class _MetricConfig:
    # The name of the metric
    name: str
    # The description of the metric
    desc: str
    # The meta_lables should be added to the metric default true
    add_meta_labels: bool
    # The key to get the metric from the IRSDK,
    # use the example export for finding the key (if it's a multi level key use the dot notation)
    ir_key: str
    # The labels to add to the metrics
    labels: dict[str, str]

class _TelemetryConfig:
    # The labels that will be added to each metric, that sent down.
    # The key should be the name of the irsdk variable, the value should be the name of the label
    # It can have any depth.
    meta_labels: dict[str, str]


class _Config:
    # The url of the prometheus push gateway example: http://localhost:9091
    push_gw_url: str
    # The ide of the client that send the data, this can be your name for example
    # or an id, if not given a random uuid will be generated
    client_id: str
    # The telemetry config
    telemetry: _TelemetryConfig


class Config:
    config: _Config

    def __init__(self):
        self.load()

    def load(self):
        with open(CONFIG_FILE, 'r') as file:
            self.config = yaml.safe_load(file)
        pass
