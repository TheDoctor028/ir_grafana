import os

from irsdk import IRSDK
from meters.registry import registry, get_job_name
from meters.client_data import client_last_write
from prometheus_client import push_to_gateway

PUSH_GW_URL = os.getenv('PUSH_GW_URL', 'http://localhost:9091')
MODE_BLACKLIST = 1
BLACKLIST = []
WHITELIST = []


def write_telemetry(name, value):
    if name in BLACKLIST and MODE_BLACKLIST:
        return
    elif name not in WHITELIST and not MODE_BLACKLIST:
        return
    client_last_write.set_to_current_time()
    push_to_gateway(PUSH_GW_URL, job=get_job_name(), registry=registry)


def main():
    ir = IRSDK()
    ir.startup("../test_files/dump.txt")
    ir.freeze_var_buffer_latest()
    write_telemetry("SessionTime", ir['SessionTime'])


if __name__ == "__main__":
    main()
