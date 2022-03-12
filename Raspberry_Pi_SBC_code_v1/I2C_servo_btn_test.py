#!/usr/bin/python

# RPi kits PCB mechatronic version of I2C_servo_btn.py - servo control using a PCA9685 I2C controller
# moves a SG90 servo on channel N from min to max position whenever a button is pressed
#
# command:  python3 /home/pi/RPi_maker_kit5/mechatronics/I2C_servo_btn_test.py

# CLI command to check I2C address:  i2cdetect -y -r 1
#

########################################################
####            various python functions            ####
########################################################

########################################################
## generic LCD display function
########################################################
def lcddisp(text1, text2, stime):
    mylcd.lcd_clear()
    mylcd.lcd_display_string(text1, 1, 0)   # display at row 1 column 0
    mylcd.lcd_display_string(text2, 2, 0)   # display at row 2 column 0
    time.sleep(stime)  # short pause to make sure the display above is 'seen'

############################################################
# this is a function to indicate when the button is pressed 
############################################################
def btn_pressed():
    # if button is pressed GPIO.input will report FALSE
    if not GPIO.input(button_pin):
        return 1


########################################################
####                   main code                    ####
########################################################
import time               # this imports the module to allow various time functions to be used
import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised
from ctypes import *
import I2C_LCD_driver

# set up the LCD display function
mylcd = I2C_LCD_driver.lcd()
lcddisp("system starting.", "***************", 1)

# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

button_pin = 26  # this is the GPIO pin for button 2 that one side of the tactile button is connected to

GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  
# this is a special setting that indicates when a pin changes from LOW to HIGH ie when the button is pressed

# --------------------------------------------------------------------------------
# Initialise the servo control board assuming it has its 
#  default address hex 40 (0x40) and is the only device on the bus
#  this can be checked by running "sudo i2cdetect -y 1"
#  for all recent RPi models the port# is 1 in the above 'detect' command - but for pre-Oct'12 models it is 0

# set up the use of a set of compiled C functions that do various servo functions
# compiled C is used because it is faster than interpreted python coding and some 
# of these functions need to run as fast as possible

picontrol_servo = CDLL("/home/pi/RPi_maker_kit5/mechatronics/libpicontrol_servo.so")
#call the servo connect C function to check connection to the compiled 'C' library
picontrol_servo.connect_servo() 

# Initialise the PCA9685 servo PWM control board assuming it has its 
#  default address i.e. hex 40 (0x40) and is the only PCA9685 device on the I2C bus
#  this can be checked by running "sudo i2cdetect -y 1"
#  for all recent RPi models the port# is 1 in the above 'detect' command - but for pre-Oct'12 models it is 0
address = "0x40" 
frequency = 50  # recommended PWM frequency for servo use
print (" setting up PWM module")
print ("  ")
filedesc = picontrol_servo.PWMsetup(0x40, 50)  # sets up the board and retrieves the I2C file descriptor for later use
print ("I2C file descriptor is: " + str(filedesc))
print ("  ")
lcddisp("system config", "  servos set up ", 1)

print("PCA9685 initialised")

servo_chan = 99
# set the min and max servo pulse lengths
# min: 1ms pulse length ie should be 205 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details
servo_min = 160 

# max: 1.5ms pulse length ie should be 308 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details 
servo_mid = 350 

# mid: 2ms pulse length ie should be 410 steps out of 4096 but fine tuned for the specific servo - see the support documentation for more details
servo_max = 560 

print (" ***************************************************************************")
print (" An individual servo channel number 0-15 needs to be entered ")
while int(servo_chan) < 0 or int(servo_chan) > 15:
    servo_chan = input(" Enter a servo channel value from 0 to 15: ")
print (" ***************************************************************************")
print (" ")

print("Program running: press the button 2 to move servo channel " + str(servo_chan) + " from min to max once - CTRL C to stop")
try:    # this loop is not strictly necessary but it does allow the script to be easily stopped with CTRL-C
    while True:  # this is the loop that checks if a button is pressed and moves each servo arm if it is

        while not btn_pressed():
            pass                         # if the button is not pressed just loop endlessly

        # button pressed so move servo on channel O between extremes.
        print("button pressed - moving servo on channel 0")
        picontrol_servo.setServo(filedesc, int(servo_chan), servo_min, 50)
        time.sleep(2)
        picontrol_servo.setServo(filedesc, int(servo_chan), servo_max, 50)
        time.sleep(2)
        picontrol_servo.setServo(filedesc, int(servo_chan), servo_mid, 50)
        time.sleep(2)
        print("press the button 2 again to move the servo or CTRL C to stop")

finally:  # this code is run when the try is interrupted with a CTRL-C
    print(" ")
    print("Cleaning up the GPIO pins before stopping")
    print(" ")
    print(" ")
    print(" ")
    GPIO.cleanup()
    print("*******************************************************")
    print("program end")
    print("*******************************************************")
    print("  ")
    mylcd.lcd_clear()
    mylcd.backlight(0)

    
# The cleanup command sets all the pins back to inputs which protects the
# Pi from accidental shorts-circuits if something metal touches the GPIO pins.

