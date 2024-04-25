import prometheus_client
from irsdk import IRSDK
from labels import Labels


class Meter:

    def __init__(self, name: str, description: str, labels: list[Labels], ir_key: str):
        self.name = name
        self.description = description
        self.labels = labels
        self.ir_key = ir_key
        self.init = False
        self.registry = None

    def init_meter(self, registry):
        if not self.init:
            self.init = True
            self.registry = registry

    def _get_merged_labels_keys(self) -> list[str]:
        merged_label_keys = []
        for label in self.labels:
            merged_label_keys.extend(label.get_keys())
        return merged_label_keys

    def _get_merged_labels_values(self, ir) -> list[str]:
        merged_label_values = []
        for label in self.labels:
            merged_label_values.extend(label.get_values(ir))
        return merged_label_values

    def set(self, ir: IRSDK):
        pass


class Gauge(Meter):
    gauge: prometheus_client.Gauge

    def __init__(self, name: str, description: str, labels: list[Labels], ir_key: str):
        super().__init__(name, description, labels, ir_key)

    def init_meter(self, registry):
        super().init_meter(registry)
        self.gauge = prometheus_client.Gauge(self.name, self.description,
                                             self._get_merged_labels_keys(), registry=self.registry)

    def set(self, ir: IRSDK):
        return self.gauge.labels(*self._get_merged_labels_values(ir)).set(ir[self.ir_key])


class Counter(Meter):
    counter: prometheus_client.Counter

    def __init__(self, name: str, description: str, labels: list[Labels], ir_key: str):
        super().__init__(name, description, labels, ir_key)

    def init_meter(self, registry):
        super().init_meter(registry)
        self.counter = prometheus_client.Counter(self.name, self.description,
                                                 self._get_merged_labels_keys(), registry=self.registry)

    def set(self, ir: IRSDK):
        return self.counter.labels(*self._get_merged_labels_values(ir)).inc(ir[self.ir_key])
