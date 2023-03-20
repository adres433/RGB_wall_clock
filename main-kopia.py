from object import *
kolor = (255,255,255)   #aktualny kolor wszystkich sekcji
rand = False            #losowy kolor segmentów
randSingle = False      #losowy kolor cwszystkich sekcji
refresh = 1000           #czas odświeżania zegara
mainTimer = machine.Timer(-1)   #timer zegara
siec.connect(True)
clock = Clock(4,1,5,30,1)
czas = TimeMy(True,'+1')
x = 0
#FUNKCJA GŁÓWNA
def main(when, how):
    global kolor, rand, randSingle, refresh
    nhow = how
    y = when
    a = list(czas.time())
    z = a[1]
    a[1] = a[2]
    a[2] = z
    #wyswietlanie daty i godziny na przemian
    if when == 1 and nhow > 5:
        nhow = 0
        y = 4
    elif when == 4 and nhow > 5:
        y = 1
        nhow = 0
    #obsługa losowego koloru dla całego napisu
    if(randSingle):
        kolor = clock.random_rgb()
    #obsługa dwukropka
    if int(nhow%2) > 0:
        if rand:
            clock.on_colon(clock.random_rgb())
        else:
            clock.on_colon(kolor)
    else:
        clock.off_colon()
    #inisjalizacja timera odświeżającego zegar
    mainTimer.init(period=refresh, mode=machine.Timer.ONE_SHOT, callback=lambda a: main(y, nhow+1))
    #godzina / data
    for x in range(clock.digits/2):
        if a[y+x] < 10 and x == 0 and y == 1:
            clock.on_char(0, 1, False, rand, kolor)
            clock.on_char(a[y+x], 0, False, rand, kolor)
        elif a[y+x] < 10 and x == 0 and y == 4:
            clock.on_char(10, 1, False, rand, kolor)
            clock.on_char(a[y+x], 0, False, rand, kolor)
        elif a[y+x] < 10 and x > 0:
            clock.on_char(0, 2, True, rand, kolor)
            clock.on_char(a[y+x], 3, True, rand, kolor)

        elif a[y+x] == 0 and x == 0:
            clock.on_char(0, 0, False, rand, kolor)
            clock.on_char(10, 1, False, rand, kolor)
        elif a[y+x] == 0 and x > 0:
            clock.on_char(0, 2, True, rand, kolor)
            clock.on_char(0, 3, True, rand, kolor)

        elif a[y+x] > 10 and x == 0:
            b = int(a[y+x] / 10)
            c = a[y+x] % 10
            clock.on_char(b, 1, False, rand, kolor)
            clock.on_char(c, 0, False, rand, kolor)
        elif a[y+x] > 10 and x > 0:
            b = int(a[y+x] / 10)
            c = a[y+x] % 10
            clock.on_char(b, 2, True, rand, kolor)
            clock.on_char(c, 3, True, rand, kolor)
    return

#oczekiwanie na połączenie z WIFI
while True:
    if siec.check():
        clock.off_all()
        del x
        break
    else:
        time.sleep(1)
        clock.on_seg(x, (255, 0, 0))
        clock.off_seg(x - 1)
        x += 1
        if x >= clock.q_segm:
            x = 0
            clock.off_all()
            machine.reset()
#start WEBREPL
webrepl.start()
#synchronizacja zegara
czas.synchro()
#wypisanie aktualnego IP
for x in siec.ip:
    if(x == '.'):
        clock.on_all((255,0,0))
    else:
        clock.on_char(int(x),0,False, False, (255,255,255))
    time.sleep(1)
    clock.off_all()
del x
#uruchomienie funkcji głównej
main(1, 0)