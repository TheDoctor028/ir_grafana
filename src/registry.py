from prometheus_client.registry import CollectorRegistry, RestrictedRegistry
from telemetry import Meter

registry = CollectorRegistry()
per_tick_registry = RestrictedRegistry(['tick'], registry)
per_lap_registry = RestrictedRegistry(['laptime'], registry)


class Registry:
    def __init__(self, per_tick_metrics: list[Meter], per_lap_metrics: list[Meter]):
        self.per_tick_metrics = per_tick_metrics
        self.per_lap_metrics = per_lap_metrics

    def get_registry(self):
        return registry

    def get_per_tick_registry(self):
        return per_tick_registry

    def get_per_lap_registry(self):
        return per_lap_registry
