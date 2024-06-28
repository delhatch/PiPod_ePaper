import os
import RPi.GPIO as GPIO
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
    # Create a list of battery voltage values. Will use to low-pass filter the ADC values.
    lp=[]
    for i in range(3):
        lp.append(0.0)
    pressedKey = -1

    def __init__(self):
        # Initialize ADC
        self.adc = Adafruit_ADS1x15.ADS1115(address=0x48,busnum=1)
        self.keys = keypad.Keys( KEY_PINS, value_when_pressed = False, pull = True )
        adc1 = self.adc.read_adc(1, gain=1) * Vadj * 1.005
        self.lp = [ adc1 ] * len( self.lp )   # Initialize the low-pass filter to the current battery voltage.

    def scan_switches(self):
        event = self.keys.events.get()
        if event:
            if event.pressed:
                self.pressedKey = event.key_number
        return

    def getKeyPressed(self):
        return self.pressedKey

    def clearKeyPressed(self):
        self.pressedKey = -1
        return

    def isPressed(self, keyGPIO):
        return GPIO.input( keyGPIO )

    def getStatus(self):
        status = [0, 0]
        #Note: adc0 = external USB voltage. Never used.
        #Note: adc1 = internal battery voltage
        # adc0 = self.adc.read_adc(0, gain=1) * Vadj * 1.005 #observed adjustment
        adc1 = self.adc.read_adc(1, gain=1) * Vadj * 1.005
        self.lp.append(adc1)  # put new battery voltage reading at end of list.
        self.lp.pop(0)        # delete/remove the oldest value
        #adc1 = sum(self.lp) / len(self.lp)  # calculate the average value.
        adc1 = sum(self.lp) / 3  # calculate the average value.
        #status[0] = adc0 > 4.5
        status[0] = True
        status[1] = "%.2f" % round(adc1, 2)
        return status

