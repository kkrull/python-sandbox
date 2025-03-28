import utime
from machine import Pin

led = Pin("LED", Pin.OUT)

while True:
    led.toggle()
    utime.sleep_ms(1000)
