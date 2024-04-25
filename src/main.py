import time

from irsdk import IRSDK
from src.registry import Registry
from prometheus_client import push_to_gateway
import telemetry
from src.config import Config
from telemetry import Gauge

MODE_BLACKLIST = 1
BLACKLIST = []
WHITELIST = []


def write_telemetry(c: Config, r: Registry):
    push_to_gateway(c.config["push_gw_url"], job=c.job_name(), registry=r.registry)
    print("Telemetry written")


def main():
    c = Config()
    ir = IRSDK()
    metaLabels = telemetry.Labels(telemetry.META_LABELS)

    laptime = Gauge('laptime', 'Laptime', [metaLabels])

    r = Registry([laptime], [])

    if c.config["test_file"]:
        ir.startup(c.config["test_file"])
    else:
        ir.startup()


if __name__ == "__main__":
    main()
