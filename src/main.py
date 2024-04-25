from irsdk import IRSDK
from src.registry import Registry
from src.config import Config
from telemetry import Telemetry
from meter import Gauge
from labels import META_LABELS, PER_LAP_LABELS


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

    print("Initializing metrics...")
    last_laptime = Gauge('last_lap_time', 'Last lap time in seconds', [META_LABELS, PER_LAP_LABELS], 'LapLastLapTime')
    fuel_lvl = Gauge('fuel_level', 'Fuel level in liters', [META_LABELS], 'FuelLevel')

    print("Initializing registry...")
    r = Registry([fuel_lvl], [last_laptime])

    print("Starting telemetry...")
    t = Telemetry(ir, c, r)
    t.start()


if __name__ == "__main__":
    main()
