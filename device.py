import os
import RPi.GPIO as GPIO
import pygame
import csv
import Adafruit_ADS1x15
import board
import keypad
import digitalio

Vadj = 0.00022917  #Adjusts raw ADC value = ((4.096 / 32767) / 1.2) * 2.2

KEY_PINS = (
    board.D26,
    board.D13,
    board.D20,
    board.D17,
    board.D5,
    board.D27,
    board.D22,
    board.D6
)

class PiPod:
    sleep = 0
    # Create a list of battery voltage values. Will use to low-pass filter the ADC values.
    lp=[]
    for i in range(15):
        lp.append(0.0)

    def __init__(self):
        # Initialize ADC
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48,busnum=1)

        self.keys = keypad.Keys( KEY_PINS, value_when_pressed = False, pull = True )

        # Set backlight pin as output and turn it on
        self.pin23 = digitalio.DigitalInOut(board.D23)
        self.pin23.direction = digitalio.Direction.OUTPUT
        self.pin23.value = True

    def scan_switches(self):
        event = self.keys.events.get()
        if event:
            if event.pressed:
                key_number = event.key_number
                if( key_number == 0 ):
                    self.VolUp()
                elif( key_number == 1 ):
                    self.VolDown()
                elif( key_number == 2 ):
                    self.UpArrow()
                elif( key_number == 3 ):
                    self.DownArrow()
                elif( key_number == 4 ):
                    self.LeftArrow()
                elif( key_number == 5 ):
                    self.RightArrow()
                elif( key_number == 6 ):
                    self.Return()
                elif( key_number == 7 ):
                    self.Escape()
        return

    def getStatus(self):
        status = [0, 0, 0]
        #Note: adc0 = external USB voltage
        #Note: adc1 = internal battery voltage
        adc0 = self.adc.read_adc(0, gain=1) * Vadj * 1.005 #observed adjustment
        adc1 = self.adc.read_adc(1, gain=1) * Vadj * 1.005
        self.lp.append(adc1)  # put new battery voltage reading at end of list.
        self.lp.pop(0)        # delete/remove the oldest value
        adc1 = sum(self.lp) / len(self.lp)  # calculate the average value.
        status[0] = adc0 > 4.5
        status[1] = "%.2f" % round(adc1, 2)
        status[2] = self.sleep

        return status

    def toggleSleep(self):
        if self.sleep == 0:
            #GPIO.output(23, GPIO.LOW)
            self.pin23.value = False   # Turn off backlight LED
            self.sleep = 1
            return True
        else:
            #GPIO.output(23, GPIO.HIGH)
            self.pin23.value = True   # Turn on backlight LED
            self.sleep = 0
            return False

    def isAsleep(self):
        return (self.sleep == 1)

    def shutdown(self):
        os.system("sudo shutdown now")
        while True:
            pass
        return 1

    def reboot(self):
        os.system("sudo reboot now")
        return 1

    def VolUp(self):
        volUpEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_u)
        pygame.event.post(volUpEvent)

    def VolDown(self):
        volDownEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_d)
        pygame.event.post(volDownEvent)

    def UpArrow(self):
        upEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)
        pygame.event.post(upEvent)

    def DownArrow(self):
        downEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)
        pygame.event.post(downEvent)

    def LeftArrow(self):
        leftEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_LEFT)
        pygame.event.post(leftEvent)

    def RightArrow(self):
        rightEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RIGHT)
        pygame.event.post(rightEvent)

    def Return(self):
        returnEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)
        pygame.event.post(returnEvent)

    def Escape(self):
        escapeEvent = pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)
        pygame.event.post(escapeEvent)
