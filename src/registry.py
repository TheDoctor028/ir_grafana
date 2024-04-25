from prometheus_client.registry import CollectorRegistry, RestrictedRegistry
from meter import Meter


class Registry:
    def __init__(self, per_tick_metrics: list[Meter], per_lap_metrics: list[Meter]):
        self.registry = CollectorRegistry()
        self.per_tick_metrics = per_tick_metrics
        self.per_lap_metrics = per_lap_metrics
        self.per_tick_registry = RestrictedRegistry([m.name for m in per_tick_metrics], self.registry)
        self.per_lap_registry = RestrictedRegistry([m.name for m in per_lap_metrics], self.registry)
        for m in per_tick_metrics:
            m.init_meter(self.registry)
        for m in per_lap_metrics:
            m.init_meter(self.registry)
