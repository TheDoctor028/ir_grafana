import time

from irsdk import IRSDK
from registry import Registry
from prometheus_client import push_to_gateway
from config import Config


class Telemetry:
    def __init__(self, ir: IRSDK, c: Config, r: Registry, tick_interval: int = 1):
        self.ir = ir
        self.config = c
        self.registry = r
        self._lap = 0
        self._last_processed_lap = -1
        self.tick_interval = tick_interval

    def start(self):
        while True:
            self._tick()
            if self._lap > self._last_processed_lap:
                self._tick_lap()
                self._lap = self.ir['Lap']

    def _tick(self):
        for m in self.registry.per_tick_metrics:
            m.set(self.ir)
        push_to_gateway(self.config['push_gw_url'], job=self.config.job_name(),
                        registry=self.registry.per_tick_registry)
        time.sleep(self.tick_interval)

    def _tick_lap(self):
        for m in self.registry.per_lap_metrics:
            m.set(self.ir)
        push_to_gateway(self.config['push_gw_url'], job=self.config.job_name(),
                        registry=self.registry.per_lap_registry)
