from piglow import PiGlow
from time import sleep

piglow = PiGlow()

def pata(min, max):
    i = min
    while i <= max:
        if i > min:
            piglow.led(i - 1, 0)
        piglow.led(i, 1)
        sleep(0.3)
        i += 1

def estrella():
    piglow.all(1)
    sleep(0.5)
    i = 6
    j = 12
    k = 18

    while i >= 1:
        piglow.led(i, 0)
        piglow.led(j, 0)
        piglow.led(k, 0)
        sleep(0.3)        

        i -= 1
        j -= 1
        k -= 1

try:
    while True:
        piglow.all(0)
        pata(1, 6)
        estrella()
        pata(7, 12)
        estrella()
        pata(13, 18)
        estrella()

except KeyboardInterrupt:
    piglow.all(0)
