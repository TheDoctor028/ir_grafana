from irsdk import IRSDK
from prometheus_client import Gauge, Counter
from meters.registry import registry

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
