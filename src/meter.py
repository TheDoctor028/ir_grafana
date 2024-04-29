import prometheus_client
from irsdk import IRSDK
from labels import Labels


class Meter:

    def __init__(self, name: str, description: str, labels: list[Labels], ir_key: str,
                 value_map: lambda v: v = lambda v: v):
        self.name = name
        self.description = description
        self.labels = labels
        self.ir_key = ir_key
        self.init = False
        self.registry = None
        self.value_map = value_map

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

    def _get_value_from_ir(self, ir: IRSDK):
        keys = self.ir_key.split('.')
        t_res = ir
        for key in keys:
            try:
                t_res = t_res[key]
            except KeyError:
                return -100

        return self.value_map(t_res)


class Gauge(Meter):
    gauge: prometheus_client.Gauge

    def __init__(self, name: str, description: str, labels: list[Labels], ir_key: str,
                 value_map: lambda v: v = lambda v: v):
        super().__init__(name, description, labels, ir_key, value_map)

    def init_meter(self, registry):
        super().init_meter(registry)
        self.gauge = prometheus_client.Gauge(self.name, self.description,
                                             self._get_merged_labels_keys(), registry=self.registry)

    def set(self, ir: IRSDK):
        return self.gauge.labels(*self._get_merged_labels_values(ir)).set(self._get_value_from_ir(ir))


class Counter(Meter):
    counter: prometheus_client.Counter

    def __init__(self, name: str, description: str, labels: list[Labels], ir_key: str,
                 value_map: lambda v: v = lambda v: v):
        super().__init__(name, description, labels, ir_key, value_map)

    def init_meter(self, registry):
        super().init_meter(registry)
        self.counter = prometheus_client.Counter(self.name, self.description,
                                                 self._get_merged_labels_keys(), registry=self.registry)

    def set(self, ir: IRSDK):
        return self.counter.labels(*self._get_merged_labels_values(ir)).inc(self._get_value_from_ir(ir))
