from prometheus_client.registry import CollectorRegistry, RestrictedRegistry

registry = CollectorRegistry()
per_tick_registry = RestrictedRegistry(['tick'], registry)
per_lap_registry = RestrictedRegistry(['laptime'], registry)


def get_job_name(c) -> str:
    return 'iracing_telemetry_client_' + c.config.client_id


class Registry:
    def __init__(self, per_tick_metrics: list[str], per_lap_metrics: list[str]):
        self.per_tick_metrics = per_tick_metrics
        self.per_lap_metrics = per_lap_metrics

    def get_registry(self):
        return registry

    def get_per_tick_registry(self):
        return per_tick_registry

    def get_per_lap_registry(self):
        return per_lap_registry
