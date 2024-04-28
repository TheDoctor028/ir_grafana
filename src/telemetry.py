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
        self._last_processed_lap = 0  # Lap 0 is not exists since when u left the pit it will be 1 instantly
        self.tick_interval = tick_interval

    def start(self):
        while True:
            if not self.ir.is_connected:
                print("iRacing not connected, waiting...")
                time.sleep(10)
                self.ir.startup()
                continue

            self.ir.freeze_var_buffer_latest()
            self._tick()
            self._lap = self.ir['Lap']
            if self._lap > self._last_processed_lap:
                self._tick_lap()
            self.ir.unfreeze_var_buffer_latest()

    def _tick(self):
        for m in self.registry.per_tick_metrics:
            m.set(self.ir)
        # print(f"Pushing metrics to {self.config['push_gw_url']}")
        push_to_gateway(self.config['push_gw_url'], job=self.config.job_name(),
                        registry=self.registry.registry)
        time.sleep(self.tick_interval)

    def _tick_lap(self):
        if self.config['dump_per_lap_metrics']:
            self.dump_per_lap_metrics()
        for m in self.registry.per_lap_metrics:
            m.set(self.ir)
        self._last_processed_lap = self.ir['Lap']
        print(f"Pushing metrics to {self.config['push_gw_url']} for lap {self._last_processed_lap}")
        push_to_gateway(self.config['push_gw_url'], job=self.config.job_name(),
                        registry=self.registry.registry)

    def dump_per_lap_metrics(self):
        self.ir.parse_yaml_async = True
        self.ir.parse_to(f'reports//{self._lap}_report.yaml')

