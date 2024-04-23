import os
import time

from irsdk import IRSDK
from meters.registry import registry, get_job_name
from meters.client_data import client_last_write
from prometheus_client import push_to_gateway, Gauge
import telemetry

PUSH_GW_URL = os.getenv('PUSH_GW_URL', 'http://localhost:9091')
MODE_BLACKLIST = 1
BLACKLIST = []
WHITELIST = []


def write_telemetry():
    client_last_write.set_to_current_time()
    push_to_gateway(PUSH_GW_URL, job=get_job_name(), registry=registry)
    print("Telemetry written")


def main():
    ir = IRSDK()
    ir.startup("../test_files/dump.txt")
    ir.freeze_var_buffer_latest()
    metaLabels = telemetry.Labels(telemetry.META_LABELS)
    print(metaLabels.get_keys())
    print(metaLabels.get_values(ir))
    laptime = Gauge('laptime', 'Laptime', metaLabels.get_keys(), registry=registry)

    while True:
        laptime.labels(*metaLabels.get_values(ir)).set(ir['LapLastLapTime'])
        write_telemetry()
        time.sleep(1)


if __name__ == "__main__":
    main()
