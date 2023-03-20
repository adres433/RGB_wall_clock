# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
import uos, machine, webrepl, gc
from object2 import *
f = open("config.adres433", 'r')
f2 = f.readlines()
f.close()
for x in range(len(f2)):
    if f2[x].find('\r') > -1:
        f2[x] = f2[x].replace('\r', '')
    if f2[x].find('\n') > -1:
        f2[x] = f2[x].replace('\n', '')

network.WLAN(network.AP_IF).active(False)
siec = Web(f2[0], f2[1])
gc.collect()