


class Event(object):

    def __init__(self, ts, mac, rssi):
        self.ts = ts
        self.mac = mac
        self.rssi = rssi

        self.is_random = self.detect_random_mac(self.mac)

    def detect_random_mac(self, mac):
        '''If MAC address is local or random, return true; else, return 0.
        '''
        universal_local_bit = mac[1]
        if universal_local_bit in ('2', '3', '6', '7', 'a', 'b', 'e', 'f'):
            return True  # random/local mac address
        else:
            return False  # global mac address
