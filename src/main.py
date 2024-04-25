import time

from irsdk import IRSDK
from src.registry import registry, Registry
from meters.client_data import client_last_write
from prometheus_client import push_to_gateway, Gauge
import telemetry
from src.config import Config

MODE_BLACKLIST = 1
BLACKLIST = []
WHITELIST = []


def write_telemetry(c: Config):
    client_last_write.set_to_current_time()
    push_to_gateway(c.config["push_gw_url"], job=c.job_name(), registry=registry)
    print("Telemetry written")


def main():
    c = Config()
    ir = IRSDK()
    r = Registry(['fuel'], ['laptime'])

    if c.config["test_file"]:
        ir.startup(c.config["test_file"])
    else:
        ir.startup()

    metaLabels = telemetry.Labels(telemetry.META_LABELS)
    print(metaLabels.get_keys())
    print(metaLabels.get_values(ir))
    laptime = Gauge('laptime', 'Laptime', metaLabels.get_keys(), registry=registry)

    while True:
        laptime.labels(*metaLabels.get_values(ir)).set(ir['LapLastLapTime'])
        write_telemetry(c)
        time.sleep(1)


if __name__ == "__main__":
    main()
