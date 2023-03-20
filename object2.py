import network, ntptime, time, ubinascii, machine
class Web():
    wifi = network.WLAN(network.STA_IF)
    mac = ubinascii.hexlify(wifi.config('mac'),':').decode()
    def __init__(self, essid, paswd):
        Web.wifi.active(True)
        self.essid = essid
        self.pswd = paswd
        self.timer = machine.Timer(-1)
        self.ip = ''
        self.connected = False
        print("Połączenie skonfigurowane.\r\n")
        return
    def __del__(self):
        del Web.wifi, self.essid, self.pswd, self.timer, Web.mac, self.ip, self.connected
        print("Połaczenie zakończone.\r\n")
        return
    def connect(self,first, *stan):
        if first:
            if Web.wifi.isconnected():
                print("Nawiązano połączenie.\r\n")
                self.timer.init(period=5 * 60 * 1000, mode=machine.Timer.PERIODIC, callback=lambda a: self.check())
                self.ip = str(Web.wifi.ifconfig()[0])
                self.connected = True
                return
            else:
                Web.wifi.connect(self.essid, self.pswd)
                self.timer.init(period=5000, mode=machine.Timer.ONE_SHOT, callback=lambda a: self.connect(False, True))
                print("Nawiązywanie połączenia z siecią "+self.essid+"...\r\n")
                return
        else:
            self.timer.deinit()
        if Web.wifi.isconnected():
            print("Nawiązano połączenie.\r\n")
            self.timer.init(period=5 * 60 * 1000, mode=machine.Timer.PERIODIC, callback=lambda a: self.check())
            self.ip = str(Web.wifi.ifconfig()[0])
            self.connected = True
            return
        else:
            if stan[0]:
                print("...\r\n")
                self.timer.init(period=5000, mode=machine.Timer.ONE_SHOT, callback=lambda a: self.connect(False, False))
            else:
                print("Nie udało się nawiązać połączenia.\r\n Kolena próba za 10s.\r\n")
                self.connected = False
                self.timer.deinit()
                self.timer.init(period=10000, mode=machine.Timer.ONE_SHOT, callback=lambda a: self.connect(True))
        return
    def check(self):
        if(Web.wifi.isconnected() and self.connected):
            return True
        if(not Web.wifi.isconnected() and self.connected):
            self.connected = False
            self.timer.deinit()
            print("Utracono połączenie z siecią WiFi.\r\n Ponowne nawiązywanie połączenia.\r\n")
            self.connect()
            return False
        return False
class TimeMy():
    rtc = machine.RTC()
    def __init__(self, summer, timezone):
        TimeMy.rtc.datetime((2020, 1, 1, 0, 0, 0, 0, 0))  # czas startowy
        self.sync = 0
        self.timezone = (str(timezone[0]),str(timezone[1:]))
        self.vsummer = summer
        self.timer = machine.Timer(-1)
        self.ntp = ntptime
        self.ntp.host = "tempus1.gum.gov.pl"
        return
    def synchro(self):
        print("Zegar RTC - synchronizacja...\r\n")
        print(TimeMy.rtc.datetime())
        try:
            self.ntp.settime()
        except OSError:
            print("Zegar RTC - wystąpił błąd synchronizacji.\r\n")
            self.timer.deinit()
            self.timer.init(period=5000, mode=machine.Timer.ONE_SHOT, callback=lambda a: self.synchro())
            return
        if (self.timezone[0].find('+') > -1):
            a = self.summer() + int(self.timezone[1])
        else:
            a = self.summer() - int(self.timezone[1])
        print(a)
        b = list(TimeMy.rtc.datetime())
        b[4] += a
        TimeMy.rtc.datetime(tuple(b))
        self.sync = time.time()
        self.timer.init(period=3600000, mode=machine.Timer.ONE_SHOT, callback=lambda a: self.synchro())
        print("Czas zsynchronizowano pomyślnie.\r\n")
        return
    def summer(self):
        if(self.vsummer and self.sync > 0):
            start = finish = 0
            a = list(time.localtime())
            a[1] = 3
            a[2] = 31
            for x in range(3,len(a)):
                a[x] = 0
            for x in range(31):
                a = time.localtime(time.mktime(a) - (x * 24 * 3600))
                if (a[6] == 6):
                    start = time.mktime(a)
                    break
            a = list(time.localtime())
            a[1] = 10
            a[2] = 31
            for x in range(3,len(a)):
                a[x] = 0
            for x in range(31):
                a = time.localtime(time.mktime(a) - (x * 24 * 3600))
                if (a[6] == 6):
                    finish = time.mktime(a)
                    break
            if(time.mktime(time.localtime()) >= start and time.mktime(time.localtime()) <= finish):
                return 1
        return 0
    def time(self):
        a = list(TimeMy.rtc.datetime())
        return a