import bluetooth
import time
from datetime import datetime
from collections import defaultdict
from statistics import mode
import mysql_connecter_v1

# devices = ['D8:C4:E9:78:09:B4', '10:2F:6B:AC:77:8F'] ## demo data
devices = mysql_connecter_v1.get_devices() # pull registered devices from DB
devices_in = [] # empty list to store check ins

# Empty dictionary to store queues for every registered device
devices_dict = defaultdict(list)

def detection(devices):
    """Bluetooth detection algorithm v1"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    epoch_time = time.time()
    print("{}: Detection cycle running...".format(now))

    for device in devices:
        result = bluetooth.lookup_name(device, timeout=3)
        if (result != None):
            print('{}: Detected!!!'.format(device))
            devices_dict[device].append(1)
        else:
            print('{}: Not Detected!'.format(device))
            devices_dict[device].append(0)
        result = None
        if len(devices_dict[device]) > 2:
            print("{} has been checked 3 times!".format(device))
            # devices_check = [i[0] for i in devices_in]
            found, position = search_sublist(devices_in, device)
            if mode(devices_dict[device]) == 1:
                time_check = epoch_time - devices_in[position][1]
                print('Time since last status change is {}'.format(time_check))
                if time_check > 60:
                    if found is False:
                        print('Mark as check in')
                        devices_in.append([device, epoch_time])
                        mysql_connecter_v1.insert_device_status(device, now, "in", 1)
                    elif found is True:
                        print('Mark as check out at position ', position)
                        mysql_connecter_v1.insert_device_status(device, now, "out", 1)
                        del devices_in[position]

            del devices_dict[device]  # clear devices_dict for next cycle


def search_sublist(alist, item):
    for i,j in enumerate(alist):
        if j[0] == item:
            return True, i

    return False, -1

while True:
    try:
        detection(devices)
        for k,v in devices_dict.items():
            print(k, v)
        print('\nDevices checked in: {}\n'.format(devices_in))
        time.sleep(5)
    except (KeyboardInterrupt, SystemError, SystemExit):
        mysql_connecter_v1.conn.close()

