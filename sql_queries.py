import json

from sql_connector import SqlConnector


def query_average_dwell(start_time, end_time):
    '''Query the Average Dwell Time for all events within the time range'''
    cmd = '''
            SELECT AVG(dwell) dwell_time
            FROM
              (select count(1), mac_id, MIN(ts), TIMESTAMPDIFF(MINUTE, MIN(ts), MAX(TS)) dwell
              FROM events
              GROUP BY 2
              #HAVING COUNT(1) > 1
              HAVING dwell >= 1
              LIMIT 10) t;
        '''
    sql = SqlConnector()
    sql.cursor.execute(cmd)
    x = sql.cursor.fetchall()
    sql.cursor.close()

    dwell_time = str(round(float(x[0]['dwell_time']), 1))
    return dwell_time


def query_unique_visitors(start_time='1999-12-31 23:59:59', end_time='2020-01-01 00:00:00'):
    '''Query the Events table for unique mac addresses'''
    cmd = '''
            SELECT COUNT(DISTINCT mac_id) unique_visitors
            FROM events
            WHERE ts BETWEEN %s AND %s;
        '''
    sql = SqlConnector()
    sql.cursor.execute(cmd, (start_time, end_time))
    x = sql.cursor.fetchall()
    sql.cursor.close()

    unique_visitors = str(format(x[0]['unique_visitors'], ",d"))
    return unique_visitors


def query_mac_search(mac):
    '''Query the Events table for unique mac addresses'''
    cmd1 = '''
            SELECT id mac_id
            FROM mac_addresses
            WHERE mac = %s;
        '''
    cmd2 = '''
            SELECT COUNT(1) mac_count
            FROM events
            WHERE mac_id = %s;
        '''

    sql = SqlConnector()
    sql.cursor.execute(cmd1, (mac,))
    x = sql.cursor.fetchall()
    if len(x) == 0:
        return '0 entries'
    else:
        pass
    mac_id = x[0]['mac_id']
    sql.cursor.execute(cmd2, (mac_id,))
    x = sql.cursor.fetchall()
    mac_count = x[0]['mac_count']
    sql.cursor.close()

    mac_count = x[0]['mac_count']
    if mac_count == 1:
        mac_count = str(format(mac_count, ",d")) + ' entry'
    else:
        mac_count = str(format(mac_count, ",d")) + ' entries'

    return mac_count


def current_device_count(period=15):
    '''Count the number of devices (non-randomized) detected within last 15
    minutes'''

    cmd = '''
            SELECT COUNT(DISTINCT mac_id) current_device_count
            FROM events
            WHERE ts BETWEEN NOW() - INTERVAL %s MINUTE AND NOW();
            '''
    sql = SqlConnector()
    sql.cursor.execute(cmd, (period,))
    x = sql.cursor.fetchall()[0]['current_device_count']
    sql.cursor.close()
    return x


def query_current_devices(period=15):
    '''Count the number of devices (non-randomized) detected within last 15
    minutes'''

    cmd = '''
            SELECT COUNT(DISTINCT mac_id) current_device_count
            FROM events
            WHERE ts BETWEEN NOW() - INTERVAL %s MINUTE AND NOW();
            '''
    sql = SqlConnector()
    sql.cursor.execute(cmd, (period,))
    x = sql.cursor.fetchall()[0]['current_device_count']
    sql.cursor.close()
    return x


def query_repeat_devices(period=15):
    '''Count the number of devices (non-randomized) detected within last 15
    minutes'''

    cmd = '''
            SELECT COUNT(1) repeat_device_count
            FROM
                (SELECT DISTINCT(mac_id)
                 FROM events
                 WHERE ts BETWEEN NOW() - INTERVAL %s MINUTE AND NOW()) t1
            JOIN
                (SELECT DISTINCT(mac_id)
                 FROM events
                 WHERE ts BETWEEN DATE(NOW()) - INTERVAL 31 DAY
                 AND DATE(NOW())) t2
            ON t1.mac_id = t2.mac_id
            ;
            '''
    sql = SqlConnector()
    sql.cursor.execute(cmd, (period,))
    x = sql.cursor.fetchall()[0]['repeat_device_count']
    sql.cursor.close()
    return x
