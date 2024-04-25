from prometheus_client import Gauge
from src.registry import registry


client_last_write = Gauge('client_last_export_unix_ts',
                          'Last time the client exported telemetry data',
                          registry=registry)


