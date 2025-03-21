from machine import Pin, PWM
import utime

led = PWM(Pin(16, Pin.OUT))
led.freq(1000)

led.duty_u16(0)
while True:
    for duty in range(0, 65536, 1):
        led.duty_u16(duty)
        utime.sleep_ms(1)
    
    for duty in range(65536, 0, -1):
        led.duty_u16(duty)
        utime.sleep_ms(1)
