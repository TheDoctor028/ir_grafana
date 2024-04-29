from irsdk import IRSDK
from registry import Registry
from config import Config
from telemetry import Telemetry
from metrics import PER_LAP_METRICS, PER_TICK_METRICS


def main():
    print("Starting up...")
    c = Config()
    print("Config loaded")
    ir = IRSDK()
    print("IRSDK loaded")

    if c["test_file"]:
        print("Using test file")
        ir.startup(c["test_file"])
    else:
        print("Using live data")
        ir.startup()

    print("Initializing registry...")
    r = Registry(PER_TICK_METRICS, PER_LAP_METRICS)

    print("Starting telemetry...")
    t = Telemetry(ir, c, r)
    t.start()


if __name__ == "__main__":
    main()
