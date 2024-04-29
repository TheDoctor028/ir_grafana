from meter import Gauge
from labels import META_LABELS, PER_LAP_LABELS, STARTUP_LABELS

lap_time = Gauge('lap_time', 'Lap time in seconds',
                 [STARTUP_LABELS, META_LABELS, PER_LAP_LABELS], 'LapLastLapTime')

best_lap_time = Gauge('best_lap_time', 'Best lap time in seconds',
                        [STARTUP_LABELS, META_LABELS], 'LapBestLapTime')

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

session_time_remain = Gauge('session_time_remain', 'Session time remaining in seconds',
                                 [STARTUP_LABELS, META_LABELS], 'SessionTimeRemain')

session_laps_remain = Gauge('session_laps_remain', 'Session laps remaining',
                            [STARTUP_LABELS, META_LABELS], 'SessionLapsRemain')


PER_TICK_METRICS = [fuel_lvl, current_laptime, fuel_lvl_pct, session_time, session_time_remain, session_laps_remain]
PER_LAP_METRICS = [lap_time, current_laptime_per_lap, best_lap_time]