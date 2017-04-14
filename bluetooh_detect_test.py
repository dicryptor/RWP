
import bluetooth
import time
from datetime import datetime
from collections import defaultdict
from statistics import mode

devices = ['D8:C4:E9:78:09:B4', '00:1D:D9:F9:79:43', '10:2F:6B:AC:77:8F'] ## demo data
devices_in = []

# Empty dictionary to store queues for every registered device
devices_dict = defaultdict(list)

# Dynamically create queue object by iterating through the list of devices and storing them in dictionary
#for i in devices:
#    devices_dict[i] = []

print("In/Out Board")

while True:
    now = datetime.now()
    print("{}: Checking...".format(now.strftime('%Y-%M-%d %H:%M:%S')))

    for i in devices:
        if i not in devices_in:
            result = bluetooth.lookup_name(i, timeout=3)
            if (result != None):
                print('{}: Detected!!!'.format(i))
                devices_dict[i].append(1)
            else:
                print('{}: Not Detected!'.format(i))
                devices_dict[i].append(0)
            result = None
            if len(devices_dict[i]) > 2:
                print("{} has been checked 3 times!".format(i))
                if mode(devices_dict[i]) == 1:
                    print("Insert status into DB")
                    devices_in.append(i)
                del devices_dict[i]

    print(devices_dict)
    print(devices_in)
    time.sleep(5)

#    tester = 'D8:C4:E9:78:09:B4'
#    result = bluetooth.lookup_name(tester, timeout=2)
#    if (result != None):
#        print("Dicryptor's S7 Edge: in")
#    else:
#        print("Dicryptor's S7 Edge: out")
#    result = bluetooth.lookup_name('00:1D:D9:F9:79:43', timeout=2)
#    if (result != None):
#        print("Paul: in")
#    else:
#        print("Paul: out")
