from machine import Pin
import utime

led = Pin(16, Pin.OUT)
while True:
    led.value(1)
    utime.sleep_ms(1000)
    led.value(0)
    utime.sleep_ms(1000)
