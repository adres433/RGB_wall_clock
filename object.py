import neopixel, machine, random as rand
class Clock():
    matrix = [(0, 1, 1, 1, 1, 1, 1), (0, 0, 0, 1, 1, 0, 0), (1, 1, 1, 0, 1, 1, 0),
         (1, 0, 1, 1, 1, 1, 0), (1, 0, 0, 1, 1, 0, 1), (1, 0, 1, 1, 0, 1, 1),
         (1, 1, 1, 1, 0, 1, 1), (0, 0, 0, 1, 1, 1, 0), (1, 1, 1, 1, 1, 1, 1),
         (1, 0, 1, 1, 1, 1, 1), (0, 0, 0, 0, 0, 0, 0), (1, 1, 0, 1, 1, 0, 1),
         (0, 1, 1, 0, 0, 1, 1)]
    matrix_r = [(1, 1, 1, 1, 1, 1, 0), (1, 0, 0, 0, 0, 1, 0), (0, 1, 1, 0, 1, 1, 1),
           (1, 1, 0, 0, 1, 1, 1), (1, 0, 0, 1, 0, 1, 1), (1, 1, 0, 1, 1, 0, 1),
           (1, 1, 1, 1, 1, 0, 1), (1, 0, 0, 0, 1, 1, 0), (1, 1, 1, 1, 1, 1, 1),
           (1, 1, 0, 1, 1, 1, 1), (0, 0, 0, 0, 0, 0, 0), (1, 0, 1, 1, 0, 1, 1),
           (0, 1, 1, 1, 1, 0, 0)]   #H - 11; C - 12
    def __init__(self,digits, colon, pin, q_led, led_segment): #ilość cyfr, ilość dwukropków, pin, ilość led, ilość led na segment
        self.digits = digits                            #ilosc cyfr
        self.colon = colon                              #ilosc separatorow
        self.led = q_led                                #ilosc led [wszystkich]
        self.pixel = neopixel.NeoPixel(machine.Pin(pin), q_led)
        self.segment = led_segment                      #ilosc led / segment
        self.q_segm = int((self.led-(2*self.colon))/self.segment)      #ilosc segmentow
        self.segm_d = int(self.q_segm/self.digits)           #ilosc segmentow / cyfre
        self.bright = 100                               #jasność w
        self.a_bright = a_bright                        #automatyczna jasność
        self.dev_matrix = []                            #wirtualna matryca zegara
        self.pixel.fill((0,0,0))                        #czyszczenie zegara
        self.pixel.write()
        return
    def __del__(self):
        del self.digits,self.colon,self.led,self.pixel,self.segment,\
            self.q_segm,self.segm_d,self.bright,self.matrix,self.matrix_r,self.au_bright
        return
    def change(self, num):                              #zwraca index 1. diody segmentu
        a = int(num / 14)
        a = a*2
        a = ((num - 1) * self.segment) + 1 + a
        if a > self.led-1:
            a = self.led-1
        return a
    def change_bright(self,kolor):                      #dostosuj jasność
        R = int((self.bright*kolor[0])/100)
        G = int((self.bright*kolor[1])/100)
        B = int((self.bright*kolor[2])/100)
        return R,G,B
    def random_rgb(self):                               #losowe kolory
        R = rand.getrandbits(8)
        G = rand.getrandbits(8)
        B = rand.getrandbits(8)
        return R,G,B
    def on_all(self, kolor):                            #zapala wszystko
        self.pixel.fill(self.change_bright(kolor))
        self.pixel.write()
        return
    def off_all(self):                                  #gasi wszystko
        self.pixel.fill((0,0,0))
        self.pixel.write()
        return
    def on_seg(self, num, kolor):                       #zapala określony segment
        for y in range(self.segment):
            self.pixel[self.change(num)+y] = self.change_bright(kolor)
        self.pixel.write()
        return
    def off_seg(self, num):                             #gasi określony segment
        for x in range(self.segment):
            self.pixel[self.change(num)+x] = (0,0,0)
        self.pixel.write()
        return
    def on_char(self, char, section, rev, random, kolor):       #ustawia znak w kreślonej sekcji wyświetlacza
        start = int((section*self.segm_d)+(int(section/2)*2))
        if not rev:
            for x in range(self.segm_d):
                if Clock.matrix[char][x] == 1:
                    if random:
                        self.on_seg(self.change(start+x), self.random_rgb())
                    else:
                        self.on_seg(self.change(start+x), kolor)
                else:
                    self.off_seg(self.change(start+x))
        else:
            start += 4
            for x in range(self.segm_d):
                if Clock.matrix_r[char][x] == 1:
                    if random:
                        self.on_seg(start - x, self.random_rgb())
                    else:
                        self.on_seg(start - x, kolor)
                else:
                    self.off_seg(start - x)
        return
    def on_colon(self,kolor):
        for x in range(self.colon):
            a = (14*(x+1))
            self.pixel[a] = self.pixel[a+1] = self.change_bright(kolor)
            self.pixel.write()
        return
    def off_colon(self):
        for x in range(self.colon):
            a = (14*(x+1))
            self.pixel[a] = self.pixel[a+1] = (0,0,0)
            self.pixel.write()
        return