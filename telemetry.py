import desietc.db

def get_db():
    """
    Query online telemetry DB for wind speed, wind direction,
    and telescope position
    """
    db = desietc.db.DB()
    env_tower = desietc.db.NightTelemetry(db, 'environmentmonitor_tower',
                                          'wind_speed, wind_direction, gust')
    env_telescope = desietc.db.NightTelemetry(db, 'environmentmonitor_telescope',
                                              'wind_gust, wind_shake')
    tcs_info = desietc.db.NightTelemetry(db, 'tcs_info', 'dome_az')
    env_dome = desietc.db.NightTelemetry(db, 'environmentmonitor_dome',
                                         'shutter_upper, shutter_lower')

    return env_tower, env_telescope, tcs_info, env_dome

def get_telemetry(table, nigjt, mjd):
    """
    Query online telemetry DB for wind speed, direction, and
    telescope position
    """
    return table(night, MJD=mjd)

