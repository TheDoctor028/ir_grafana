import time

from irsdk import IRSDK
from registry import Registry


class Telemetry:
    def __init__(self, ir: IRSDK, r: Registry, tick_interval: int = 1):
        self.ir = ir
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
        time.sleep(self.tick_interval)
        pass

    def _tick_lap(self):
        for m in self.registry.per_lap_metrics:
            m.set(self.ir)
        pass
