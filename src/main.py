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
    lap_time = Gauge('lap_time', 'Lap time in seconds',
                         [STARTUP_LABELS, META_LABELS, PER_LAP_LABELS], 'LapLastLapTime')

    current_laptime_per_lap = Gauge('current_lap_time_per_lap', 'Current lap time in seconds',
                            [STARTUP_LABELS, META_LABELS, PER_LAP_LABELS], 'LapCurrentLapTime')

    current_laptime = Gauge('current_lap_time', 'Current lap time in seconds',
                            [STARTUP_LABELS, META_LABELS], 'LapCurrentLapTime')

    fuel_lvl = Gauge('fuel_level', 'Fuel level in liters',
                     [STARTUP_LABELS, META_LABELS], 'FuelLevel')

    fuel_lvl_pct = Gauge('fuel_level_pct', 'Fuel level in %',
                     [STARTUP_LABELS, META_LABELS], 'FuelLevelPct')

    session_time = Gauge('session_time', 'Session time in seconds',
                         [STARTUP_LABELS, META_LABELS], 'SessionTime')

    print("Initializing registry...")
    r = Registry(
        [fuel_lvl, current_laptime, fuel_lvl_pct, session_time],
        [lap_time, current_laptime_per_lap])

    print("Starting telemetry...")
    t = Telemetry(ir, c, r)
    t.start()


if __name__ == "__main__":
    main()
