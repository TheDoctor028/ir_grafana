import prometheus_client

META_LABELS = {
    "WeekendInfo": {
        "TrackID": "track_id",
        "SeriesID": "series_id",
        "SeasonID": "season_id",
        "SessionID": "session_id",
        "SubSessionID": "subsession_id",
    },
}


class Labels:
    def __init__(self, labels: dict):
        self.labels = labels

    def _get_keys(self, d):
        ks = []
        for key, value in d.items():
            if type(value) is dict:
                ks.extend(self._get_keys(value))
            else:
                ks.append(value)
        return ks

    def get_keys(self):
        return self._get_keys(self.labels)

    def _get_values(self, d, ir):
        vs = []
        for key, value in d.items():
            if type(value) is dict:
                vs.extend(self._get_values(value, ir[key]))
            else:
                vs.append(ir[key])
        return vs

    def get_values(self, ir):
        return self._get_values(self.labels, ir)


class Meter:

    def __init__(self, name: str, description: str, labels: list[Labels], registry):
        self.name = name
        self.description = description
        self.labels = labels
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

    def get_meter(self):
        pass


class Gauge(Meter):

    def __init__(self, name: str, description: str, labels: list[Labels], registry):
        super().__init__(name, description, labels, registry)
        self.gauge = prometheus_client.Gauge(name, description, self._get_merged_labels_keys(), registry=self.registry)

    def get_meter(self):
        return self.gauge


class Counter(Meter):

    def __init__(self, name: str, description: str, labels: list[Labels], registry):
        super().__init__(name, description, labels, registry)
        self.counter = prometheus_client.Counter(name, description,
                                                 self._get_merged_labels_keys(), registry=self.registry)

    def get_meter(self):
        return self.counter
