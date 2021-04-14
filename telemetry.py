import desietc.db

def get_telemetry():
    """
    Query online telemetry DB for wind speed, direction, and
    telescope position
    """ 
    telescope = query("""
                SELECT DATE(T.time_recorded), AVG(T.wind_speed)
                    AS wind_speed, AVG(T.wind_direction) AS wind_direction
                FROM telemetry.environmentmonitor_tower AS T
                WHERE T.time_recorded > '20210319'
                GROUP BY DATE(T.time_recorded)
                ORDER BY DATE(T.time_recorded) DESC
    """, maxrows=50)
    return telescope


def query(sql, maxrows=10, dates=None):
    """
    Individual query
    """
    db = desietc.db.DB()
    df = db.query(sql, maxrows, dates)
    return df
