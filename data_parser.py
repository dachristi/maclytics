import os
import re
import sys
import json
from os import listdir

from events import Event
from sql_connector import SqlConnector


def main():
    files = ['queue/%s' %f for f in listdir('queue')
             if f.endswith('txt')]
    for f in files:
        print(f)
        with open(f, 'r') as f_obj:
            parse(f_obj.read(), f)


def parse(text, f):
    '''
    Given text, parse the timestamp, MAC address, and signal strength.
    Return as a list of entry objects.
    '''
    sql = SqlConnector()
    file_date = re.search(r'data\_(\d{4}\-\d{2}-\d{2})', f).group(1)
    lines = text.split('\n')
    for line in lines:
        if line == '':
            continue
        ts = ts_parser(line, file_date)
        mac = mac_parser(line)
        rssi = rssi_parser(line)
        event = Event(ts, mac, rssi)
        if event.is_random:
            write_to_random_table(sql, event)
        else:
            write_to_events_table(sql, event)
    sql.cnx.commit()
    sql.cnx.close()
    move_processed_file(f)
    return None


def ts_parser(line, file_date):
    '''
    Given a line of text, parse the timestamp.
    '''

    ts_pattern = re.compile(r'(\d{2}\:\d{2}\:\d{2})\.\d{6}')
    try:
        ts = ''.join([file_date, ' ', re.search(ts_pattern, line).group(1)])
    except AttributeError:
        ts = '1999-12-31 23:59:59'
    return ts


def mac_parser(line):
    '''
    Given a line of text, parse the mac address.
    '''
    mac_pattern = re.compile(r'([0-9A-Fa-f]{2}\:[0-9A-Fa-f]{2}\:[0-9A-Fa-f]{2}\:[0-9A-Fa-f]{2}\:[0-9A-Fa-f]{2}\:[0-9A-Fa-f]{2})')
    try:
        full_mac = re.search(mac_pattern, line).group(1)
        mac = re.sub(r'\:', '', full_mac)
    except AttributeError:
        mac = '000000000000'
    return mac


def rssi_parser(line):
    rssi_pattern = re.compile(r'\-(\d{1,3})dBm')
    try:
        rssi = re.search(rssi_pattern, line).group(1)
    except AttributeError:
        rssi = 999
    return rssi


def write_to_random_table(sql, event):
    cmd = '''
            INSERT INTO events_random
            (ts, mac, rssi)
            VALUES
            (%s,%s,%s);
            '''
    sql.cursor.execute(cmd, (event.ts, event.mac, event.rssi))
    return None


def write_to_events_table(sql, event):
    cmd1 = '''
            SELECT id
            FROM mac_addresses
            WHERE mac = %s;
            '''

    cmd2 = '''
             INSERT INTO mac_addresses
             (mac)
             VALUES
             (%s);
             '''

    cmd3 = '''
            INSERT INTO events
            (ts, mac_id, rssi)
            VALUES
            (%s,%s,%s);
            '''

    sql.cursor.execute(cmd1, (event.mac,))
    x = sql.cursor.fetchall()

    if len(x) == 0:
        sql.cursor.execute(cmd2, (event.mac,))
        sql.cursor.execute(cmd1, (event.mac,))
        x = sql.cursor.fetchall()
        mac_id = x[0]['id']
    else:
        mac_id = x[0]['id']

    sql.cursor.execute(cmd3, (event.ts, mac_id, event.rssi))
    return None


def move_processed_file(f):
    '''Move the file to the processed_files directory.'''
    file_name = re.search(r'queue/([\w\-\_\.]+)', f).group(1)
    os.rename(f, 'processed_files/%s' % file_name)
    return None


if __name__ == '__main__':
    sys.exit(main())
