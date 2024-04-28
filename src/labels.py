import uuid

_META_LABELS = {
    "WeekendInfo": {
        "TrackID": "track_id",
        "SeriesID": "series_id",
        "SeasonID": "season_id",
        "SessionID": "session_id",
        "SubSessionID": "subsession_id",
    },
}

_PER_LAP_LABELS = {
    "Lap": ["lap", lambda v: v-1],
}


class Labels:
    def __init__(self, labels: dict):
        self.labels = labels

    def get_keys(self):
        return self.labels.keys()

    def get_values(self, ir):
        return self.labels.values()


class ExtractedLabels(Labels):
    def __init__(self, labels: dict):
        super().__init__(labels)

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


class ModifiedExtractedLabels(Labels):
    def __init__(self, labels: dict):
        super().__init__(labels)

    def _get_keys(self, d):
        ks = []
        for key, value in d.items():
            if type(value) is dict:
                ks.extend(self._get_keys(value))
            else:
                ks.append(value[0])
        return ks

    def get_keys(self):
        return self._get_keys(self.labels)

    def _get_values(self, d, ir):
        vs = []
        for key, value in d.items():
            if type(value) is dict:
                vs.extend(self._get_values(value, ir[key]))
            else:
                vs.append(value[1](ir[key]))
        return vs

    def get_values(self, ir):
        return self._get_values(self.labels, ir)


META_LABELS = ExtractedLabels(_META_LABELS)
PER_LAP_LABELS = ModifiedExtractedLabels(_PER_LAP_LABELS)
STARTUP_LABELS = Labels({"client_startup_identifier": uuid.uuid4().hex})
