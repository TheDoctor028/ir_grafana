from irsdk import IRSDK
from registry import Registry
from config import Config
from telemetry import Telemetry
from meter import Gauge
from labels import META_LABELS, PER_LAP_LABELS, STARTUP_LABELS


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
    last_laptime = Gauge('last_lap_time', 'Last lap time in seconds',
                         [STARTUP_LABELS, META_LABELS, PER_LAP_LABELS], 'LapLastLapTime')

    current_laptime_per_lap = Gauge('current_lap_time_per_lap', 'Current lap time in seconds',
                            [STARTUP_LABELS, META_LABELS, PER_LAP_LABELS], 'LapCurrentLapTime')

    current_laptime = Gauge('current_lap_time', 'Current lap time in seconds',
                            [STARTUP_LABELS, META_LABELS], 'LapCurrentLapTime')

    fuel_lvl = Gauge('fuel_level', 'Fuel level in liters',
                     [STARTUP_LABELS, META_LABELS], 'FuelLevel')

    print("Initializing registry...")
    r = Registry([fuel_lvl, current_laptime], [last_laptime, current_laptime_per_lap])

    print("Starting telemetry...")
    t = Telemetry(ir, c, r)
    t.start()


if __name__ == "__main__":
    main()
