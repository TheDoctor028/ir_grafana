from irsdk import IRSDK
from src.registry import Registry
from src.config import Config
from telemetry import Telemetry
from meter import Gauge
from labels import META_LABELS


def main():
    c = Config()
    ir = IRSDK()

    if c["test_file"]:
        ir.startup(c["test_file"])
    else:
        ir.startup()

    last_laptime = Gauge('last_lap_time', 'Last lap time in seconds', [META_LABELS], 'LapLastLapTime')

    r = Registry([last_laptime], [])

    t = Telemetry(ir, c, r)
    t.start()


if __name__ == "__main__":
    main()
