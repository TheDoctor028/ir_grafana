import time

from irsdk import IRSDK
from src.registry import Registry
from prometheus_client import push_to_gateway
from src.config import Config
from telemetry import Telemetry
from meter import Gauge
from labels import META_LABELS

MODE_BLACKLIST = 1
BLACKLIST = []
WHITELIST = []


def write_telemetry(c: Config, r: Registry):
    push_to_gateway(c.config["push_gw_url"], job=c.job_name(), registry=r.registry)
    print("Telemetry written")


def main():
    c = Config()
    ir = IRSDK()

    if c.config["test_file"]:
        ir.startup(c.config["test_file"])
    else:
        ir.startup()

    last_laptime = Gauge('last_lap_time', 'Last lap time in seconds', [META_LABELS], 'LapLastLapTime')

    r = Registry([last_laptime], [])

    t = Telemetry(ir, r)
    t.start()


if __name__ == "__main__":
    main()
