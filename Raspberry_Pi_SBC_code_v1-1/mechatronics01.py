#!/usr/bin/python
# 
# RPi Maker Kit mechatronic control program that runs on a Pi with PCB v5.0 and uses a Flask web interface 

#  need to use sudo below so that port 80 (production) with Flask web server is OK
# command to run:  sudo python3 /home/pi/RPi_maker_kit5/mechatronics/mechatronics01.py

# version control set by the following variables reported in the system switch setting
version = "version 1.0"
version_date = "220127"

# various system file paths
global servo_objects_file         # master file of the various servo motor mechatronic objects
servo_objects_file = "/home/pi/RPi_maker_kit5/mechatronics/action_sequences01/servo_objects4x.txt"

global servo_channels_file        # additional servo object file to detail the individual servo's used in the object
servo_channels_file = "/home/pi/RPi_maker_kit5/mechatronics/action_sequences01/servo_servos4x.txt"

global stepper_options_file       # master file of the various stepper motor mechatronic objects
stepper_options_file = "/home/pi/RPi_maker_kit5/mechatronics/action_sequences01/stepper_options4x.txt"

global mdrive_objects_file       # master file of the various drive motor mechatronic objects
mdrive_objects_file = "/home/pi/RPi_maker_kit5/mechatronics/action_sequences01/mdrive_objects4x.txt"

global custom_servo_objects_file  # master file of the various custome servo motor mechatronic objects
custom_servo_objects_file = "/home/pi/RPi_maker_kit5/mechatronics/action_sequences01/custom_servo_objects4x.txt"

global semaphore_letter_file      # special file defining the alphabet letter servo 'flagging' data
semaphore_letter_file = "/home/pi/RPi_maker_kit5/mechatronics/action_sequences01/letters.csv"

global semaphore_servo_file       # semaphore servo data - channel#'s and movement calibration 
semaphore_servo_file = "/home/pi/RPi_maker_kit5/mechatronics/action_sequences01/semaphore_servo_data.csv"

# various folder paths
global sound_folder                            # master folder path for the various sound .mp3 and .wav files
sound_folder = "/home/pi/RPi_maker_kit5/mechatronics/sounds/"

global action_folder                           # master folder path for all the various 'action' files
action_folder = "/home/pi/RPi_maker_kit5/mechatronics/action_sequences01/"

# special array for the allowed sound file types 
global allowed_sound_extensions
allowed_sound_extensions = {'mp3', 'wav'}


########################################################
####            various python functions            ####
########################################################

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# Raspberry Pi L298N more developed PWM motor functions but based upon the article at 
#  http://www.instructables.com/id/Control-DC-and-stepper-motors-with-L298N-Dual-Moto/
#  which describes the L298N motor controller use with an Arduino Uno
# 
#  N.B. depending upon how the motors are connected the motor direction
#    signals to the in1, in2, in3 nd in4 pins may need to be reversed
#
# these cut-down functions are for use with mechatronic/Maker Kit builds
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

def Aforward_pwm(dutycycleA):    # M2
    dutycycleB = 0
    # in1, in2, in3 and in4 to be adjusted so that both motors go fwd
    print ("forward " + str(dutycycleA) + " - " +str(dutycycleB))
    print ("IN pins 1-4:" + str(mdrive_IN1) + ", " + str(mdrive_IN2) + ", " + str(mdrive_IN3) + ", " + str(mdrive_IN4) )
    # set enA (right motor) with the PWM dutycycle
    pwm_enA.start(dutycycleA)
    # set in1 off and in2 on i.e. LOW - HIGH for forward motion
    GPIO.output(mdrive_IN1, 0)
    GPIO.output(mdrive_IN2, 1)

    # set enB (left motor) with the PWM dutycycle
    pwm_enB.start(dutycycleB)
    # set in3 off and in4 on -i.e. LOW - HIGH for forward motion
    GPIO.output(mdrive_IN3, 0)
    GPIO.output(mdrive_IN4, 1)

def Bforward_pwm(dutycycleB):   # M1
    dutycycleA = 0
    # in1, in2, in3 and in4 to be adjusted so that both motors go fwd
    print ("forward " + str(dutycycleA) + " - " +str(dutycycleB))
    print ("IN pins 1-4:" + str(mdrive_IN1) + ", " + str(mdrive_IN2) + ", " + str(mdrive_IN3) + ", " + str(mdrive_IN4) )
    # set enA (right motor) with the PWM dutycycle
    pwm_enA.start(dutycycleA)
    # set in1 off and in2 on i.e. LOW - HIGH for forward motion
    GPIO.output(mdrive_IN1, 0)
    GPIO.output(mdrive_IN2, 1)

    # set enB (left motor) with the PWM dutycycle
    pwm_enB.start(dutycycleB)
    # set in3 off and in4 on -i.e. LOW - HIGH for forward motion
    GPIO.output(mdrive_IN3, 0)
    GPIO.output(mdrive_IN4, 1)
 
def Abackward_pwm(dutycycleA):  # M2
    dutycycleB = 0
    # in1, in2, in3 and in4 to be adjusted so that both motors go back
    print ("backward " + str(dutycycleA) + " - " +str(dutycycleB))
    print ("IN pins 1-4:" + str(mdrive_IN1) + ", " + str(mdrive_IN2) + ", " + str(mdrive_IN3) + ", " + str(mdrive_IN4) )
    # set enA (right motor) with the PWM dutycycle
    pwm_enA.start(dutycycleA)
    # set in1 on and in2 off i.e. HIGH - LOW for backward motion
    GPIO.output(mdrive_IN1, 1)
    GPIO.output(mdrive_IN2, 0)

    # set enB (left motor) with the PWM dutycycle
    pwm_enB.start(dutycycleB)
    # set in3 on and in4 off i.e. HIGH - LOW for backward motion
    GPIO.output(mdrive_IN3, 1)
    GPIO.output(mdrive_IN4, 0)

def Bbackward_pwm(dutycycleB):  # M1
    dutycycleA = 0
    # in1, in2, in3 and in4 to be adjusted so that both motors go back
    print ("backward " + str(dutycycleA) + " - " +str(dutycycleB))
    print ("IN pins 1-4:" + str(mdrive_IN1) + ", " + str(mdrive_IN2) + ", " + str(mdrive_IN3) + ", " + str(mdrive_IN4) )
    # set enA (right motor) with the PWM dutycycle
    pwm_enA.start(dutycycleA)
    # set in1 on and in2 off i.e. HIGH - LOW for backward motion
    GPIO.output(mdrive_IN1, 1)
    GPIO.output(mdrive_IN2, 0)

    # set enB (left motor) with the PWM dutycycle
    pwm_enB.start(dutycycleB)
    # set in3 on and in4 off i.e. HIGH - LOW for backward motion
    GPIO.output(mdrive_IN3, 1)
    GPIO.output(mdrive_IN4, 0)

def Astop_pwm():
    # motor A braking
    # set enA with 100% PWM dutycycle
    print ("IN pins 1-4:" + str(mdrive_IN1) + ", " + str(mdrive_IN2) + ", " + str(mdrive_IN3) + ", " + str(mdrive_IN4) )
    pwm_enA.start(100)
    # set in1 off and in2 off i.e. LOW- LOW for no motion
    GPIO.output(mdrive_IN1, 0)
    GPIO.output(mdrive_IN2, 0)

def Bstop_pwm():
    # motor B braking
    # set enB with 100% PWM dutycycle
    print ("IN pins 1-4:" + str(mdrive_IN1) + ", " + str(mdrive_IN2) + ", " + str(mdrive_IN3) + ", " + str(mdrive_IN4) )
    pwm_enB.start(100)
    # set in3 off and in4 off i.e. LOW- LOW for no motion
    GPIO.output(mdrive_IN3, 0)
    GPIO.output(mdrive_IN4, 0)

########################################################
######## function to return the CPU temperature ########
########################################################
# Return CPU temperature as a character string                                     
def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))

########################################################
## generic LCD display function
########################################################
def lcddisp(text1, text2, stime):
    mylcd.lcd_clear()
    mylcd.lcd_display_string(text1, 1, 0)   # display at row 1 column 0
    mylcd.lcd_display_string(text2, 2, 0)   # display at row 2 column 0
    sleep(stime)  # short pause to make sure the display above is 'seen'

####################################################################
## function to copy an_objects and remove spaces from desc field  ##
####################################################################
def servo_obj_transform():
    global an_objects
    global object_number
    # replace any _ characters in the descriptions fields with spaces as spaces are not allowed in the file
    serv_obj = an_objects.copy() # take a copy of an_objects
    for i in range (1, object_number+1):
        serv_obj[i][3]=serv_obj[i][3].replace("_", " ")
    return (serv_obj)      # return copy of an_objects with underscores replaced by spaces in description field

######################################################################
## function to copy step_options and remove spaces from desc field  ##
######################################################################
def step_obj_transform():
    global step_options
    global sopt_number
    # replace any _ characters in the descriptions fields with spaces as spaces are not allowed in the file
    st_obj = step_options.copy() # take a copy of step_options
    for i in range (1, sopt_number+1):
        st_obj[i][3]=st_obj[i][3].replace("_", " ")
    return (st_obj)      # return copy of step-options with underscores replaced by spaces in description field

########################################################################
## function to copy mdrive_objects and remove spaces from desc field  ##
########################################################################
def mdrive_obj_transform():
    global mdrive_objects
    global mdrive_number
    # replace any _ characters in the descriptions fields with spaces as spaces are not allowed in the file
    md_obj = mdrive_objects.copy() # take a copy of step_options
    for i in range (1, mdrive_number+1):
        md_obj[i][3]=md_obj[i][3].replace("_", " ")
    return (md_obj)      # return copy of mdrive_objects with underscores replaced by spaces in description field

###############################################################
## function to check a file's 'security' before uploading it ##
###############################################################
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_sound_extensions


######################################################################
## function to set the semaphore 'servo's to their 'zero' positions ##
######################################################################
def semaphore_zero():
    global semaphore_servo_data
    set_servo('leftshoulder', 0, filedesc, semaphore_servo_data[0][1], semaphore_servo_data[1][1], semaphore_servo_data[2][1], semaphore_servo_data[3][1])
    set_servo('rightshoulder', 0,filedesc,  semaphore_servo_data[0][1], semaphore_servo_data[1][1], semaphore_servo_data[2][1], semaphore_servo_data[3][1])
    set_servo('leftelbow', 90, filedesc, semaphore_servo_data[0][1], semaphore_servo_data[1][1], semaphore_servo_data[2][1], semaphore_servo_data[3][1])
    set_servo('rightelbow', 90, filedesc, semaphore_servo_data[0][1], semaphore_servo_data[1][1], semaphore_servo_data[2][1], semaphore_servo_data[3][1])

    return()

#####################################################################
# function to set up the semaphore 'app' and flag a message
#####################################################################
def semaphore_flagging(message_string):
    global semaphore_servo_data_read 
    global semaphore_letters_read
    global semaphore_servo_data
    global letters
    global semaphore_stop

    # set up all the semaphore flag servo parameters
    # -----------------------------------------------
    # semaphore_servo_data[0][1] is left shoulder servo - normally channel 14
    # semaphore_servo_data[1][1] is left elbow servo - normally channel 15
    # semaphore_servo_data[2][1] is right shoulder servo - normally channel 13
    # semaphore_servo_data[3][1] is right elbow servo - normally channel 12

    # the 5 servo pulse lengths for the 0, 45, 90, 135 and 180 degree positions for both left and right shoulder servos
    # each number may have to be fine tuned for the specific servo - see the support documentation for more details

    # semaphore_servo_data[4][1] = 490 left shoulder 0
    # semaphore_servo_data[5][1] = 370 left shoulder 45
    # semaphore_servo_data[6][1] = 260 left shoulder 90
    # semaphore_servo_data[7][1] = 170 left shoulder 135
    # semaphore_servo_data[8][1] = 100 left shoulder 180

    # semaphore_servo_data[9][1] = 115 right shoulder 0
    # semaphore_servo_data[10][1] = 230 right shoulder 45
    # semaphore_servo_data[11][1] = 315 right shoulder 90
    # semaphore_servo_data[12][1] = 400 right shoulder 135
    # semaphore_servo_data[13][1] = 520 right shoulder 180

    # set the 3 servo pulse lengths for the 45, 90, and 135 degree positions for both left and right elbow servos
    # each number may have to be fine tuned for the specific servo - see the support documentation for more details

    # semaphore_servo_data[14][1] = 410 left elbow 45
    # semaphore_servo_data[15][1] = 305 left elbow 90
    # semaphore_servo_data[16][1] = 170 left elbow 135

    # semaphore_servo_data[17][1] = 400 right elbow 45
    # semaphore_servo_data[18][1] = 295 right elbow 90
    # semaphore_servo_data[19][1] = 175 right elbow 135

    if semaphore_servo_data_read != "yes":
        semaphore_servo_data = list(csv.reader(open(semaphore_servo_file)))
        semaphore_servo_data_read = "yes"
        print ("semaphore servo data read")

    # signal arrays i.e. letters with additional special signals

    # For most of the letters only the shoulder joints are set 
    # with the elbow joint 'fixed' in the 'straight thru' 90 position
    # but for the letters H, I, O, W, X & Z the elbow joint needs to be set
    # to either 45 or 135 to produce the 'cross body' flag position
    # for H: right elbow to be set to 135
    # for I: right elbow to be set to 45
    # for O: right elbow to be set to 45
    # for W: left elbow to be set to 135
    # for X: left elbow to be set to 135
    # for Z: left elbow to be set to 45
    if semaphore_letters_read != "yes":
        letters = list(csv.reader(open(semaphore_letter_file)))
        letters[0][0] = "A"  # need this fix as the first letter seems to have a spurious character
        semaphore_letters_read = "yes"
        print ("semaphore letters read")

    message_string = message_string.upper()
    print ("text message in UPPER case is: " + message_string)
    message_array = list(message_string)
    #print ("message as an array is: " + str(message_array))
    mylcd.lcd_clear()
    mylcd.lcd_display_string("message text: ", 1, 1) # display at row 1 column 1
    mylcd.lcd_display_string(message_string, 2, 1)   # display at row 2 column 1
    sleep(2)  # short pause to make sure the display above is 'seen'

    # use message letter gap read from the semaphore letter gap file
    letter_interval = readinterval("/home/pi/RPi_maker_kit5/mechatronics/action_sequences01/semaphore_letter_gap.txt")
    print ("letter interval: " + str(letter_interval) + " seconds")

    # loop through the individual letters in the 'message' string
    for i in range (0, len(message_string)):

        #print i
        mylcd.lcd_clear()     
        mylcd.lcd_display_string(message_string, 1, 0)                          # display at row 1 column 0
        #print message_array[i]
        if str(message_array[i]) != " ":
            print ("Working on the letter: " + str(i) + " - " + str(message_array[i]))
            mylcd.lcd_display_string("letter " + str(message_array[i]), 2, 0)   # display at row 2 column 0
        else:
            print ("Working on a 'space' - letter: " + str(i)  )
            mylcd.lcd_display_string("space ", 2, 0)                            # display at row 2 column 0

        # find the chr in the letters array to get the two shoulder servo angles for that letter
        for irow in range(0, 27):  
            #print ("looking at letters row: " + str(irow))
            #print ("looking at letters column 0: " + str(letters[irow][0]) + str(len(letters[irow][0])) )
            if letters[irow][0] == message_array[i]:   # we have found the row - the column should always be 0
                print ("letters row is: " + str(irow))
                print ("left and right shoulder servo angles are: " + str(letters[irow][1]) + " and " + str(letters[irow][2]))
                # set the servo positions with the 'found' servo angles
                set_servo('leftshoulder', letters[irow][1], filedesc, semaphore_servo_data[0][1], semaphore_servo_data[1][1], semaphore_servo_data[2][1], semaphore_servo_data[3][1])
                set_servo('rightshoulder', letters[irow][2], filedesc, semaphore_servo_data[0][1], semaphore_servo_data[1][1], semaphore_servo_data[2][1], semaphore_servo_data[3][1])
                # check if the current letter is one of the special 'elbow' letters
                check_elbow(message_array[i], filedesc, semaphore_servo_data[0][1], semaphore_servo_data[1][1], semaphore_servo_data[2][1], semaphore_servo_data[3][1])

                sleep (letter_interval)
                break
            if irow > 26:
                print ("message letter " + str(i) + " not found")

    return()


#####################################################################
# this is a function to drive the stepper motor for a full revolution
#####################################################################

def stepper_drive(s_counter, s_dir, w_time):
    global stepseq
    global stepselnum
    global stepstop

    # Start main stepper motor loop
    stepseqcyclecount = 0  # this is the number of full 8 step sequence cycles completed
    tstart = time()        # start the clock by recording the current time

    while stepstop == "no":
        #print (s_counter)
        #print (Seq[s_counter])

        for pin in range(0, 4):   # loop through the GPIO pins setting them to HIGH or LOW according to the Seq{} value
            xpin = StepPins[pin]
            if Seq[s_counter][pin]!=0:        # if not 0 then assume 1 so set HIGH (True)
                #print (" Enable GPIO %i" %(xpin))
                GPIO.output(xpin, 1)
            else:
                GPIO.output(xpin, 0)  # if = 0 then set LOW (False)

        s_counter += s_dir    # update the s_counter in ether the forward or backward direction
        if s_counter == -1:     # this means the last item was 0 and we are going backwards
            s_counter = 7         # so this is necessary if we are going backwards
        #print (" step counter: " + str(s_counter))

        # If we reach the end of the sequence start again
        if (s_dir == 1 and s_counter == 7) or (s_dir == -1 and s_counter == 0):
            s_counter = 0
            stepseqcyclecount = stepseqcyclecount + 1
            #print (" 8 step cycle count = " + str(stepseqcyclecount))
            if stepseqcyclecount > 2048/4:  # the full step sequence has 2048 individual steps for a full revolution
                tfinish = time()  # stop the clock by recording the difference between the current and the start times
                if s_dir == 1:
                    print (" full step sequence - forward rotation: this should be 1 full shaft revolution")
                else:
                    print (" full step sequence - backward rotation: this should be 1 full shaft revolution")
                print (" time taken for 1 revolution: " + str(tfinish-tstart) + " seconds")
                #break
                # reset the start parameters for continuous rotation
                stepseqcyclecount = 0
                tstart = time()

        # Wait before moving on - a short wait time is needed as the control board may not be able to keep up
        sleep(w_time)

    return ()

########################################
# this is a function to play a sound
########################################
def play_sound(sound_file_name, time_ms, play_option):   # time_ms not used yet: play_option is either 'once' or 'repeat'
    global sound_folder
    global audio_out
    print ("playing sound")
    print ("sound path: " + sound_folder + sound_file_name)
    print ("time ms: " + time_ms)
    print ("play option: " + play_option)
    # play the sound once/repeat depending upon play_option
    # in a new release use time_ms setting to limit the time the sound is played
    if play_option == "repeat":
        print ("playing sound: repeat")
        player = subprocess.Popen(["omxplayer", "--no-keys", "--loop", "-o", audio_out, sound_folder+sound_file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    elif play_option == "once":
        print ("playing sound: once")
        player = subprocess.Popen(["omxplayer", "--no-keys", "-o", audio_out, sound_folder+sound_file_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        pass


################################################################
# this is a function to get the Raspberry Pi IP address 
################################################################
def getIP():
    try:   # use a try loop in case the mechatronic is not online
        testIP = "8.8.8.8"
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect((testIP, 0))
        ipaddr = s.getsockname()[0]

    except:
        ipaddr = "not online?"

    return ipaddr

################################################################
# this is a function to get the Raspberry Pi MAC address 
#  for any interface - default is the wlan0
###############################################################

def getMAC(interface='wlan0'):
  # Return the MAC address of the specified interface
  try:
    str = open('/sys/class/net/%s/address' %interface).read()
  except:
    str = "00:00:00:00:00:00"
  return str[0:17]

################################################################
# this is a function using the GPIO C library 
#   to indicate when a button is pressed 
################################################################
def btn_pressed(bpin):
    # if button is pressed mechatronics_gpio.read_pin(bpin) will report FALSE ie LOW
    if not mechatronics_gpio.read_pin(bpin):
        return 1

################################################################

##################################################################
#
# function to read the semaphore message text from its SD log file  
#
##################################################################
def readmessage(filepath):
    # open message file to read
    messagefile = open(filepath, "r") # file path passed as a parameter
    message = messagefile.read()
    # close the file
    messagefile.close()
    return(message);


#########################################################################
#
# function to read the semaphore letter gap interval from its SD log file  
#
#########################################################################
def readinterval(filepath):
    # open letter gap file to read
    gapfile = open(filepath, "r") # file path passed as a parameter
    interval = int(gapfile.read())
    # close the file
    gapfile.close()
    return(interval);

#####################################################
## function to set the semaphore elbow servo position
#####################################################
def check_elbow(letter, fd, lsservo, leservo, rsservo, reservo): # check for H, I, O, W, X, or Z

    if letter == "H":
        pulse_left = int(semaphore_servo_data[15][1])
        pulse_right = int(semaphore_servo_data[19][1])
    elif letter == "I":
        pulse_left = int(semaphore_servo_data[15][1])
        pulse_right = int(semaphore_servo_data[17][1])
    elif letter == "O":
        pulse_left = int(semaphore_servo_data[15][1])
        pulse_right = int(semaphore_servo_data[17][1])

    elif letter == "W":
        pulse_left = int(semaphore_servo_data[16][1])
        pulse_right = int(semaphore_servo_data[18][1])
    elif letter == "X":
        pulse_left = int(semaphore_servo_data[16][1])
        pulse_right = int(semaphore_servo_data[18][1])
    elif letter == "Z":
        pulse_left = int(semaphore_servo_data[14][1])
        pulse_right = int(semaphore_servo_data[18][1])

    else:
        pulse_left = int(semaphore_servo_data[15][1])
        pulse_right = int(semaphore_servo_data[18][1])

    # set the left elbow 
    picontrol_servo.setServo(fd, int(leservo), pulse_left, 5)

    # set the right elbow 
    picontrol_servo.setServo(fd, int(reservo), pulse_right, 5)

    print ("left and right elbow servo pulses are: " + str(pulse_left) + " and " + str(pulse_right) )

    return ()


######################################################
## generic function to set a semaphore servo position
######################################################
def set_servo(joint, angle, fd, lsservo, leservo, rsservo, reservo):
    # convert the main passed parameters to integers
    angle = int(angle)
    lsservo = int(lsservo)
    leservo = int(leservo)
    rsservo = int(rsservo)
    reservo = int(reservo)

    if joint == "leftshoulder":
        channel = lsservo
        if angle == 0:
            servo_pulse = int(semaphore_servo_data[4][1])
        elif angle == 45:
            servo_pulse = int(semaphore_servo_data[5][1])
        elif angle == 90:
            servo_pulse = int(semaphore_servo_data[6][1])
        elif angle == 135:
            servo_pulse = int(semaphore_servo_data[7][1])
        elif angle == 180:
            servo_pulse = int(semaphore_servo_data[8][1])
        else:
            print ("incorrect servo angle set for left shoulder")
            return ()

    elif joint =="leftelbow":
        channel = leservo
        if angle == 45:
            servo_pulse = int(semaphore_servo_data[14][1])
        elif angle == 90:
            servo_pulse = int(semaphore_servo_data[15][1])
        elif angle == 135:
            servo_pulse = int(semaphore_servo_data[16][1])
        else:
            print ("incorrect servo angle set for left elbow")
            return ()

    elif joint == "rightshoulder":
        channel = rsservo
        if angle == 0:
            servo_pulse = int(semaphore_servo_data[9][1])
        elif angle == 90:
            servo_pulse = int(semaphore_servo_data[11][1])
        elif angle == 135:
            servo_pulse = int(semaphore_servo_data[12][1])
        elif angle == 180:
            servo_pulse = int(semaphore_servo_data[13][1])
        else:
            print ("incorrect servo angle set for right shoulder")
            return ()

    elif joint =="rightelbow":
        channel = reservo
        if angle == 45:
            servo_pulse = int(semaphore_servo_data[17][1])
        elif angle == 90:
            servo_pulse = int(semaphore_servo_data[18][1])
        elif angle == 135:
            servo_pulse = int(semaphore_servo_data[19][1])
        else:
            print ("incorrect servo angle set for right elbow")
            return ()


    else:
        print ("incorrect joint value in the set_servo function")
        return ()

    print ("channel, servo_pulse: " + str(channel) + ", " + str(servo_pulse) )
    picontrol_servo.setServo(fd, channel, servo_pulse, 5)
    return ()

#################################################
# this is a simple function to indicate when a 
#  pulled-up switch is pressed using RPI GPIO
#################################################
def btn_pressed(bpin):
    # if button is pressed GPIO.input will report LOW/FALSE
    if not GPIO.input(bpin):
        return 1

###################################
# buzzer 'tune' player function
###################################
def play(melody,tempo,pause,pace=0.800):
    for i in range(0, len(melody)):		# Play song
        noteDuration = pace/tempo[i]
        buzz(melody[i],noteDuration, 'yes')	# Change the frequency along the song note
        pauseBetweenNotes = noteDuration * pause
        sleep(pauseBetweenNotes)

####################################################################
# function to read the standard music notes from their log file 
#####################################################################
def readnotes():
    # open notes file to read
    notesfile = open("/home/pi/RPi_maker_kit5/mechatronics/sounds/mechatronic_notes.txt", "r") # file path hardcoded
    readnotes = notesfile.read()
    notes = eval(readnotes)
    # close the log file
    notesfile.close()
    return(notes);

####################################################################
#  basic buzzer functions
#  only does something if the 'installed' parameter is 'yes'
#  and assumes the buzzer pin is already set as an OUTPUT
####################################################################

def buzz(frequency, length, installed):	 #function "buzz" is fed the pitch (frequency) and duration (length in seconds)
    if installed == 'yes':
        # allow for a 'silent' duration
        if(frequency==0):
            sleep(length)
            return
        period = 1.0 / frequency 		     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
        delayValue = period / 2		         #calcuate the time for half of the wave
        numCycles = int(length * frequency)	 #the number of waves to produce is the duration times the frequency
	
        for i in range(numCycles):		   #start a loop from 0 to the variable "cycles" calculated above
            GPIO.output(buzzer_pin, True)  #set buzzer pin to high
            sleep(delayValue)		   #wait with buzzer pin high
            GPIO.output(buzzer_pin, False) #set buzzer pin to low
            sleep(delayValue)		   #wait with buzzer pin low

def beep(number, length):  # simple function for beep length and on/off for 'number' times at standard beep frequency 1200Hz
    for i in range(1, number+1):
        #print ("beep: " + str(i))
        buzz(1200, length, 'yes')
        sleep(length)


####################################################################
#  function to set a LED ON/OFF
#  only does something if the 'installed' parameter is 'yes'
#  and assumes the LED_pin is already set as an OUTPUT
####################################################################
def LED_set(LED_pin, set):
    if set == 'ON':
        GPIO.output(LED_pin, 1)
    else:
        GPIO.output(LED_pin, 0)



########################################################
####                   main code                    ####
########################################################

import I2C_LCD_driver
from time import *
import numpy as np
import subprocess
from ctypes import *
import socket
import os
from os import listdir
from os.path import isfile, join
import sys
import csv   # used to read data into 2-dimensional arrays e.g. for letters and other semaphore data
from flask import Flask, render_template, flash, request, redirect, url_for, Response
from werkzeug.utils import secure_filename
import RPi.GPIO as GPIO   # this imports the module to allow the GPIO pins to be easily utilised

GPIO.setwarnings(False)
# This code sets the RPi to use the BCM (Broadcom) pin numbers which is usually the default but is positively set here
GPIO.setmode(GPIO.BCM)

# RAG LEDs - just used to show the the system startup cycle/status
redpin = 16
amberpin = 20
greenpin = 21
GPIO.setup(redpin, GPIO.OUT)
GPIO.output(redpin, 1)         # set RED LED ON as near to the start of the system switch on as possible
GPIO.setup(amberpin, GPIO.OUT)
GPIO.output(amberpin, 0)       # set AMBER LED OFF at system switch on
GPIO.setup(greenpin, GPIO.OUT)
GPIO.output(greenpin, 0)       # set GREEN LED OFF at system switch on

# RGB pins - used to show cycle/status for individual device actions
RGBred = 22
RGBgreen = 27
RGBblue = 17
GPIO.setup(RGBred, GPIO.OUT)
GPIO.output(RGBred, 0)         # set RED RGB OFF at system switch on
GPIO.setup(RGBgreen, GPIO.OUT)
GPIO.output(RGBgreen, 0)       # set GREEN RGB OFF at system switch on
GPIO.setup(RGBblue, GPIO.OUT)
GPIO.output(RGBblue, 0)        # set BLUE RGB OFF at system switch on

# passive buzzer
buzzpin = 12
GPIO.setup(buzzpin, GPIO.OUT)

# set up the LCD display function
mylcd = I2C_LCD_driver.lcd()
lcddisp("system starting.", "***************", 1)

# hardware variable used to show which type of Raspberry Pi SBC is being used
#   - and therefore could 'constrain' some operations that can be carried out
global hardware
hardware = subprocess.check_output("cat /proc/device-tree/model", shell=True)
hardware = hardware.decode("utf-8")
print("hardware: " + hardware)
hardware = hardware.replace(" Plus","+")
hardware = hardware.replace("Raspberry Pi ","RPi")
print("updated hardware: " + hardware)

global semaphore_letters_read 
semaphore_letters_read = "no"     # made global so that the data is available to the web 'route' functions
global semaphore_servo_data_read 
semaphore_servo_data_read = "no"  # made global so that the data is available to the web 'route' functions

global message 
message = ""
global message_read 
message_read = "no"   # made global so that the data is available to the web 'route' functions

global semaphore_servo_data        # made global so that the data is available to the web 'route' functions
global letters                     # made global so that the data is available to the web 'route' functions

GPIO.output(redpin, 0)         # set RED LED OFF
GPIO.output(amberpin, 1)       # set AMBER LED ON at the start of config processing

# display the startup text on the screen + LCD
print ("displaying the system config text")
lcddisp("mechatronic .....", "config starting", 2)

print ("setting up the Flask object")
mechatronic_app01 = Flask(__name__)  # creates a Flask web server object called mechatronic_app01 for the web mode
mechatronic_app01.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024   # used to limit a soundfile upload size to 1MB
#mechatronic_app01.config['SOUND_FOLDER'] = "/home/pi/RPi_maker_kit5/mechatronics/sounds/"
mechatronic_app01.secret_key = "secret key"
lcddisp("system config", "Flask setup OK..", 1)

####################################################################
##  ** series of checks that the various data files are available **
####################################################################
# check that the servo_objects_file, servo_channels_file, stepper_options_file, and custom_servo_objects_file all exist
if os.path.isfile(servo_channels_file):
    lcddisp("system config", "s-chan file OK", 1)
else:
    lcddisp("*SYSTEM STOPPED*", "NO s-chan file", 1)
    sys.exit()
# ---------------------------------------------------------------------------------
if os.path.isfile(servo_objects_file):
    lcddisp("system config", "s-obj file OK", 1)
else:
    lcddisp("*SYSTEM STOPPED*", "NO s-object file", 1)
    sys.exit()
# ---------------------------------------------------------------------------------
if os.path.isfile(stepper_options_file):
    lcddisp("system config", "step-opt file OK", 1)
else:
    lcddisp("*SYSTEM STOPPED*", "NO step-opt file", 1)
    sys.exit()
# ---------------------------------------------------------------------------------
if os.path.isfile(mdrive_objects_file):
    lcddisp("system config", "dm-obj file OK", 1)
else:
    lcddisp("*SYSTEM STOPPED*", "NO dm-obj file", 3)
    sys.exit()
# --------------------------------------------------------------------------------
if os.path.isfile(custom_servo_objects_file):
    lcddisp("system config", "cust-opt file OK", 1)
else:
    lcddisp("*SYSTEM STOPPED*", "NO cust-opt file", 1)
    sys.exit()
# --------------------------------------------------------------------------------

# --------------------------------------------------------------------------------
# servo object variables
# -------------------------------------------------------------------------------
# read in the servo objects that have been set up so far along with the special servo channels data
#  **note** the file names are 'latched' to the file format version and hence the sofware version
#      as different s/w versions may have different file layouts/formats for the text
# the default dtype for  np.loadtxt is for floating point content, so change it to be able to load mixed data.
global an_objects     # array for all the currently defined servo objects: # made global so that the data is available to the web 'route' functions
# NB the object name, sequence file name and description have underscores instead of spaces
an_objects = np.loadtxt(servo_objects_file, dtype=np.object)

global object_number   # the number of currently defined servo objects: made global so that the data is available to the web 'route' functions
object_number = len(an_objects)-1    # number of defined servo objects:  len -1 because the 1st row is just the header titles

print (" number of servo objects defined is " + str(object_number) )

lcddisp("system config", "servo objects: "+ str(object_number), 1)

global an_objects_read   # used to minimise the number of times the data has to be read
an_objects_read = "yes"

global obseq   # used for the individual servo action sequences & made global so that the data is available to the web 'route' functions
global obseq_read  # used to minimise the number of times the data has to be read
obseq_read = "no"
global servo_channels  # used to capture the servo channel# and short description used by each servo object
servo_channels = np.loadtxt(servo_channels_file, dtype=np.object)
global servochanrows   # the number of rows in the servo_channels array which should be #objects+1 ie object_number+1
servochanrows = servo_channels.shape[0]
print ("servo channels loaded: number of rows " +str(servo_channels.shape[0]) )
global servo_channels_read   # used to minimise the number of times the data has to be read
servo_channels_read = "yes"

global servoselnum # used for the currently selected servo object: made global so that the data is available to the web 'route' functions
servoselnum = 0

global servostop   # used to signify that a servo object operation has been stopped: made global so that the data is available to the web 'route' functions
servostop ="yes"

# --------------------------------------------------------------------------------
# stepper object variables
# --------------------------------------------------------------------------------
# read in the stepper options that have been set up so far
#  **note** the file name is 'latched' to the sofware version
#      as different s/w versions may have different file formats
# the default dtype for  np.loadtxt is for floating point content, so change it to be able to load mixed data.
global step_options  # array for all the currently defined stepper objects: made global so that the data is available to the web 'route' functions
step_options = np.loadtxt(stepper_options_file, dtype=np.object)
global sopt_number   # the number of currently defined stepper objects: made global so that the data is available to the web 'route' functions
sopt_number = len(step_options)-1   # number of defined stepper objects: len -1 because the 1st row is just the header titles
# replace any _ characters in the descriptions fields with spaces as spaces are not allowed in the file
for i in range (1, sopt_number+1):
    step_options[i][3]=step_options[i][3].replace("_", " ")
print (" number of stepper options defined is " + str(sopt_number) )

lcddisp("system config", "s-opt options: "+ str(sopt_number), 1)

global step_options_read   # used to minimise the number of times the data has to be read
step_options_read = "yes"

global stepseq   # used for the individual stepper action sequences: made global so that the data is available to the web 'route' functions
global stepseq_read  # used to minimise the number of times the data has to be read
stepseq_read = "no"
global stepselnum  # used for the currently selected stepper object: made global so that the data is available to the web 'route' functions
stepselnum = 0

global stepstop    # used to signify that a stepper object operation has been stopped: made global so that the data is available to the web 'route' functions
stepstop ="yes"

# -------------------------------------------------------------------------
### set up the motor drive object variables IF they are being used yet  ###
# -------------------------------------------------------------------------
global mdrive_objects
global mdrivestop    # used to signify that a motor drive object operation has been stopped: made global so data is available to the web
mdrivestop = 'yes'
global mdrive_number   # the number of defined mdrive objects: made global so that the data is available to the web 'route' functions
mdrive_number = 0
# read in the motor drive objects that have been set up so far
#  **note** the file name is 'latched' to the sofware version
#      as different s/w versions may have different file formats
# the default dtype for  np.loadtxt is for floating point content, so change it to be able to load mixed data.
global mdrive_objects  # array for defined motor drive objects: made global so that the data is available to the web 'route' functions
mdrive_objects = np.loadtxt(mdrive_objects_file, dtype=np.object)
mdrive_number = len(mdrive_objects)-1   # number of defined mdrive objects: len -1 because the 1st row is just the header titles
# replace any _ characters in the descriptions fields with spaces as spaces are not allowed in the file
#for i in range (1, mdrive_number+1):
#   mdrive_objects[i][3]=mdrive_objects[i][3].replace("_", " ")
print (" number of motor drive defined is " + str(mdrive_number) )

lcddisp("system config", "mdrive-objs: "+ str(mdrive_number), 1)

global mdrive_obj_read   # used to minimise the number of times the data has to be read
mdrive_obj_read = "yes"

global mdriveseq   # used for the individual motor drive action sequences: made global so data is available to the web 'route' functions
global mdriveseq_read  # used to minimise the number of times the data has to be read
mdriveseq_read = "no"
global mdriveselnum  # used for the currently selected motor drive object: made global so data is available to the web 'route' functions
mdriveselnum = 0

drivestop ="yes"

# --------------------------------------------------------------------------------
# custom servo object variables
# --------------------------------------------------------------------------------
# read in the custom servo objects that have been set up so far
#  **note** the file name is 'latched' to the sofware version
#      as different s/w versions may have different file formats
# the default dtype for  np.loadtxt is for floating point content, so change it to be able to load mixed data.
global cust_objects  # made global so that the data is available to the web 'route' functions
cust_objects = np.loadtxt(custom_servo_objects_file, dtype=np.object)
global cust_number   # made global so that the data is available to the web 'route' functions
cust_number = len(cust_objects)-1   # len -1 because the 1st row is just the header titles
# replace any _ characters in the descriptions fields with spaces
for i in range (1, cust_number+1):
    cust_objects[i][3]=cust_objects[i][3].replace("_", " ")
print (" number of custom servo objects defined is " + str(cust_number) )
lcddisp("system config", "cust options: "+ str(cust_number), 1)

global custstop   # made global so that the data is available to the web 'route' functions
custstop = "yes"

global semaphore_stop  # made global so that the data is available to the web 'route' functions
semaphore_stop = "no"

global robotarm_stop   # made global so that the data is available to the web 'route' functions
robotarm_stop ="no"
# --------------------------------------------------------------------------------
global soundfiles
global soundfile_sel
soundfile_sel = 0
global soundfiles_num
soundfiles_num = 0
global soundfile_read
soundfolder_read = "no"

# --------------------------------------------------------------------------------

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
global filedesc   # made global so that the data is available to the web 'route' functions
filedesc = picontrol_servo.PWMsetup(0x40, 50)  # sets up the board and retrieves the I2C file descriptor for later use
print ("I2C file descriptor is: " + str(filedesc))
print ("  ")
lcddisp("system config", "  servos set up ", 1)

# GPIO pin numbering for the various Maker Kit items e.g. the buttons, the stepper motor control module pins, etc.
# these numbers are all hard coded as they are fixed by the Maker Kit PCB construction

# top and bottom buttons
button1pin = 7
button2pin = 26
GPIO.setup(button1pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(button2pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# stepper motor
stepIN1pin = 8
stepIN2pin = 11
stepIN3pin = 9
stepIN4pin = 10
GPIO.setup(stepIN1pin, GPIO.OUT)
GPIO.setup(stepIN2pin, GPIO.OUT)
GPIO.setup(stepIN3pin, GPIO.OUT)
GPIO.setup(stepIN4pin, GPIO.OUT)

# mdrive motor GPIO settings - IF it is being used (L298N motor controller assumed)
mdrive_enA = 24 # servo1 on the Maker Kit PCB
mdrive_IN1 = 4  # spare GPIO on the Maker Kit PCB
mdrive_IN2 = 14 # spare GPIO on the Maker Kit PCB
mdrive_IN3 = 15 # spare GPIO on the Maker Kit PCB
mdrive_IN4 = 18 # spare GPIO on the Maker Kit PCB
mdrive_enB = 25 # servo2 on the Maker Kit PCB
GPIO.setup(mdrive_enA, GPIO.OUT)
GPIO.setup(mdrive_IN1, GPIO.OUT)
GPIO.setup(mdrive_IN2, GPIO.OUT)
GPIO.setup(mdrive_IN3, GPIO.OUT)
GPIO.setup(mdrive_IN4, GPIO.OUT)
GPIO.setup(mdrive_enB, GPIO.OUT)

pwm_enA = GPIO.PWM(mdrive_enA, 20)  # set the enA pin as a software set PWM pin with frequency 20
pwm_enB = GPIO.PWM(mdrive_enB, 20)  # set the enB pin as a software set PWM pin with frequency 20
# Start the software PWM pins with a duty cycle of 0 (i.e. motors not moving)
pwm_enA.start(0)
pwm_enB.start(0)

lcddisp("system config", " mdrives set up", 1)


##############################################################################################
# one-time set up for the stepper motor so it can be used with any subsequent switch settings
##############################################################################################
StepPins = [stepIN1pin,stepIN2pin,stepIN3pin,stepIN4pin]    # set all the stepper motor controller GPIO pins into an array
# Set all the stepper motor controller GPIO pins initially set LOW
for pin in StepPins:
   #print ("Setup pins")
   GPIO.output(pin, 0)   # set all the stepper control pins LOW to start
# Define the phase sequence for the unipolar stepper motor i.e.
# for GPIO pins IN1, IN2, IN3 and IN4 connected to the drive coils using  
# the blue & yellow (coil 1) plus pink & orange (coil 2) wires
# the red wire is the common centre tap for both drive coils
# as shown in manufacturers datasheet
# Full step sequence: sets two phases at a time producing a 0.18 degree step angle 
#  and twice the torque as two coils are energised at the same time
Seq = [[1,0,0,1],
       [1,1,0,0],
       [0,1,1,0],
       [0,0,1,1],
       [1,0,0,1],
       [1,1,0,0],
       [0,1,1,0],
       [0,0,1,1]]
StepCount = len(Seq)
StepDir = -1  # Set to 1 for clockwise
              # Set to -1 for anti-clockwise

FullTime = 2/float(1000)  # shortest time that works to give the highest speed - might need to be fine tuned
HalfTime = 2*FullTime     # wait time for half speed option - might need to be fine tuned
WaitTime = FullTime       # default to full speed to start
# Initialise variables
StepCounter = 0
if StepDir == -1:
    StepCounter = 7
lcddisp("system config", "  stepper set up", 1)

#############################################
global audio_out
audio_out = "local"  # set to either local or hdmi to play the sounds to either the local audio output socket or via HDMI

################################
# web mode ready to use
################################
GPIO.output(greenpin, 1)       # set GREEN LED ON when system is ready
GPIO.output(amberpin, 0)       # set AMBER LED OFF
lcddisp("web mode active.", "*system ready*", 1)

try:    # using try ahead of the 'while' loop allows CTRL-C to be used to cleanly end the cycle
    # the following is just an endless loop
    ######################
    #  start of main loop
    ######################
    while True:

        ###############################################################################
        # this route goes to the selection mode routine when the URL root is selected
        ###############################################################################
        @mechatronic_app01.route("/") # run the code below this function when the URL root is accessed
        def start():
            # display the web control select text on the LCD
            print ("displaying the web control select text")
            mylcd.lcd_clear()
            mylcd.lcd_display_string("mechatronics    ..", 1, 0) # display at row 1 column 1
            mylcd.lcd_display_string("select an option", 2, 0) # display at row 2 column 1

            template_data = {
            'title' : "main options selection",
            'description' : "Raspberry Pi powered stepper and servo motor controller",
            }
            return render_template('select_mode.html', **template_data)


        ################################################################################################
        # this route runs the various stepper options when one of the <stepper_option> URLs is selected
        ################################################################################################
        @mechatronic_app01.route("/stepper/<stepper_option>") # run the code below this function when <stepper_option> is accessed where stepper_option is a variable
        def stepperopt(stepper_option=None):
            global step_options
            global stepseq
            global stepselnum
            global stepstop
            global sopt_number
            global servo_channels
            global mdrivestop

            # display the web control select text on the LCD
            print ("displaying the web control select text")
            mylcd.lcd_clear()
            mylcd.lcd_display_string("mechatronics    ..", 1, 0) # display at row 1 column 1
            mylcd.lcd_display_string("stepper options:", 2, 0) # display at row 2 column 1
            print (" start route " )
            print (" stepper_option[0:14]: " + str(stepper_option[0:14]))
            if stepper_option == 'stepper_list':
                print (" - in stepper_option: list")
                stepselnum = 0
                webwarning = "" 

            elif stepper_option[0:14] == 'stepper_choose':
                print (" - in stepper_option: choose")
                webwarning = "" 
                stepselnum = int(''.join(filter(str.isdigit, stepper_option)))  #  extract the object number from the passed URL 
                if stepselnum >0 and stepselnum <= sopt_number:
                    print ("object# selected: " + str(stepselnum))
                    webwarning = "SELECTED: stepper object " + str(stepselnum) + " - " + str(step_options[stepselnum][0])
                    # now get the stepper activity sequences from its file
                    #  - but first check that the file is in the system
                    if os.path.isfile(action_folder+str(step_options[stepselnum][2])):
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string("stepper run ON", 1, 0)   # display at row 1 column 0
                        mylcd.lcd_display_string("action file OK", 2, 0)    # display at row 2 column 0
                        print ("stepper action file " + str(step_options[stepselnum][2]) + " found OK")
                        sleep(1)  # short pause so that the LCD display above is 'seen'
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string("stepper run ON", 1, 0)   # display at row 1 column 0
                        mylcd.lcd_display_string(str(step_options[stepselnum][2]), 2, 0) # display at row 2 column 0
                        print ("stepper action file " + str(step_options[stepselnum][2]) + " selected")

                        # the default dtype for np.loadtxt is for floating point content, so change it to be able to load mixed data.
                        stepseq = np.loadtxt(action_folder+str(step_options[stepselnum][2]), dtype=np.object)
                        print ("step activity sequence loaded")
                    else:
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string("*FILE ERROR*", 1, 0)  # display at row 1 column 0
                        mylcd.lcd_display_string("*NO action file*", 2, 0) # display at row 2 column 0
                        print ("action file " + str(step_options[stepselnum][2]) + " NOT found")
                        webwarning = "FILE ERROR: stepper object "+str(stepselnum)+" - "+str(step_options[stepselnum][0])+" - file not found"
                        stepselnum = 0
                else:
                    stepselnum = 0
                    webwarning = "WARNING: selected stepper object# is out of range"

            elif stepper_option == 'stepper_run':
                print (" - in stepper_option: run")
                # for this version of the code only 1 line of 'actions' can be processed
                # so only process activity 'line' row 1 since row 0 just has the header labels

                stepstop ="no"
                # check that a valid stepper object has been chosen before trying to 'run'
                if stepselnum >0 and stepselnum <= sopt_number:
                    for row in range (1, 2):    # when more rows can be processed use (1, int(len(obseq)))
                        print (" processing activity sequence row " + str(row) )
                        # ------------------------------------------------------------------------------------------------------
                        # run the 'stepper motor' activities: setting direction, speed and sound from the activity sequence file
                        # ------------------------------------------------------------------------------------------------------

                        # start sound as a background process unless it is set to 'nothing'
                        print (" sound file: " + str(stepseq[row][3]) )
                        if str(stepseq[row][3]) != "nothing":
                            # play the sound once/repeat depending upon stepseq[row][5]
                            # in a new release use the time_ms setting, stepseq[row][4], to limit the time the sound is played
                            #   but just set to a dummy value for now
                            play_sound(str(stepseq[row][3]), "all", str(stepseq[row][5]))
                        else:
                            pass

                        print ("direction: " + str(stepseq[row][1]) )
                        print ("speed: " + str(stepseq[row][2]) )
                        if stepseq[row][1] == "clock":
                            StepDir = 1
                        else:
                            StepDir = -1

                        StepCounter = 0
                        if StepDir == -1:
                            StepCounter = 7

                        if stepseq[row][2] == "full":
                            WaitTime = FullTime
                        else:
                            WaitTime = HalfTime

                        webwarning = "" 
                        stepper_drive(StepCounter, StepDir, WaitTime)

                else:
                        webwarning = "WARNING: stepper object# NOT selected "

            elif stepper_option == 'stepper_stop':
                print (" - in stepper_option: stop")
                stepstop ="yes"
                webwarning = "" 
                # Set all the stepper motor controller GPIO pins LOW
                print ("Stepper control pins: setting them LOW")
                for pin in StepPins:
                    print ("pin: " + str(pin) + " set LOW")
                    GPIO.output(pin, 0)

                # stop any sounds that might be playing
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")

            else:
                template_data = {
                    'title' : "main options selection",
                    'description' : "Raspberry Pi powered stepper and servo motor controller",
                }
                return render_template('select_mode.html', **template_data)

            template_data = {
                'title' : "stepper motor operation",
                'description' : "stepper motor controller options",
                'stepperobjs' : sopt_number,
                'selstepobj' : stepselnum,
                'warnweb' : webwarning,
            }
            return render_template('stepper_options.html', **template_data, step_options = step_options)


        #################################################################################
        # this route runs the various servo options when /servo_options is selected
        #################################################################################
        @mechatronic_app01.route("/servo/<servo_option>") # run the code below this function when <servo_option> is accessed where servo_option is a variable
        def servoopt(servo_option=None):
            global an_objects
            global obseq
            global servoselnum
            global servochanrows
            global servostop
            global object_number
            global filedesc
            global mdrivestop

            # display the web control select text on the LCD
            print ("displaying the web control select text")
            mylcd.lcd_clear()
            mylcd.lcd_display_string("mechatronics    ..", 1, 0) # display at row 1 column 1
            mylcd.lcd_display_string("servo options:", 2, 0) # display at row 2 column 1
            print (" start route " )
            print (" servo_option[0:12]: " + str(servo_option[0:12]))
            if servo_option == 'servo_list':
                print (" - in servo_option: list")
                servoselnum = 0
                webwarning = "" 

            elif servo_option[0:12] == 'servo_choose':
                print (" - in servo_option: choose")
                servoselnum = int(''.join(filter(str.isdigit, servo_option)))  #  extract the object number from the passed URL
                webwarning = ""
                if servoselnum > 0 and servoselnum <= object_number:
                    servostop = "no"
                    print ("servostop: " + servostop + " - object# selected: " + str(servoselnum))
                    webwarning = "SELECTED: servo object " +str(servoselnum) + " - " + str(an_objects[servoselnum][0])
                    # now get the servo activity sequences from its file
                    #   - but check the servo activity file exists before opening it
                    if os.path.isfile(action_folder+str(an_objects[servoselnum][2])):
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string("servo move ON", 1, 0)   # display at row 1 column 0
                        mylcd.lcd_display_string("servo file OK", 2, 0)    # display at row 2 column 0
                        print ("servo object file " + str(an_objects[servoselnum][2]) + " found OK")
                        sleep(1)  # short pause so that the LCD display above is 'seen'
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string("servo selected", 1, 0)   # display at row 1 column 0
                        mylcd.lcd_display_string(str(an_objects[servoselnum][0]), 2, 0) # display at row 2 column 0
                        # the default dtype for  np.loadtxt is for floating point content, so change it to be able to load mixed data.
                        obseq = np.loadtxt(action_folder+str(an_objects[servoselnum][2]), dtype=np.object)
                        print ("servo activity sequence loaded")
                    else:
                        mylcd.lcd_clear()
                        mylcd.lcd_display_string("*FILE ERROR*", 1, 0)  # display at row 1 column 0
                        mylcd.lcd_display_string("*NO action file*", 2, 0) # display at row 2 column 0
                        print ("servo object file " + str(an_objects[servoselnum][2]) + " NOT found")
                        webwarning = "FILE ERROR: servo object "+str(servoselnum)+" - "+str(an_objects[servoselnum][0])+" - file not found"
                        servoselnum = 0
                else:
                    servoselnum = 0
                    webwarning ="WARNING selected servo object# is out of range"

                #  *** the default/common template generation code is at the end of the if/elif/else sequence ***

            elif servo_option == 'servo_run':
                print (" - in servo_option: run")
                webwarning = "" 
                print ("servostop: " + servostop + " - servo: " + str(servoselnum) + " running")

                # check that a valid servo object has been chosen before trying to 'run'
                if servoselnum > 0 and servoselnum <= object_number and servostop == "no":
                    webwarning = "RUNNING: servo object " +str(servoselnum)

                    for row in range (1, int(len(obseq))):

                        for repeat in range (1, int(obseq[row][8])+1):
                            print ("-repeat cycle: " + str(repeat))

                            print (" processing activity sequence row " + str(row) )
                            # -----------------------------------------------------------------------
                            # run the 'servo motor' activities defined by the activity sequence file
                            # -----------------------------------------------------------------------
                            ### action value 1 ###
                            # check sound file is needed before trying to play it
                            if str(obseq[row][3]) != "nothing" and servostop == "no":
                                if os.path.isfile(sound_folder+str(obseq[row][3])):
                                    mylcd.lcd_clear()
                                    mylcd.lcd_display_string("servo move ON", 1, 0)   # display at row 1 column 0
                                    mylcd.lcd_display_string("sound file OK", 2, 0)   # display at row 2 column 0
                                    print ("sound file " + str(obseq[row][3]) + " found OK")
                                    sleep(1)
                                    mylcd.lcd_clear()
                                    mylcd.lcd_display_string("servo move ON", 1, 0)   # display at row 1 column 0
                                    mylcd.lcd_display_string(str(an_objects[servoselnum][0]), 2, 0) # display at row 2 column 0
                                    play_sound(str(obseq[row][3]), "all", "once") # start action value 1 sound as a background process

                                else:
                                    mylcd.lcd_clear()
                                    mylcd.lcd_display_string("*SYSTEM STOPPED*", 1, 0)  # display at row 1 column 0
                                    mylcd.lcd_display_string("NO sound file", 2, 0) # display at row 2 column 0
                                    print ("sound file " + str(obseq[row][3]) + " NOT found")
                                    sleep(3)
                                    sys.exit()

                            # make value 1 servo movement with its associated wait time (or minimum 50ms)
                            print (" servo value1: " + str(int(obseq[row][2])))
                            if servostop == "no":
                                if int(obseq[row][4]) > 50:
                                    picontrol_servo.setServo(filedesc, int(obseq[row][0]), int(obseq[row][2]), int(obseq[row][4]))
                                else:
                                    picontrol_servo.setServo(filedesc, int(obseq[row][0]), int(obseq[row][2]), 50)

                            ### action value 2 ###
                            # check sound file is needed before trying to play it
                            if str(obseq[row][6]) != "nothing" and servostop == "no":
                                if os.path.isfile(sound_folder+str(obseq[row][6])):   # check the sound file is on the system
                                    mylcd.lcd_clear()
                                    mylcd.lcd_display_string("servo move ON", 1, 0)   # display at row 1 column 0
                                    mylcd.lcd_display_string("sound file OK", 2, 0)   # display at row 2 column 0
                                    print ("sound file " + str(obseq[row][6]) + " found OK")
                                    sleep(1)
                                    mylcd.lcd_clear()
                                    mylcd.lcd_display_string("servo move ON", 1, 0)   # display at row 1 column 0
                                    mylcd.lcd_display_string(str(an_objects[servoselnum][0]), 2, 0) # display at row 2 column 0
                                    play_sound(str(obseq[row][6]), "all", "once")  

                                else:
                                    mylcd.lcd_clear()
                                    mylcd.lcd_display_string("*SYSTEM STOPPED*", 1, 0)  # display at row 1 column 0
                                    mylcd.lcd_display_string("NO sound file", 2, 0) # display at row 2 column 0
                                    print ("sound file " + str(obseq[row][6]) + " NOT found")
                                    sleep(3)
                                    sys.exit()

                            # make value 2 servo movement with its associated wait time (or minimum 50ms)
                            print (" servo value2: " + str(int(obseq[row][5])))
                            if servostop == "no":
                                if int(obseq[row][7]) > 50:
                                    picontrol_servo.setServo(filedesc, int(obseq[row][0]), int(obseq[row][5]), int(obseq[row][7]))
                                else:
                                    picontrol_servo.setServo(filedesc, int(obseq[row][0]), int(obseq[row][5]), 50)

                            # 'just in case' stop the audio from playing so that each repeat cycle gets a 'clean' start for any sounds
                            player = subprocess.Popen(["omxplayer", "q" ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                            print ("  ")

                #  *** the default/common template generation code is at the end of the if/elif/else sequence ***

            elif servo_option == 'servo_stop':
                print (" - in servo_option: stop")
                servostop = "yes"
                webwarning = "" 
                if servoselnum > 0 and servoselnum <= object_number:
                    webwarning = "SELECTED: servo object " +str(servoselnum)

                # return servos to default position?

                # stop any sounds that might be playing
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")

                #  *** the default/common template generation code is at the end of the if/elif/else sequence ***

            else:
                template_data = {
                    'title' : "main options selection",
                    'description' : "Raspberry Pi powered stepper and servo motor controller",
                }
                return render_template('select_mode.html', **template_data)


            ##  if here then display the default servo_options.html template

            template_data = {
                'title' : "servo motor operation",
                'description' : "servo motor controller options",
                'servoobjs' : object_number,
                'selservoobj' : servoselnum,
                'warnweb' : webwarning,
                'rowsservochans' : servochanrows,

            }
            return render_template('servo_options.html', **template_data, an_objects = an_objects, servo_channels = servo_channels)


        ####################################################################################################
        # this route runs the various motor drive options when one of the <mdrive_option> URLs is selected
        ####################################################################################################
        @mechatronic_app01.route("/mdrive/<mdrive_option>") # run the code below this function when <mdrive_option> is accessed where mdrive_option is a variable
        def mdriveobj(mdrive_option=None):
            global mdrive_objects
            global mdriveseq
            global mdriveselnum
            global mdrivestop
            global mdrive_number

            # display the web control select text on the LCD
            print ("displaying the web control select text")
            lcddisp("mechatronic web..", "mdrive objects:", 0.1)
            print (" mdrive_option[0:13]: " + str(mdrive_option[0:13]))
            if mdrive_option == 'mdrive_list':
                print (" - in mdrive_option: list")
                mdriveselnum = 0
                webwarning = "" 
                mdrive_option_last = 'mdrive_list'

            elif mdrive_option[0:13] == 'mdrive_choose':
                print (" - *** in mdrive_option: choose")
                webwarning = "" 
                mdrivestop = 'no'
                mdrive_option_last = 'mdrive_choose'
                mdriveselnum = int(''.join(filter(str.isdigit, mdrive_option)))  #  extract the object number from the passed URL 
                if mdriveselnum >0 and mdriveselnum <= mdrive_number:
                    print ("object# selected: " + str(mdriveselnum))
                    webwarning = "SELECTED: motor drive object " + str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])
                    # now get the motor drive activity sequences from its file
                    #  - but first check that the file is in the system
                    if os.path.isfile(action_folder+str(mdrive_objects[mdriveselnum][2])):
                        lcddisp("mdrive run ON", "action file OK", 0.1)
                        print ("drive motor action file " + str(mdrive_objects[mdriveselnum][2]) + " found OK")
                        lcddisp("mdrive selected", str(mdrive_objects[mdriveselnum][0]), 0.1)
                        # the default dtype for  np.loadtxt is for floating point content, so change it to be able to load mixed data.
                        mdriveseq = np.loadtxt(action_folder+str(mdrive_objects[mdriveselnum][2]), dtype=np.object)
                        print ("drive motor activity sequence loaded")
                    else:
                        lcddisp("*FILE ERROR*", "*NO action file*", 0.1)
                        print ("action file " + str(step_options[stepselnum][2]) + " NOT found")
                        webwarning = "FILE ERROR: drive motor object "+str(mdriveselnum)+" - "+str(mdrive_objects[mdriveselnum][0])+" - file not found"
                        mdriveselnum = 0
                else:
                    mdriveselnum = 0
                    webwarning = "WARNING: selected drive motor object# is out of range"

            elif mdrive_option == 'mdrive_run' and mdrivestop != 'yes':
                print (" - *** in mdrive_option: run")
                mdrive_option_last = 'mdrive_run'
                webwarning = "RUNNING: motor drive object " + str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])
                # check that a valid motor drive object has been chosen before trying to 'run'
                if mdriveselnum >0 and mdriveselnum <= mdrive_number:
                    lcddisp("mdrive running", str(mdrive_objects[mdriveselnum][0]), 0.1)
                    while mdrive_option == 'mdrive_run' and mdrivestop != 'yes':
                        for row in range (1, int(len(mdriveseq))):    
                            print (" processing activity sequence row " + str(row) )
                            # ------------------------------------------------------------------------------------------------------
                            # run the 'drive motor' activities: setting direction, speed and sound from the activity sequence file
                            # ------------------------------------------------------------------------------------------------------

                            # start sound as a background process unless it is set to 'nothing'
                            print (" sound file: " + str(mdriveseq[row][4]) )
                            if str(mdriveseq[row][4]) != "nothing":
                                # play the sound once/repeat depending upon mdriveseq[row][6]
                                # in a new release use the time_ms setting, mdriveseq[row][5], to limit the time the sound is played
                                #   but it will be just set to a dummy value for now
                                play_sound(str(mdriveseq[row][4]), "all", str(mdriveseq[row][6]))
                            else:
                                pass

                            print ("motor#: " + str(mdriveseq[row][0]) )
                            print ("direction: " + str(mdriveseq[row][1]) )
                            print ("speed: " + str(mdriveseq[row][2]) )
                            print ("run time (secs): " + str(mdriveseq[row][3]) )

                            # code to run a drive motor inserted below
                            webwarning = "RUNNING: motor drive object " + str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])

                            if mdrivestop == 'yes':
                                lcddisp("* drive motor *", "actions stopped", 3)
                                Astop_pwm()
                                Bstop_pwm()
                                # stop any sounds that might be playing
                                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                print ("omxplayer killed")
                                webwarning = "STOPPED: motor drive object " + str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])
                                print (str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0]) + " stopped by mdrivestop flag" )
                                print (" **** BREAKING out of for loop ")
                                break   # break out of the main 'for' loop that runs all the actions

                            elif str(mdriveseq[row][1]) == "stop" and str(mdriveseq[row][0]) == "M2":
                                Astop_pwm()
                                # stop any sounds that might be playing
                                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                print ("omxplayer killed")
                                lcddisp("** M2 motor **", "stop " + str((mdriveseq[row][3]) + "s"), 0.1)
                                sleep( int(mdriveseq[row][3]) )
                            elif str(mdriveseq[row][1]) == "stop" and str(mdriveseq[row][0]) == "M1":
                                Bstop_pwm()
                                # stop any sounds that might be playing
                                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                print ("omxplayer killed")
                                lcddisp("** M1 motor **", "stop " + str((mdriveseq[row][3]) + "s"), 0.1)
                                sleep( int(mdriveseq[row][3]) )
                            elif str(mdriveseq[row][3]) == "continuous" and str(mdriveseq[row][1]) == "forwards" and str(mdriveseq[row][0]) == "M2":
                                Aforward_pwm( int(mdriveseq[row][2]) )
                                lcddisp("** M2 motor **", "fwd continuous", 0.1)
                            elif str(mdriveseq[row][3]) == "continuous" and str(mdriveseq[row][1]) == "forwards" and str(mdriveseq[row][0]) == "M1":
                                Bforward_pwm( int(mdriveseq[row][2]) )
                                lcddisp("** M1 motor **", "fwd continuous", 0.1)
                            elif str(mdriveseq[row][3]) == "continuous" and str(mdriveseq[row][1]) == "backwards" and str(mdriveseq[row][0]) == "M2":
                                Abackward_pwm( int(mdriveseq[row][2]) )
                                lcddisp("** M2 motor **", "back continuous", 0.1)
                            elif str(mdriveseq[row][3]) == "continuous" and str(mdriveseq[row][1]) == "backwards" and str(mdriveseq[row][0]) == "M1":
                                Bbackward_pwm( int(mdriveseq[row][2]) )
                                lcddisp("** M1 motor **", "back continuous", 0.1)

                            elif str(mdriveseq[row][3]) != "continuous" and str(mdriveseq[row][1]) == "forwards" and str(mdriveseq[row][0]) == "M2":
                                lcddisp("** M2 motor **", "fwd " + str((mdriveseq[row][3]) + "s"), 0.1)
                                Aforward_pwm( int(mdriveseq[row][2]) )
                                sleep( int(mdriveseq[row][3]) )
                                Astop_pwm()

                            elif str(mdriveseq[row][3]) != "continuous" and str(mdriveseq[row][1]) == "forwards" and str(mdriveseq[row][0]) == "M1":
                                lcddisp("** M1 motor **", "fwd " + str((mdriveseq[row][3]) + "s"), 0.1)
                                Bforward_pwm( int(mdriveseq[row][2]) )
                                sleep( int(mdriveseq[row][3]) )
                                Bstop_pwm()

                            elif str(mdriveseq[row][3]) != "continuous" and str(mdriveseq[row][1]) == "backwards" and str(mdriveseq[row][0]) == "M2":
                                lcddisp("** M2 motor **", "back " + str((mdriveseq[row][3]) + "s"), 0.1)
                                Abackward_pwm( int(mdriveseq[row][2]) )
                                sleep( int(mdriveseq[row][3]) )
                                Astop_pwm()
                                # stop any sounds that might be playing
                                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                print ("omxplayer killed")

                            elif str(mdriveseq[row][3]) != "continuous" and str(mdriveseq[row][1]) == "backwards" and str(mdriveseq[row][0]) == "M1":
                                lcddisp("** M1 motor **", "back " + str((mdriveseq[row][3]) + "s"), 0.1)
                                Bbackward_pwm( int(mdriveseq[row][2]) )
                                sleep( int(mdriveseq[row][3]) )
                                Bstop_pwm()
                                # stop any sounds that might be playing
                                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                                print ("omxplayer killed")

                            else:
                                lcddisp("* drive motor *", "action " +str(row) + " not OK", 3)

                        # if here then the for loop has ended or has been stopped and a break executed
                        #  so check what the last command was and reset the conditions appropriately
                        print (" mdrive_option and mdrivestop values: " + str(mdrive_option) + " - " + str(mdrivestop) )
                        if mdrive_option == 'mdrive_run' and mdrivestop != 'yes':
                            print ("for loop ended - but while loop continues: no stop received")
                            mdrivestop = 'no'
                        elif mdrivestop == 'yes':
                            #  while loop continues but wait for another run command to go elsewhere
                            print ("for loop ended")
                            mdrive_option = 'mdrive_choose'  # go to here when the while loop  'breaks'
                            mdrivestop = 'no'

                    print ("while loop ended")

                else:
                    webwarning = "WARNING: drive motor object# NOT selected "

            elif mdrive_option == 'mdrive_stop':
                print (" - *** in mdrive_option: stop")
                mdrivestop = 'yes'
                webwarning = "STOPPED: motor drive object " + str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])
                mdrive_option_last = 'mdrive_stop'
                # Set both motors to stop just in case
                Astop_pwm()
                Bstop_pwm()

                # stop any sounds that might be playing
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")
                lcddisp("mdrive stopped", str(mdrive_objects[mdriveselnum][0]), 0.1)

            else:   # if here then an unknown mdrive command has been passed from the browser
                template_data = {
                    'title' : "mechatronic: main options selection",
                    'description' : "mechatronic: Raspberry Pi powered stepper and servo motor controller",
                    'build' : hardware,

                }
                return render_template('select_mode.html', **template_data)


            template_data = {
                'title' : "mechatronic: drive motor operation",
                'description' : "mechatronic: drive motor controller options",
                'mdriveobjs' : mdrive_number,
                'selmdriveobj' : mdriveselnum,
                'warnweb' : webwarning,
                'build' : hardware

            }
            return render_template('mdrive_options.html', **template_data, mdrive_objects = mdrive_objects)


        #################################################################################
        # this route provides custom mechatronic selection when /custom_mech is selected
        #################################################################################
        @mechatronic_app01.route("/custom/<custom_option>") # run the code below this function when /custom/<custom_option> is accessed where custom_option is a variable
        def custmech(custom_option=None):
            global cust_number
            global cust_objects
            global custselnum
            global semaphore_servo_data
            global semaphore_stop
            global message_read
            global message
            global mdrivestop

            if custom_option == 'custom_list':
                print (" - in custom_option: list")
                # display the web control select text on the LCD
                print ("displaying the web control select text")
                mylcd.lcd_clear()
                mylcd.lcd_display_string("mechatronics    ..", 1, 0) # display at row 1 column 1
                mylcd.lcd_display_string("custom options: ", 2, 0) # display at row 2 column 1

                custselnum = 0
                webwarning = "" 
                page_title = "custom mechatronic object list"

                template_data = {
                    'title' : page_title,
                    'description' : "Raspberry Pi powered custom build options",
                    'warnweb' : webwarning,
                    'custselobj' : str(custselnum),
                    'custobjs' : cust_number,
                    'sem_message' : message,

                }
                return render_template('custom_mech.html', **template_data, cust_objects = cust_objects)

            elif custom_option == 'custom1':
                print (" - in custom_option: custom1 - semaphore")
                semaphore_stop ="no"
                webwarning = "" 
                custselnum = 1
                page_title = "semaphore messaging"

                # ---------------------------------------------------------------
                # use message text read from file
                if message_read != "yes":
                    message = readmessage("/home/pi/RPi_maker_kit5/mechatronics/action_sequences01/semaphore_message.txt")
                    print ("message read from file: " + message)
                    message_read = "yes"

                template_data = {
                    'title' : page_title,
                    'description' : "Raspberry Pi powered semaphore flagging demonstration",
                    'warnweb' : webwarning,
                    'custselobj' : str(custselnum),
                    'custobjs' : cust_number,
                    'sem_message' : message,

                }
                return render_template('semaphore01.html', **template_data, cust_objects = cust_objects)


            elif custom_option == 'custom1_update':
                print (" - in custom_option: custom1 - semaphore message update")
                semaphore_stop ="no"
                webwarning = "MESSAGE: updated" 
                custselnum = 1
                page_title = "semaphore messaging"

                message = request.args.get('msgsem')  # updated message from browser

                template_data = {
                    'title' : page_title,
                    'description' : "Raspberry Pi powered semaphore flagging demonstration",
                    'warnweb' : webwarning,
                    'custselobj' : str(custselnum),
                    'custobjs' : cust_number,
                    'sem_message' : message,

                }
                return render_template('semaphore01.html', **template_data, cust_objects = cust_objects)


            elif custom_option == 'custom1_send':
                print (" - in custom_option: custom1 - semaphore message send")
                semaphore_stop ="no"
                webwarning = "MESSAGE: sent" 
                custselnum = 1
                page_title = "semaphore messaging"

                semaphore_flagging(message) # send message

                print ("message ended")
                mylcd.lcd_clear()
                mylcd.lcd_display_string(message, 1, 1)    # display at row 1 column 1
                mylcd.lcd_display_string("message ended", 2, 1)   # display at row 2 column 1
                sleep(2)  # short pause to make sure the display above is 'seen'

                # set servos to zero position
                semaphore_zero()

                template_data = {
                    'title' : page_title,
                    'description' : "Raspberry Pi powered semaphore flagging demonstration",
                    'warnweb' : webwarning,
                    'custselobj' : str(custselnum),
                    'custobjs' : cust_number,
                    'sem_message' : message,

                }
                return render_template('semaphore01.html', **template_data, cust_objects = cust_objects)


            elif custom_option == 'custom1_stop':
                print (" - in custom_option: custom1 - semaphore message stopped")
                semaphore_stop ="yes"
                webwarning = "MESSAGE: stopped" 
                custselnum = 1
                page_title = "semaphore messaging"

                print ("message ended")
                mylcd.lcd_clear()
                mylcd.lcd_display_string(message, 1, 1)    # display at row 1 column 1
                mylcd.lcd_display_string("message ended", 2, 1)   # display at row 2 column 1
                sleep(2)  # short pause to make sure the display above is 'seen'

                # set servos to zero position
                semaphore_zero()

                template_data = {
                    'title' : page_title,
                    'description' : "Raspberry Pi powered semaphore flagging demonstration",
                    'warnweb' : webwarning,
                    'custselobj' : str(custselnum),
                    'custobjs' : cust_number,
                    'sem_message' : message,

                }
                return render_template('semaphore01.html', **template_data, cust_objects = cust_objects)


            elif custom_option == 'custom2':
                print (" - in custom_option: custom2 - robot arm")
                robotarm_stop ="no"
                webwarning = "Sorry: this custom mechatronic object is still being developed" 
                custselnum = 1
                page_title = "robot arm"

                template_data = {
                    'title' : page_title,
                    'description' : "Raspberry Pi powered XYZ robot arm with a gripper head",
                    'warnweb' : webwarning,
                    'custselobj' : str(custselnum),
                    'custobjs' : cust_number,

                }
                return render_template('robot_arm01.html', **template_data, cust_objects = cust_objects)


            elif custom_option == 'sem_stop':
                print (" - in custom_option: sem_stop")
                semaphore_stop ="yes"
                webwarning = "" 

                template_data = {
                    'title' : page_title,
                    'description' : "Raspberry Pi powered stepper and servo motor controller",
                    'warnweb' : webwarning,
                    'custselobj' : str(custselnum),
                    'custobjs' : cust_number,

                }
                return render_template('custom_mech.html', **template_data, cust_objects = cust_objects)


        #################################################################################
        # this route displays various system stats when /system_stats is selected
        #################################################################################
        @mechatronic_app01.route("/system_stats") # run the code below this function when /system_stats is accessed
        def sysstat():
            global stepseq
            global stepselnum
            global stepstop
            global audio_out
            global hardware
            global version
            global object_number
            global sopt_number
            global mdrive_number
            global cust_number
            global mdrivestop

            # display the web control select text on the LCD
            print ("displaying the web control select text")
            mylcd.lcd_clear()
            mylcd.lcd_display_string("mechatronics    ..", 1, 0) # display at row 1 column 1
            mylcd.lcd_display_string("system stats: ", 2, 0) # display at row 2 column 1
            wifimac = getMAC("wlan0")
            CPU_temp = getCPUtemperature()
            print ("CPU temperature  : " + str(CPU_temp) )
            print (" start route " )

            ipaddress = getIP()
            host = os.uname()[1]
            if audio_out == "local":
                audiobox = "local socket"
            elif audio_out == "hdmi":
                audiobox = "HDMI cable"
            else:
                audiobox = "undefined"
            template_data = {
                'title' : "system stats",
                'description' : "Raspberry Pi powered stepper and servo motor controller",
                'boxhost' : host,
                'boxIP' : ipaddress,
                'swversion' : version, 
                'build' : hardware,
                'boxaudio' : audiobox,
                'servoobjs' : object_number,
                'stepperobjs' : sopt_number,
                'mdriveobjs' : mdrive_number,
                'macwifi' : wifimac,
                'custobjs' : cust_number,
                'cputemp' : CPU_temp,

            }
            return render_template('system_stats.html', **template_data)



        ###################################################################################
        # this route displays various maintenance activities when /maintenance is selected
        ###################################################################################
        @mechatronic_app01.route("/maintenance/<maintain_option>", methods = ['POST', 'GET']) # run the code below this function when /maintenance/<maintain_option> is accessed where maintain_option is a variable - allowing both POST and GET HTTP methods
        def maintain(maintain_option=None):

            global stepseq
            global stepselnum
            global stepactlen
            global stepactsel
            global stepstop
            global step_options
            global sopt_number

            global servoselnum
            global an_objects
            global object_number
            global obseq
            global servoactlen
            global servoactsel
            global servo_channels
            global servochanrows

            global mdriveselnum
            global mdrive_objects
            global mdrive_number
            global mdriveseq
            global mdriveactlen
            global mdriveactsel
            global mdrivestop

            global soundfiles
            global soundfile_sel
            global soundfiles_num
            global soundfolder_read
            global audio_out

            global hardware

            # display the maintenance select text on the LCD
            print ("displaying the maintenance select text")
            lcddisp("mechatronic web..", "maintenance: ", 1)

            if maintain_option == 'maintain_list':
                print (" - in maintain_option: maintain_list")
                # display the web control select text on the LCD
                print ("displaying the web control select text")
                lcddisp("maintenance......", "option list......", 1)

                servoselnum = 0
                stepselnum = 0
                webwarning = "" 
                page_title = "mechatronic: maintenance options "

            # --------------------------------------------------------------------------------------

            elif maintain_option == 'object_type_choose':
                print (" - in maintain_option: object_type_choose")
                # display the object type selection text on the LCD
                print ("displaying the object type selection text")
                lcddisp("obj management", "type choose", 1)

                webwarning = "" 
                page_title = "mechatronic: object type selection"

                template_data = {
                    'title' : "mechatronic: object type selection",
                    'description' : "mechatronic: maintenance - object management: type selection",
                    'warnweb' : webwarning,
                    'build' : hardware,

                }
                return render_template('obj_type_choose.html', **template_data)

            # --------------------------------------------------------------------------------------

            elif maintain_option == 'object_type_stepper':
                print (" - in maintain_option: object_type_stepper")
                # display the stepper object management text on the LCD
                print ("displaying the stepper object management text")
                lcddisp("obj management", "stepper objects", 1)

                webwarning = "" 
                page_title = "mechatronic: stepper object management"
                stepactsel = 0
                stepselnum = 0
                stepactlen = 0
                stepcopy_objects = step_obj_transform()  # use a local copy of step_options with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: stepper object management",
                    'description' : "mechatronic: maintenance - stepper object management",
                    'warnweb' : webwarning,
                    'selstepobj' : stepselnum,
                    'selstepact' : stepactsel,
                    'lenstepact' : stepactlen,
                    'stepperobjs' : sopt_number,
                    'build' : hardware,

                }
                return render_template('obj_type_stepper.html', **template_data, stepcopy_objects = stepcopy_objects)


            elif maintain_option[0:16] == 'obj_stepper_edit':
                print (" - in maintain_option: obj_stepper_edit")
                stepselnum = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the stepper object# from the passed URL
                stepseq = np.loadtxt(action_folder+str(step_options[stepselnum][2]), dtype=np.object)

                print ("stepper activity sequence loaded: array length " +str(len(stepseq)) + " - array shape " + str(np.shape(stepseq)) )
                # need to check if this is a 'new' sequence file with just a dummy first action line'
                #  and if so set the length etc  

                if stepseq[0][0] == "newstep": 
                    # a new action file !
                    stepactlen = 1
                else:
                    stepactlen = len(stepseq)
                print ("number of step actions: " + str(stepactlen-1) )
                #print (stepseq)

                # display the stepper object edit text on the LCD
                print ("displaying the stepper object edit text")
                lcddisp("stepper objects", "editing #" +str(stepselnum), 1)

                webwarning = "EDITING: stepper object " +str(stepselnum) + " - " + str(step_options[stepselnum][0])
                stepactsel = 0

                stepcopy_objects = step_obj_transform()  # use a local copy of step_options with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: stepper object edit",
                    'description' : "mechatronic: maintenance - stepper object management",
                    'warnweb' : webwarning,
                    'stepperobjs' : sopt_number,
                    'selstepobj' : stepselnum,
                    'selstepact' : stepactsel,
                    'lenstepact' : stepactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_stepper.html', **template_data, stepcopy_objects = stepcopy_objects, stepseq = stepseq)


            elif maintain_option == 'obj_stepper_new':
                print (" - in maintain_option: obj_stepper_new")
                print ("step_options at obj_stepper_new")
                print (step_options)

                # increase the number of stepper objects by 1
                sopt_number = sopt_number + 1

                # create the new 'step_options' data row in the master file
                new_object_name =  request.args.get('newobjname')  # object name
                new_object_number =  str(sopt_number)              # object number
                new_seqfile =  request.args.get('newseqfile')          # sequence file
                # convert any spaces in the new sequence file field to underscores and check it ends with .txt
                new_seqfile =  new_seqfile.replace(" ", "_")
                if new_seqfile[-4][-1] != ".txt":
                    new_seqfile = new_seqfile + ".txt"
                    print (" .txt added to new sequence file name ")
                new_object_desc =  request.args.get('newobjdesc')  # object description
                if len(new_object_desc) == 0:
                    new_object_desc = "---"
                # convert any spaces in the new name and description fields to underscores
                new_object_name = new_object_name.replace(" ", "_")
                #print ("new_object_name = " + new_object_name)
                #print ("new_object_number = " + new_object_number)
                new_object_desc = new_object_desc.replace(" ", "_")
                #print ("new_object_desc = " + new_object_desc)
                #print ("new_seqfile = " + new_seqfile)
                new_row = np.array([new_object_name, new_object_number, new_seqfile, new_object_desc])
                #print (new_row)
                # add the new row directly to the step_options master
                #print ("step_options before adding new row:")
                #print (step_options)

                temparray = np.vstack( (step_options, new_row) )

                #print ("temparray after new row")
                #print (temparray)

                step_options = temparray
                print ("step_options after new row")
                print (step_options)

                # resave the master objects numpy array as a file with the extended step_options content
                np.savetxt(str(stepper_options_file), step_options, fmt="%s", delimiter="  ")

                # initialise a new sequence numpy 2D array  and store as a file
                #  the first value of the first line is set to 'newstep' to signify 
                #  that this a new file without any set actions
                # the second line is actually set with some dummy values 
                #  just so that the the numpy array is created as 2D
                new_seq_content = np.array([("newstep", "direction", "speed", "sound_file_name", "time_ms", "play"), 
                                            ("1", "clock", "full", "nothing", "all", "repeat")])
                print ("new seq file length: " + str(len(new_seq_content)) )
                print ("new seq file shape: " + str(np.shape(new_seq_content)) )
                # now save the 2D numpy array as a .txt file with spaces as the element delimiter
                np.savetxt(action_folder+str(step_options[sopt_number][2]), new_seq_content, fmt="%s", delimiter="  ")

                # display the stepper object edit text on the LCD
                print ("displaying the stepper object edit text")
                lcddisp("new stepper obj", str(step_options[sopt_number][0]), 1)

                webwarning = "CREATED NEW: stepper object " +str(sopt_number) + " - " + str(step_options[sopt_number][0])
                stepactsel = 0
                stepselnum = 0
                stepactlen = 0
                # create the local copy of the updated step_options array
                stepcopy_objects = step_obj_transform()  # use a local copy of step_options with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: new stepper object",
                    'description' : "mechatronic: maintenance - stepper object management",
                    'warnweb' : webwarning,
                    'stepperobjs' : sopt_number,
                    'selstepobj' : stepselnum,
                    'selstepact' : stepactsel,
                    'lenstepact' : stepactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_stepper.html', **template_data, stepcopy_objects = stepcopy_objects )


            elif maintain_option == 'obj_stepper_clone':
                print (" - in maintain_option: obj_stepper_clone")

                # increase the number of stepper objects by 1
                sopt_number = sopt_number + 1

                # create the new 'step_options' data row in the master file
                clone_object_name =  request.args.get('cloneobjname')   # object name
                clone_object_number =  request.args.get('cloneobjnum')  # object number
                clone_seqfile =  request.args.get('cloneseqfile')        # sequence file
                # convert any spaces in the new clone sequence file field to underscores and check it ends with .txt
                clone_seqfile =  clone_seqfile.replace(" ", "_")
                if clone_seqfile[-4][-1] != ".txt":
                    clone_seqfile = clone_seqfile + ".txt"
                    print (" .txt added to clone sequence file name ")
                clone_object_desc =  request.args.get('cloneobjdesc')  # object description
                if len(clone_object_desc) == 0:
                    clone_object_desc = "---"
                # convert any spaces in the clone name and description fields to underscores
                clone_object_name = clone_object_name.replace(" ", "_")
                #print ("clone_object_name = " + clone_object_name)
                #print ("clone_object_number = " + clone_object_number)
                clone_object_desc = clone_object_desc.replace(" ", "_")
                #print ("clone_object_desc = " + clone_object_desc)
                #print ("clone_seqfile = " + clone_seqfile)
                new_row = np.array([clone_object_name, clone_object_number, clone_seqfile, clone_object_desc])
                #print (new_row)
                # add the new row directly to the step_options master
                #print ("step_options before adding new row:")
                #print (step_options)

                temparray = np.vstack( (step_options, new_row) )

                #print ("temparray after new row")
                #print (temparray)

                step_options = temparray
                #print ("step_options after new row")
                #print (step_options)

                # resave the master objects file with the extended step_options content
                np.savetxt(str(stepper_options_file), step_options, fmt="%s", delimiter="  ")

                # create the new sequence file from the file to be cloned
                os.system("sudo cp " + action_folder+str(step_options[int(clone_object_number)][2]) + " " + action_folder+str(step_options[sopt_number][2]) )

                # display the stepper object clone text on the LCD
                print ("displaying the stepper object clone text")
                lcddisp("new object #"+str(sopt_number), "cloning #"+str(clone_object_number), 1)

                webwarning = "CLONED: stepper object " +str(sopt_number) + " created from: " + str(step_options[int(clone_object_number)][0])
                stepactsel = 0
                stepselnum = 0
                stepactlen = 0
                stepcopy_objects = step_obj_transform()  # use a local copy of step_options with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: stepper object cloning",
                    'description' : "mechatronic: maintenance - stepper object management",
                    'warnweb' : webwarning,
                    'stepperobjs' : sopt_number,
                    'selstepobj' : stepselnum,
                    'selstepact' : stepactsel,
                    'lenstepact' : stepactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_stepper.html', **template_data, stepcopy_objects = stepcopy_objects)


            elif maintain_option[0:23] == 'obj_stepper_action_edit':
                print (" - in maintain_option: obj_stepper_action_edit")
                stepactsel = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the stepper object# from the passed URL

                # display the stepper object edit text on the LCD
                print ("displaying the stepper object edit text")
                lcddisp("step object #"+str(stepselnum), "**action #" +str(stepactsel), 1)

                webwarning = "EDITING: stepper object " +str(stepselnum) + " - " + str(step_options[stepselnum][0])+ " / action " +str(stepactsel)
                stepcopy_objects = step_obj_transform()  # use a local copy of step_options with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: stepper object action edit",
                    'description' : "mechatronic: maintenance - stepper object management",
                    'warnweb' : webwarning,
                    'stepperobjs' : sopt_number,
                    'selstepobj' : stepselnum,
                    'selstepact' : stepactsel,
                    'lenstepact' : stepactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_stepper.html', **template_data, stepcopy_objects = stepcopy_objects, stepseq = stepseq)


            elif maintain_option == 'obj_stepper_action_update':
                print (" - in maintain_option: obj_stepper_action_update")

                # display the stepper object edit text on the LCD
                print ("displaying the stepper object action update text")
                lcddisp("step object #"+str(stepselnum), "action#" +str(stepactsel) + " updated", 1)

                webwarning = "UPDATED: stepper object " +str(stepselnum) + " - " + str(step_options[stepselnum][0])+ " / action " +str(stepactsel)

                ## update the action line from the URL responses and resave the file
                for i in range(0, 6):
                    # do some field content validation here at some point
                    stepseq[int(stepactsel)][i] = request.args.get('field'+str(i))  # updated message from browser
                    if i == 3:
                        stepseq[stepactsel][i] =  stepseq[stepactsel][i].replace(" ", "_")
                # now check that this was not the first action line to be set
                print ("stepseq[0][0]: " +str(stepseq[0][0]) )
                if str(stepseq[0][0]) == "newstep": 
                    # a new action file - so reset the [0][0] value
                    stepseq[0][0] = "step"     
             
                # resave the complete action file
                np.savetxt(action_folder+str(step_options[stepselnum][2]), stepseq, fmt="%s", delimiter="  ")
                print ("selected stepper object action file resaved")

                stepcopy_objects = step_obj_transform()  # use a local copy of the step_options with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: stepper object action update",
                    'description' : "mechatronic: maintenance - stepper object management",
                    'warnweb' : webwarning,
                    'stepperobjs' : sopt_number,
                    'selstepobj' : stepselnum,
                    'selstepact' : stepactsel,
                    'lenstepact' : stepactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_stepper.html', **template_data, stepcopy_objects = stepcopy_objects, stepseq = stepseq)


            elif maintain_option == 'obj_stepper_action_create':
                print (" - in maintain_option: obj_stepper_action_create")

                stepactsel = stepactlen
                print ("stepactsel: " + str(stepactsel))
                stepactlen = stepactlen + 1
                print ("stepactlen: " + str(stepactlen))

                # display the stepper object edit text on the LCD
                print ("displaying the stepper object action create text")
                lcddisp("step object #"+str(stepselnum), "action" +str(stepactsel) + " created", 1)

                webwarning = "CREATED: stepper object " +str(stepselnum) + " - " + str(step_options[stepselnum][0])+ " / action " +str(stepactsel)

                ## create the action line from the URL responses and resave the file
                for i in range(0, 6):
                    # do some field content validation here at some point
                    print ("i: " + str(i) )
                    print ("fieldi value: " + str(request.args.get('field'+str(i))) )
                    stepseq[int(stepactsel)][i] = request.args.get('field'+str(i))  # updated message from browser
                    if i == 3:
                        stepseq[stepactsel][i] =  stepseq[stepactsel][i].replace(" ", "_")
                # now check that this was not the first action line to be set
                print ("stepseq[0][0]: " +str(stepseq[0][0]) )
                if str(stepseq[0][0]) == "newstep": 
                    # a new action file - so reset the [0][0] value
                    stepseq[0][0] = "step"

                # resave the complete action file
                np.savetxt(action_folder+str(step_options[stepselnum][2]), stepseq, fmt="%s", delimiter="  ")
                print ("selected stepper object action file resaved")

                stepcopy_objects = step_obj_transform()  # use a local copy of the step_options with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: stepper object action create",
                    'description' : "mechatronic: maintenance - stepper object management",
                    'warnweb' : webwarning,
                    'stepperobjs' : sopt_number,
                    'selstepobj' : stepselnum,
                    'selstepact' : stepactsel,
                    'lenstepact' : stepactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_stepper.html', **template_data, stepcopy_objects = stepcopy_objects, stepseq = stepseq)


            elif maintain_option[0:23] == 'obj_stepper_action_test':
                print (" - in maintain_option: obj_stepper_action_test")
                #print ("step_options at obj_stepper_action_test")
                #print (step_options)

                stepacttest = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the step object# from the passed URL
                stepactsel = stepacttest

                # display the stepper object testing text on the LCD
                print ("displaying the stepper object testing text")
                lcddisp("stepper obj#"+str(stepselnum), "testing action#" +str(stepacttest), 1)

                webwarning = "TESTED: stepper object " +str(stepselnum) + " - " + str(step_options[stepselnum][0])+ " / action " +str(stepacttest)

                ## test the action line selected from the URL response

                # kill any previous audio that might be playing 
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")

                print (" processing activity sequence row " + str(stepacttest) )
                # -----------------------------------------------------------------------
                # run the 'stepper motor' activities defined by the activity sequence file
                # -----------------------------------------------------------------------
                # check sound file is needed before trying to play it
                if str(stepseq[stepacttest][3]) != "nothing":
                    if os.path.isfile(sound_folder+str(stepseq[stepacttest][3])):
                        lcddisp("step move ON", "sound file OK", 1)
                        print ("sound file " + str(stepseq[stepacttest][3]) + " found OK")
                        mylcd.lcd_display_string(str(step_options[stepselnum][0]), 2, 0) # display at stepacttest 2 column 0
                        play_sound(str(stepseq[stepacttest][3]), "all", "once") # start action value 1 sound as a background process

                    else:
                        lcddisp("*SYSTEM ERROR*", "NO sound file", 3)
                        print ("sound file " + str(stepseq[stepacttest][3]) + " NOT found")
                        webwarning = "ERROR: no sound file found for action " + str(stepacttest)

                print ("direction: " + str(stepseq[stepacttest][1]) )
                print ("speed: " + str(stepseq[stepacttest][2]) )
                if stepseq[stepacttest][1] == "clock":
                    StepDir = 1
                else:
                    StepDir = -1

                StepCounter = 0
                if StepDir == -1:
                    StepCounter = 7

                if stepseq[stepacttest][2] == "full":
                    WaitTime = FullTime
                else:
                    WaitTime = HalfTime

                stepstop = "no"
                stepper_drive(StepCounter, StepDir, WaitTime)

                lcddisp("step object #"+str(stepselnum), "action#" + str(stepacttest) + " tested!", 1)
                stepstop = "yes"

                # 'just in case' stop the audio from playing so that any subsequent tests get a 'clean' start for any sounds
                player = subprocess.Popen(["omxplayer", "q" ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                stepcopy_objects = step_obj_transform()  # use a local copy of the step_options with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: step object action test",
                    'description' : "mechatronic: maintenance - step object management",
                    'warnweb' : webwarning,
                    'stepperobjs' : sopt_number,
                    'selstepobj' : stepselnum,
                    'selstepact' : stepactsel,
                    'lenstepact' : stepactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_stepper.html', **template_data, stepcopy_objects = stepcopy_objects, stepseq = stepseq)


            elif maintain_option == 'obj_stepper_action_stoptest':
                print (" - in maintain_option: obj_stepper_action_stoptest")
                #print ("step_options at obj_stepper_action_stoptest")
                #print (step_options)
                stepstop = "yes"

                webwarning = "TEST STOPPED: stepper object " +str(stepselnum) + " - " + str(step_options[stepselnum][0])+ " / action " +str(stepactsel)
                lcddisp("step object #"+str(stepselnum), "#" + str(stepactsel) + " test stopped", 1)
                # 'just in case' stop the audio from playing so that any subsequent tests get a 'clean' start for any sounds
                player = subprocess.Popen(["omxplayer", "q" ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                stepcopy_objects = step_obj_transform()  # use a local copy of the step_options with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: step object action test",
                    'description' : "mechatronic: maintenance - step object management",
                    'warnweb' : webwarning,
                    'stepperobjs' : sopt_number,
                    'selstepobj' : stepselnum,
                    'selstepact' : stepactsel,
                    'lenstepact' : stepactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_stepper.html', **template_data, stepcopy_objects = stepcopy_objects, stepseq = stepseq)


            # --------------------------------------------------------------------------------------

            elif maintain_option == 'object_type_servo':
                print (" - in maintain_option: object_type_servo")
                #print ("an_objects at object_type_servo")
                #print (an_objects)

                # display the servo object management text on the LCD
                print ("displaying the servo object management text")
                lcddisp("obj management", "servo objects", 1)

                webwarning = "" 
                page_title = "mechatronic: servo object management"
                servoselnum = 0    # normal selected servo object number
                servoactsel = 0
                servoactlen = 0
                servocopy_objects = servo_obj_transform()  # use a local copy of an_objects with underscores removed from description field
                #print ("an_objects at object_type_servo after local copy created")
                #print (an_objects)
                template_data = {
                    'title' : "mechatronic: servo object management",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels)


            elif maintain_option[0:14] == 'obj_servo_edit':
                print (" - in maintain_option: obj_servo_edit")
                #print ("an_objects at obj_servo_edit")
                #print (an_objects)

                servoselnum = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the servo object# from the passed URL
                obseq = np.loadtxt(action_folder+str(an_objects[servoselnum][2]), dtype=np.object)
                print ("servo activity sequence loaded: array length " +str(len(obseq)) + " - array shape " + str(np.shape(obseq)) )

                # need to check if this is a 'new' sequence file with just a dummy first action line'
                #  and if so set the length etc  

                if obseq[0][0] == "newservo": 
                    # a new action file !
                    servoactlen = 1
                else:
                    servoactlen = len(obseq)
                print ("number of servo actions: " + str(servoactlen-1) )
                #print (obseq)

                # display the servo object edit text on the LCD
                print ("displaying the servo object edit text")
                lcddisp("servo objects", "editing #" +str(servoselnum), 1)

                webwarning = "EDITING: servo object " +str(servoselnum) + " - " + str(an_objects[servoselnum][0])
                servoactsel = 0
                servocopy_objects = servo_obj_transform()  # use a local copy of an_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: servo object management",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels, obseq = obseq)


            elif maintain_option == 'obj_servo_new':
                print (" - in maintain_option: obj_servo_new")
                #print ("an_objects at obj_servo_new")
                #print (an_objects)

                servocopy_objects = servo_obj_transform()  # use a local copy of an_objects with underscores removed from description field
                # increase the number of servo objects by 1
                object_number = object_number + 1

                # create the new 'an_objects' data row
                new_object_name =  request.args.get('newobjname')  # object name
                new_button_number =  str(object_number)            # button number
                newseqfile =  request.args.get('seqfile')          # sequence file
                # convert any spaces in the new sequence file field to underscores and check it ends with .txt
                newseqfile =  newseqfile.replace(" ", "_")
                if newseqfile[-4][-1] != ".txt":
                    newseqfile = newseqfile + ".txt"
                    print (" .txt added to new sequence file name ")
                new_object_desc =  request.args.get('newobjdesc')  # object description
                if len(new_object_desc) == 0:
                    new_object_desc = "---"
                # convert any spaces in the new name and description fields to underscores
                new_object_name = new_object_name.replace(" ", "_")
                #print ("new_object_name = " + new_object_name)
                #print ("new_button_number = " + new_button_number)
                new_object_desc = new_object_desc.replace(" ", "_")
                #print ("new_object_desc = " + new_object_desc)
                #print ("newseqfile = " + newseqfile)
                new_row = np.array([new_object_name, new_button_number, newseqfile, new_object_desc])
                #print (new_row)
                # add the new row directly to the an_objects master
                #print ("an_objects before adding new row:")
                #print (an_objects)

                temparray = np.vstack( (an_objects, new_row) )

                #print ("temparray after new row")
                #print (temparray)

                an_objects = temparray
                #print ("an_objects after new row")
                #print (an_objects)

                # resave the master objects numpy array as a file with the extended an_objects content
                np.savetxt(str(servo_objects_file), an_objects, fmt="%s", delimiter="  ")

                # initialise a new sequence numpy 2D array and store as a file
                #  the first value of the first line is set to 'newservo' to signify 
                #  that this a new file without any set actions
                # the second line is actually set with some dummy values 
                #  just so that the the numpy array is created as 2D
                new_seq_content = np.array([("newservo", "ref", "move1", "sound1_file_name", "time_ms", "move2", "sound2_file_name", "time_ms", "repeat"), 
                                            ("0", "1", "100", "nothing", "500", "100", "nothing", "500", "1") ])
                print ("new seq file length: " + str(len(new_seq_content)) )
                print ("new seq file shape: " + str(np.shape(new_seq_content)) )

                np.savetxt(action_folder+str(an_objects[object_number][2]), new_seq_content, fmt="%s", delimiter="  ")

                # create a new servo channels 'row' with 'null' values
                servochanrows = servochanrows + 1
                new_servo_channel_row = np.array([new_object_name, "0", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"])
                # add the new row to the servo_channels array
                tempchan = np.vstack( (servo_channels, new_servo_channel_row) )
                servo_channels = tempchan

                # resave the servo channel numpy array in its text file
                np.savetxt(str(servo_channels_file), servo_channels, fmt="%s", delimiter="  ")


                # display the servo object edit text on the LCD
                print ("displaying the servo object edit text")
                lcddisp("new servo object", str(an_objects[object_number][0]), 1)

                webwarning = "EDITING: servo object " +str(servoselnum) + " - " + str(an_objects[servoselnum][0])
                servoactsel = 0
                servoselnum = 0
                servoactlen = 0
                # recreate the local copy of the new an_objects array
                servocopy_objects = servo_obj_transform()  # use a local copy of an_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: servo object management",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels)



            elif maintain_option == 'obj_servo_clone':
                print (" - in maintain_option: obj_servo_clone")

                # increase the number of servo objects by 1
                object_number = object_number + 1

                # create the new 'an_objects' data row in the master file
                clone_object_name =  request.args.get('cloneobjname')   # object name
                clone_object_number =  request.args.get('cloneobjnum')  # object number
                clone_seqfile =  request.args.get('cloneseqfile')        # sequence file
                # convert any spaces in the new clone sequence file field to underscores and check it ends with .txt
                clone_seqfile =  clone_seqfile.replace(" ", "_")
                if clone_seqfile[-4][-1] != ".txt":
                    clone_seqfile = clone_seqfile + ".txt"
                    print (" .txt added to clone sequence file name ")
                clone_object_desc =  request.args.get('cloneobjdesc')  # object description
                if len(clone_object_desc) == 0:
                    clone_object_desc = "---"
                # convert any spaces in the clone name and description fields to underscores
                clone_object_name = clone_object_name.replace(" ", "_")
                #print ("clone_object_name = " + clone_object_name)
                #print ("clone_object_number = " + clone_object_number)
                clone_object_desc = clone_object_desc.replace(" ", "_")
                #print ("clone_object_desc = " + clone_object_desc)
                #print ("clone_seqfile = " + clone_seqfile)
                new_row = np.array([clone_object_name, clone_object_number, clone_seqfile, clone_object_desc])
                #print (new_row)
                # add the new row directly to the an_objects master
                #print ("an_objects before adding new row:")
                #print (an_objects)

                temparray = np.vstack( (an_objects, new_row) )

                #print ("temparray after new row")
                #print (temparray)

                an_objects = temparray
                #print ("an_objects after new row")
                #print (an_objects)

                # resave the master objects file with the extended an_objects content
                np.savetxt(str(servo_objects_file), an_objects, fmt="%s", delimiter="  ")

                # create the new sequence file from the file to be cloned
                os.system("sudo cp " + action_folder+str(an_objects[int(clone_object_number)][2]) + " " + action_folder+str(an_objects[object_number][2]) )

                # create a new servo channels 'row' with 'null' values
                servochanrows = servochanrows + 1
                new_servo_channel_row = np.array([clone_object_name, "0", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"])
                # add the new row to the servo_channels array
                tempchan = np.vstack( (servo_channels, new_servo_channel_row) )
                servo_channels = tempchan

                # resave the servo channel numpy array in its text file
                np.savetxt(str(servo_channels_file), servo_channels, fmt="%s", delimiter="  ")

                # display the servo object clone text on the LCD
                print ("displaying the servo object clone text")
                lcddisp("new object #"+str(object_number), "cloning #"+str(clone_object_number), 1)

                webwarning = "CLONED: servo object " +str(object_number) + " created from: " + str(an_objects[int(clone_object_number)][0])
                servoactsel = 0
                servoselnum = 0
                servoactlen = 0
                servocopy_objects = servo_obj_transform()  # use a local copy of an_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: servo object cloning",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels)



            elif maintain_option == 'obj_servo_channel_create':
                print (" - in maintain_option: obj_servo_channel_create")

                # display the servo object edit text on the LCD
                print ("displaying the servo object edit text")
                lcddisp("servo object #"+str(servoselnum), "channel index", 1)

                webwarning = "CREATE: servo object " +str(servoselnum) + " - new channel index entry - NOT SET UP YET" 
                servocopy_objects = servo_obj_transform()  # use a local copy of an_objects with underscores removed from description field

                #  N.B. new servochanrows not created yet - but code to be added here


                template_data = {
                    'title' : "mechatronic: servo object channel update",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels, obseq = obseq)


            elif maintain_option == 'obj_servo_channel_update':
                print (" - in maintain_option: obj_servo_channel_update")

                # display the servo object edit text on the LCD
                print ("displaying the servo object edit text")
                lcddisp("servo object #"+str(servoselnum), "channel index", 1)

                webwarning = "UPDATE: servo object " +str(servoselnum) + " - new channel index entry - NOT SET UP YET" 
                servocopy_objects = servo_obj_transform()  # use a local copy of an_objects with underscores removed from description field

                #  N.B. servochanrows update not code yet - but code to be added here


                template_data = {
                    'title' : "mechatronic: servo object channel update",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels, obseq = obseq)



            elif maintain_option[0:21] == 'obj_servo_action_edit':
                print (" - in maintain_option: obj_servo_action_edit")
                #print ("an_objects at obj_servo_action_edit")
                #print (an_objects)

                servoactsel = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the servo object# from the passed URL

                # display the servo object edit text on the LCD
                print ("displaying the servo object edit text")
                lcddisp("servo object #"+str(servoselnum), "**action #" +str(servoactsel), 1)

                webwarning = "EDITING: servo object " +str(servoselnum) + " - " + str(an_objects[servoselnum][0])+ " / action " +str(servoactsel)
                servocopy_objects = servo_obj_transform()  # use a local copy of an_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: servo object action update",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels, obseq = obseq)


            elif maintain_option == 'obj_servo_action_update':
                print (" - in maintain_option: obj_servo_action_update")
                #print ("an_objects at obj_servo_action_update")
                #print (an_objects)

                # display the servo object edit text on the LCD
                print ("displaying the servo object action update text")
                lcddisp("servo object #"+str(servoselnum), "action#" +str(servoactsel) + " updated", 1)

                webwarning = "UPDATED: servo object " +str(servoselnum) + " - " + str(an_objects[servoselnum][0])+ " / action " +str(servoactsel)
                servocopy_objects = servo_obj_transform()  # use a local copy of an_objects with underscores removed from description field

                ## update the action line from the URL responses and resave the file
                for i in range(0, 9):
                    # do some field content validation here at some point
                    obseq[servoactsel][i] = request.args.get('field'+str(i))  # updated message from browser
                # now check that this was not the first action line to be set
                print ("obseq[0][0]: " +str(obseq[0][0]) )
                if str(obseq[0][0]) == "newservo": 
                    # a new action file - so reset the [0][0] value
                    obseq[0][0] = "servo" 


                # resave the complete action file
                np.savetxt(action_folder+str(an_objects[servoselnum][2]), obseq, fmt="%s", delimiter="  ")
                print ("selected servo object action file resaved")

                template_data = {
                    'title' : "mechatronic: servo object action update",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels, obseq = obseq)



            elif maintain_option == 'obj_servo_action_create':
                print (" - in maintain_option: obj_servo_action_create")

                servoactsel = servoactlen
                print ("servoactsel: " + str(servoactsel))
                servoactlen = servoactlen + 1
                print ("servoactlen: " + str(servoactlen))

                # display the servo object edit text on the LCD
                print ("displaying the servo object action create text")
                lcddisp("servo object #"+str(servoselnum), "action" +str(servoactsel) + " created", 1)

                webwarning = "CREATED: servo object " +str(servoselnum) + " - " + str(an_objects[servoselnum][0])+ " / action " +str(servoactsel)

                ## create the action line from the URL responses and resave the file
                for i in range(0, 9):
                    # do some field content validation here at some point
                    print ("i: " + str(i) )
                    print ("fieldi value: " + str(request.args.get('field'+str(i))) )
                    obseq[int(servoactsel)][i] = request.args.get('field'+str(i))  # updated message from browser
                    if i == 3 or i == 6:
                        obseq[servoactsel][i] =  obseq[servoactsel][i].replace(" ", "_")
                # now check that this was not the first action line to be set
                print ("obseq[0][0]: " +str(obseq[0][0]) )
                if str(obseq[0][0]) == "newservo": 
                    # a new action file - so reset the [0][0] value
                    obseq[0][0] = "servo"

                # resave the complete action file
                np.savetxt(action_folder+str(an_objects[servoselnum][2]), obseq, fmt="%s", delimiter="  ")
                print ("selected servo object action file resaved")

                servocopy_objects = servo_obj_transform()  # use a local copy of the an_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: servo object action update",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, obseq = obseq)


            elif maintain_option[0:23] == 'obj_servo_action_delete':
                print (" - in maintain_option: obj_servo_action_delete")
                #print ("an_objects at obj_servo_action_delete")
                #print (an_objects)

                servoactdel = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the servo object# from the passed URL

                # display the servo object delete text on the LCD
                print ("displaying the servo object delete text")
                lcddisp("servo object #"+str(servoselnum), "delete action#" +str(servoactdel), 1)

                webwarning = "DELETED: servo object " +str(servoselnum) + " - " + str(an_objects[servoselnum][0])+ " / action " +str(servoactdel)

                ## delete the action line selected from the URL responses and resave the file

                if servoactlen > 2:   # roll back the higher actions if there were more than one originally
                    for i in range (servoactdel, servoactlen-1):
                        for j in range (0,9):
                            obseq[i,j] = obseq[i+1,j]
                    print ("obseq before delete:")
                    print (obseq)
                    obseq = np.delete(obseq, servoactlen-1, axis=0)  # delete the last row
                    print ("obseq after delete:")
                    print (obseq)

                elif servoactlen == 2: # special case when there is just one action left
                    obseq[0][0] = "newservo"    # use the header 1st value to flag this special case
                    for j in range (0,9):
                        obseq[1][j] = "-"       # put dummy values into the first 'action' row so that it is read properly as a 2D array

                print ("last action row deleted - length now: " + str(len(obseq)) )
                servoactlen = servoactlen -1      # and now there is one less action
                print ("servoactlen reduced to: " + str(servoactlen) )

                # resave the complete action file
                np.savetxt(action_folder+str(an_objects[servoselnum][2]), obseq, fmt="%s", delimiter="  ")
                print ("selected servo object action file resaved")

                servocopy_objects = servo_obj_transform()  # use a local copy of the an_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: servo object action delete",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels, obseq = obseq)


            elif maintain_option[0:21] == 'obj_servo_action_test':
                print (" - in maintain_option: obj_servo_action_test")
                #print ("an_objects at obj_servo_action_test")
                #print (an_objects)

                servoacttest = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the servo object# from the passed URL
                servoactsel = servoacttest

                # display the servo object testing text on the LCD
                print ("displaying the servo object testing text")
                lcddisp("servo object #"+str(servoselnum), "testing action#" +str(servoacttest), 1)

                webwarning = "TESTED: servo object " +str(servoselnum) + " - " + str(an_objects[servoselnum][0])+ " / action " +str(servoacttest)

                ## test the action line selected from the URL response

                # kill any previous audio that might be playing 
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")

                print (" processing activity sequence row " + str(servoacttest) )
                # -----------------------------------------------------------------------
                # run the 'servo motor' activities defined by the activity sequence file
                # -----------------------------------------------------------------------
                ### action value 1 ###
                # check sound file is needed before trying to play it
                if str(obseq[servoacttest][3]) != "nothing":
                    if os.path.isfile(sound_folder+str(obseq[servoacttest][3])):
                        lcddisp("servo move ON", "sound file OK", 1)
                        print ("sound file " + str(obseq[servoacttest][3]) + " found OK")
                        mylcd.lcd_display_string(str(an_objects[servoselnum][0]), 2, 0) # display at servoacttest 2 column 0
                        play_sound(str(obseq[servoacttest][3]), "all", "once") # start action value 1 sound as a background process

                    else:
                        lcddisp("*SYSTEM ERROR*", "NO sound file", 3)
                        print ("sound file " + str(obseq[servoacttest][3]) + " NOT found")
                        webwarning = "ERROR: no sound file found for action " + str(servoacttest) + " movement 1"

                # make value 1 servo movement with its associated wait time (or minimum 50ms)
                print (" servo value1: " + str(int(obseq[servoacttest][2])))
                if int(obseq[servoacttest][4]) > 50:
                    picontrol_servo.setServo(filedesc, int(obseq[servoacttest][0]), int(obseq[servoacttest][2]), int(obseq[servoacttest][4]))
                else:
                    picontrol_servo.setServo(filedesc, int(obseq[servoacttest][0]), int(obseq[servoacttest][2]), 50)

                ### action value 2 ###
                # check sound file is needed before trying to play it
                if str(obseq[servoacttest][6]) != "nothing":
                    if os.path.isfile(sound_folder+str(obseq[servoacttest][6])):   # check the sound file is on the system
                        lcddisp("servo move ON", "sound file OK", 1)
                        print ("sound file " + str(obseq[servoacttest][6]) + " found OK")
                        mylcd.lcd_display_string(str(an_objects[servoselnum][0]), 2, 0) # display at servoacttest 2 column 0
                        play_sound(str(obseq[servoacttest][6]), "all", "once")  

                    else:
                        lcddisp("*SYSTEM STOPPED*", "NO sound file", 3)
                        print ("sound file " + str(obseq[servoacttest][6]) + " NOT found")
                        webwarning = "ERROR: no sound file found for action " + str(servoacttest) + " movement 2"

                # make value 2 servo movement with its associated wait time (or minimum 50ms)
                print (" servo value2: " + str(int(obseq[servoacttest][5])))
                if int(obseq[servoacttest][7]) > 50:
                    picontrol_servo.setServo(filedesc, int(obseq[servoacttest][0]), int(obseq[servoacttest][5]), int(obseq[servoacttest][7]))
                else:
                    picontrol_servo.setServo(filedesc, int(obseq[servoacttest][0]), int(obseq[servoacttest][5]), 50)

                lcddisp("servo object #"+str(servoselnum), "action#" + str(servoacttest) + " tested!", 1)

                # 'just in case' stop the audio from playing so that any subsequent tests get a 'clean' start for any sounds
                player = subprocess.Popen(["omxplayer", "q" ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                servocopy_objects = servo_obj_transform()  # use a local copy of the an_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: servo object action test",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels, obseq = obseq)


            elif maintain_option == 'obj_servo_action_addnew':
                print (" - in maintain_option: obj_servo_action_addnew")
                #print ("an_objects at obj_servo_action_addnew")
                #print (an_objects)

                # get the the new action insertion point from the browser returned value
                actinsertnum = int(request.args.get('newactnum'))  # input from browser

                # display the servo object add new action text on the LCD
                print ("displaying the servo object add new action text")
                lcddisp("servo object #"+str(servoselnum), "insert new action#" +str(actinsertnum), 1)

                webwarning = "INSERTED: servo object " +str(servoselnum) + " - " + str(an_objects[servoselnum][0])+ " / new action " +str(actinsertnum)

                ## insert the action line selected from the URL responses and resave the file
                #print ("obseq before insert:")
                #print (obseq)
                servoactlen = servoactlen + 1
                new_action_row = np.array(["-", "-", "-", "-", "-", "-", "-", "-", "-"])
                # add a new row at the end of the actions array
                tempseq = np.vstack( (obseq, new_action_row) )
                obseq = tempseq
                #print ("obseq after new row added at end:")
                #print (obseq)

                # roll forward the existing actions into the new space unless the insertion is at the end in which case it is already done
                if actinsertnum != servoactlen:
                    for i in range (servoactlen-1, actinsertnum-1, -1):
                        #print ("i=" + str(i))
                        for j in range (0,9):
                            obseq[i,j] = obseq[i-1,j]
                    # populate the 'old' actinsertnum row with dummy values to be the new row
                    for j in range (0,9):
                        obseq[actinsertnum,j] = "-"

                #print ("obseq after insertion completion:")
                #print (obseq)

                #print ("new action row inserted - length now: " + str(len(obseq)) )
                #print ("servoactlen increased to: " + str(servoactlen) )

                # resave the complete action file
                np.savetxt(action_folder+str(an_objects[servoselnum][2]), obseq, fmt="%s", delimiter="  ")
                print ("selected servo object action file resaved")

                servocopy_objects = servo_obj_transform()  # use a local copy of the an_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: servo object action update",
                    'description' : "mechatronic: maintenance - servo object management",
                    'warnweb' : webwarning,
                    'servoobjs' : object_number,
                    'selservoobj' : servoselnum,
                    'selservoact' : servoactsel,
                    'lenservoact' : servoactlen,
                    'rowsservochans' : servochanrows,
                    'build' : hardware,

                }
                return render_template('obj_type_servo.html', **template_data, servocopy_objects = servocopy_objects, servo_channels = servo_channels, obseq = obseq)


            # --------------------------------------------------------------------------------------

            elif maintain_option == 'object_type_mdrive':
                print (" - in maintain_option: object_type_mdrive")
                #print ("mdrive_objects at object_type_mdrive")
                #print (mdrive_objects)

                # display the mdrive object management text on the LCD
                print ("displaying the mdrive object management text")
                lcddisp("obj management", "mdrive objects", 1)

                webwarning = "" 
                page_title = "mechatronic: mdrive object management"
                mdriveselnum = 0
                mdriveactsel = 0
                mdriveactlen = 0
                mdrivecopy_objects = mdrive_obj_transform()  # use a local copy of mdrive_objects with underscores removed from description field
                #print ("mdrive_objects at object_type_mdrive after local copy created")
                #print (mdrive_objects)
                template_data = {
                    'title' : "mechatronic: mdrive object management",
                    'description' : "mechatronic: maintenance - mdrive object management",
                    'warnweb' : webwarning,
                    'mdriveobjs' : mdrive_number,
                    'selmdriveobj' : mdriveselnum,
                    'selmdriveact' : mdriveactsel,
                    'lenmdriveact' : mdriveactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_mdrive.html', **template_data, mdrivecopy_objects = mdrivecopy_objects )


            elif maintain_option[0:15] == 'obj_mdrive_edit':
                print (" - in maintain_option: obj_mdrive_edit")
                #print ("mdrive_objects at obj_mdrive_edit")
                #print (mdrive_objects)

                mdriveselnum = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the mdrive object# from the passed URL
                mdriveseq = np.loadtxt(action_folder+str(mdrive_objects[mdriveselnum][2]), dtype=np.object)
                print ("mdrive activity sequence loaded: array length " +str(len(mdriveseq)) + " - array shape " + str(np.shape(mdriveseq)) )

                # need to check if this is a 'new' sequence file with just a dummy first action line'
                #  and if so set the length etc  

                if mdriveseq[0][0] == "newmotor": 
                    # a new action file !
                    mdriveactlen = 1
                else:
                    mdriveactlen = len(mdriveseq)
                print ("number of mdrive actions: " + str(mdriveactlen-1) )
                #print (mdriveseq)

                # display the mdrive object edit text on the LCD
                print ("displaying the mdrive object edit text")
                lcddisp("mdrive objects", "editing #" +str(mdriveselnum), 1)

                webwarning = "EDITING: mdrive object " +str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])
                mdriveactsel = 0
                mdrivecopy_objects = mdrive_obj_transform()  # use a local copy of mdrive_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: mdrive object management",
                    'description' : "mechatronic: maintenance - mdrive object management",
                    'warnweb' : webwarning,
                    'mdriveobjs' : mdrive_number,
                    'selmdriveobj' : mdriveselnum,
                    'selmdriveact' : mdriveactsel,
                    'lenmdriveact' : mdriveactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_mdrive.html', **template_data, mdrivecopy_objects = mdrivecopy_objects, mdriveseq = mdriveseq)


            elif maintain_option == 'obj_mdrive_new':
                print (" - in maintain_option: obj_mdrive_new")
                #print ("mdrive_objects at obj_mdrive_new")
                #print (mdrive_objects)

                mdrivecopy_objects = mdrive_obj_transform()  # use a local copy of mdrive_objects with underscores removed from description field
                # increase the number of mdrive objects by 1
                mdrive_number = mdrive_number + 1

                # create the new 'mdrive_objects' data row
                new_object_name =  request.args.get('newobjname')  # object name
                new_button_number =  str(mdrive_number)            # button number
                newseqfile =  request.args.get('seqfile')          # sequence file
                # convert any spaces in the new sequence file field to underscores and check it ends with .txt
                newseqfile =  newseqfile.replace(" ", "_")
                if newseqfile[-4][-1] != ".txt":
                    newseqfile = newseqfile + ".txt"
                    print (" .txt added to new sequence file name ")
                new_object_desc =  request.args.get('newobjdesc')  # object description
                if len(new_object_desc) == 0:
                    new_object_desc = "---"
                # convert any spaces in the new name and description fields to underscores
                new_object_name = new_object_name.replace(" ", "_")
                #print ("new_object_name = " + new_object_name)
                #print ("new_button_number = " + new_button_number)
                new_object_desc = new_object_desc.replace(" ", "_")
                #print ("new_object_desc = " + new_object_desc)
                #print ("newseqfile = " + newseqfile)
                new_row = np.array([new_object_name, new_button_number, newseqfile, new_object_desc])
                #print (new_row)
                # add the new row directly to the mdrive_objects master
                #print ("mdrive_objects before adding new row:")
                #print (mdrive_objects)

                temparray = np.vstack( (mdrive_objects, new_row) )

                #print ("temparray after new row")
                #print (temparray)

                mdrive_objects = temparray
                #print ("mdrive_objects after new row")
                #print (mdrive_objects)

                # resave the master objects file with the extended mdrive_objects content
                np.savetxt(str(mdrive_objects_file), mdrive_objects, fmt="%s", delimiter="  ")

                # initialise a new sequence numpy 2D array and store as a file
                #  the first value of the first line is set to 'newmotor' to signify 
                #  that this a new file without any set actions
                # the second line is actually set with some dummy values 
                #  just so that the the numpy array is created as 2D
                new_seq_content = np.array([("newmotor", "direction", "%speed", "run_duration(sec)", "sound_file_name", "play_time_ms", "play"),
                                            ("M1", "forwards", "50", "5", "nothing", "all", "once") ])
                print ("new seq file length: " + str(len(new_seq_content)) )
                print ("new seq file shape: " + str(np.shape(new_seq_content)) )

                np.savetxt(action_folder+str(mdrive_objects[mdrive_number][2]), new_seq_content, fmt="%s", delimiter="  ")

                # display the mdrive object edit text on the LCD
                print ("displaying the mdrive object edit text")
                lcddisp("new mdrive object", str(mdrive_objects[mdrive_number][0]), 1)

                webwarning = "EDITING: mdrive object " +str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])
                mdriveactsel = 0
                mdriveselnum = 0
                mdriveactlen = 0
                # recreate the local copy of the new mdrive_objects array
                mdrivecopy_objects = mdrive_obj_transform()  # use a local copy of mdrive_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: mdrive object management",
                    'description' : "mechatronic: maintenance - mdrive object management",
                    'warnweb' : webwarning,
                    'mdriveobjs' : mdrive_number,
                    'selmdriveobj' : mdriveselnum,
                    'selmdriveact' : mdriveactsel,
                    'lenmdriveact' : mdriveactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_mdrive.html', **template_data, mdrivecopy_objects = mdrivecopy_objects )


            elif maintain_option[0:22] == 'obj_mdrive_action_edit':
                print (" - in maintain_option: obj_mdrive_action_edit")
                #print ("mdrive_objects at obj_mdrive_action_edit")
                #print (mdrive_objects)

                mdriveactsel = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the mdrive object# from the passed URL

                # display the mdrive object edit text on the LCD
                print ("displaying the mdrive object edit text")
                lcddisp("mdrive object #"+str(mdriveselnum), "**action #" +str(mdriveactsel), 1)

                webwarning = "EDITING: mdrive object " +str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])+ " / action " +str(mdriveactsel)
                mdrivecopy_objects = mdrive_obj_transform()  # use a local copy of mdrive_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: mdrive object action update",
                    'description' : "mechatronic: maintenance - mdrive object management",
                    'warnweb' : webwarning,
                    'mdriveobjs' : mdrive_number,
                    'selmdriveobj' : mdriveselnum,
                    'selmdriveact' : mdriveactsel,
                    'lenmdriveact' : mdriveactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_mdrive.html', **template_data, mdrivecopy_objects = mdrivecopy_objects, mdriveseq = mdriveseq)


            elif maintain_option == 'obj_mdrive_action_update':
                print (" - in maintain_option: obj_mdrive_action_update")
                #print ("mdrive_objects at obj_mdrive_action_update")
                #print (mdrive_objects)

                # display the mdrive object edit text on the LCD
                print ("displaying the mdrive object action update text")
                lcddisp("mdrive object #"+str(mdriveselnum), "action#" +str(mdriveactsel) + " updated", 1)

                webwarning = "UPDATED: mdrive object " +str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])+ " / action " +str(mdriveactsel)
                mdrivecopy_objects = mdrive_obj_transform()  # use a local copy of mdrive_objects with underscores removed from description field

                ## update the action line from the URL responses and resave the file
                for i in range(0, 7):
                    # do some field content validation here at some point
                    mdriveseq[mdriveactsel][i] = request.args.get('field'+str(i))  # updated message from browser
                # now check that this was not the first action line to be set
                print ("mdriveseq[0][0]: " +str(mdriveseq[0][0]) )
                if str(mdriveseq[0][0]) == "newmotor": 
                    # a new action file - so reset the [0][0] value
                    mdriveseq[0][0] = "motor" 

                # resave the complete action file
                np.savetxt(action_folder+str(mdrive_objects[mdriveselnum][2]), mdriveseq, fmt="%s", delimiter="  ")
                print ("selected mdrive object action file resaved")

                template_data = {
                    'title' : "mechatronic: mdrive object action update",
                    'description' : "mechatronic: maintenance - mdrive object management",
                    'warnweb' : webwarning,
                    'mdriveobjs' : mdrive_number,
                    'selmdriveobj' : mdriveselnum,
                    'selmdriveact' : mdriveactsel,
                    'lenmdriveact' : mdriveactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_mdrive.html', **template_data, mdrivecopy_objects = mdrivecopy_objects, mdriveseq = mdriveseq)


            elif maintain_option == 'obj_mdrive_action_create':
                print (" - in maintain_option: obj_mdrive_action_create")

                mdriveactsel = mdriveactlen
                print ("mdriveactsel: " + str(mdriveactsel))
                mdriveactlen = mdriveactlen + 1
                print ("mdriveactlen: " + str(mdriveactlen))

                # display the mdrive object edit text on the LCD
                print ("displaying the mdrive object action create text")
                lcddisp("mdrive object #"+str(mdriveselnum), "action" +str(mdriveactsel) + " created", 1)

                webwarning = "CREATED: mdrive object " +str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])+ " / action " +str(mdriveactsel)

                ## create the action line from the URL responses and resave the file
                for i in range(0, 7):
                    # do some field content validation here at some point
                    #print ("i: " + str(i) )
                    #print ("fieldi value: " + str(request.args.get('field'+str(i))) )
                    mdriveseq[int(mdriveactsel)][i] = request.args.get('field'+str(i))  # updated message from browser
                    if i == 4:
                        mdriveseq[mdriveactsel][i] =  mdriveseq[mdriveactsel][i].replace(" ", "_")
                # now check that this was not the first action line to be set
                print ("mdriveseq[0][0]: " +str(mdriveseq[0][0]) )
                if str(mdriveseq[0][0]) == "newmotor": 
                    # a new action file - so reset the [0][0] value
                    mdriveseq[0][0] = "motor"

                # resave the complete action file
                np.savetxt(action_folder+str(mdrive_objects[mdriveselnum][2]), mdriveseq, fmt="%s", delimiter="  ")
                print ("selected mdrive object action file resaved")

                mdrivecopy_objects = mdrive_obj_transform()  # use a local copy of the mdrive_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: mdrive object action update",
                    'description' : "mechatronic: maintenance - mdrive object management",
                    'warnweb' : webwarning,
                    'mdriveobjs' : mdrive_number,
                    'selmdriveobj' : mdriveselnum,
                    'selmdriveact' : mdriveactsel,
                    'lenmdriveact' : mdriveactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_mdrive.html', **template_data, mdrivecopy_objects = mdrivecopy_objects, mdriveseq = mdriveseq)


            elif maintain_option[0:24] == 'obj_mdrive_action_delete':
                print (" - in maintain_option: obj_mdrive_action_delete")
                #print ("mdrive_objects at obj_mdrive_action_delete")
                #print (mdrive_objects)

                mdriveactdel = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the mdrive object# from the passed URL

                # display the mdrive object delete text on the LCD
                print ("displaying the mdrive object delete text")
                lcddisp("mdrive object #"+str(mdriveselnum), "delete action#" +str(mdriveactdel), 1)

                webwarning = "DELETED: mdrive object " +str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])+ " / action " +str(mdriveactdel)

                ## delete the action line selected from the URL responses and resave the file

                if mdriveactlen > 2:   # roll back the higher actions if there were more than one originally
                    for i in range (mdriveactdel, mdriveactlen-1):
                        for j in range (0,7):
                            mdriveseq[i,j] = mdriveseq[i+1,j]
                    print ("mdriveseq before delete:")
                    print (mdriveseq)
                    mdriveseq = np.delete(mdriveseq, mdriveactlen-1, axis=0)  # delete the last row
                    print ("mdriveseq after delete:")
                    print (mdriveseq)

                elif mdriveactlen == 2: # special case when there is just one action left
                    mdriveseq[0][0] = "newmotor"    # use the header 1st value to flag this special case
                    for j in range (0,7):
                        mdriveseq[1][j] = "-"       # put dummy values into the first 'action' row so that it is read properly as a 2D array

                print ("last action row deleted - length now: " + str(len(mdriveseq)) )
                mdriveactlen = mdriveactlen -1      # and now there is one less action
                print ("mdriveactlen reduced to: " + str(mdriveactlen) )

                # resave the complete action file
                np.savetxt(action_folder+str(mdrive_objects[mdriveselnum][2]), mdriveseq, fmt="%s", delimiter="  ")
                print ("selected mdrive object action file resaved")

                mdrivecopy_objects = mdrive_obj_transform()  # use a local copy of the mdrive_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: mdrive object action update",
                    'description' : "mechatronic: maintenance - mdrive object management",
                    'warnweb' : webwarning,
                    'mdriveobjs' : mdrive_number,
                    'selmdriveobj' : mdriveselnum,
                    'selmdriveact' : mdriveactsel,
                    'lenmdriveact' : mdriveactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_mdrive.html', **template_data, mdrivecopy_objects = mdrivecopy_objects, mdriveseq = mdriveseq)


            elif maintain_option[0:22] == 'obj_mdrive_action_test':
                print (" - in maintain_option: obj_mdrive_action_test")
                #print ("mdrive_objects at obj_mdrive_action_test")
                #print (mdrive_objects)

                mdriveacttest = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the mdrive object# from the passed URL
                mdriveactsel = mdriveacttest

                # display the mdrive object testing text on the LCD
                print ("displaying the mdrive object testing text")
                lcddisp("mdrive object #"+str(mdriveselnum), "testing action#" +str(mdriveacttest), 1)

                webwarning = "TESTED: mdrive object " +str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])+ " / action " +str(mdriveacttest)

                ## test the action line selected from the URL response

                # kill any previous audio that might be playing 
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")

                print (" processing activity sequence row " + str(mdriveacttest) )
                # ------------------------------------------------------------------------------------------------------
                # run the 'drive motor' activities: setting direction, speed and sound from the activity sequence file
                # ------------------------------------------------------------------------------------------------------

                # start sound as a background process unless it is set to 'nothing'
                print (" sound file: " + str(mdriveseq[mdriveacttest][4]) )

                # check sound file is needed before trying to play it
                if str(mdriveseq[mdriveacttest][4]) != "nothing":
                    if os.path.isfile(sound_folder+str(mdriveseq[mdriveacttest][4])):
                        lcddisp("drive motor ON", "sound file OK", 1)
                        print ("sound file " + str(mdriveseq[mdriveacttest][4]) + " found OK")
                        mylcd.lcd_display_string(str(mdrive_objects[mdriveselnum][0]), 2, 0)   # display at row 2 column 0
                        # play the sound once/repeat depending upon mdriveseq[mdriveacttest][6]
                        # in a new release use the time_ms setting, mdriveseq[mdriveacttest][5], to limit the time the sound is played
                        #   but it will be just set to a dummy value for now
                        play_sound(str(mdriveseq[mdriveacttest][4]), "all", str(mdriveseq[mdriveacttest][6])) # start sound as a background process

                    else:
                        lcddisp("*SYSTEM ERROR*", "NO sound file", 3)
                        print ("sound file " + str(mdriveseq[mdriveacttest][4]) + " NOT found")
                        webwarning = "ERROR: no sound file found for action " + str(mdriveacttest)

                print ("motor#: " + str(mdriveseq[mdriveacttest][0]) )
                print ("direction: " + str(mdriveseq[mdriveacttest][1]) )
                print ("speed: " + str(mdriveseq[mdriveacttest][2]) )
                print ("run time (secs): " + str(mdriveseq[mdriveacttest][3]) )

                # code to run a drive motor inserted below
                if str(mdriveseq[mdriveacttest][1]) == "stop" and str(mdriveseq[mdriveacttest][0]) == "M2":
                    Astop_pwm()
                    # stop any sounds that might be playing
                    player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print ("omxplayer killed")
                    lcddisp("** M2 motor **", "stopped", 0.1)
                    sleep( int(mdriveseq[mdriveacttest][3]) )
                elif str(mdriveseq[mdriveacttest][1]) == "stop" and str(mdriveseq[mdriveacttest][0]) == "M1":
                    Bstop_pwm()
                    # stop any sounds that might be playing
                    player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print ("omxplayer killed")
                    lcddisp("** M1 motor **", "stopped", 0.1)
                    sleep( int(mdriveseq[mdriveacttest][3]) )
                elif str(mdriveseq[mdriveacttest][3]) == "continuous" and str(mdriveseq[mdriveacttest][1]) == "forwards" and str(mdriveseq[mdriveacttest][0]) == "M2":
                    Aforward_pwm( int(mdriveseq[mdriveacttest][2]) )
                    lcddisp("** M2 motor **", "fwd continuous", 0.1)
                elif str(mdriveseq[mdriveacttest][3]) == "continuous" and str(mdriveseq[mdriveacttest][1]) == "forwards" and str(mdriveseq[mdriveacttest][0]) == "M1":
                    Bforward_pwm( int(mdriveseq[mdriveacttest][2]) )
                    lcddisp("** M1 motor **", "fwd continuous", 0.1)
                elif str(mdriveseq[mdriveacttest][3]) == "continuous" and str(mdriveseq[mdriveacttest][1]) == "backwards" and str(mdriveseq[mdriveacttest][0]) == "M2":
                    Abackward_pwm( int(mdriveseq[mdriveacttest][2]) )
                    lcddisp("** M2 motor **", "back continuous", 0.1)
                elif str(mdriveseq[mdriveacttest][3]) == "continuous" and str(mdriveseq[mdriveacttest][1]) == "backwards" and str(mdriveseq[mdriveacttest][0]) == "M1":
                    Bbackward_pwm( int(mdriveseq[mdriveacttest][2]) )
                    lcddisp("** M1 motor **", "back continuous", 0.1)

                elif str(mdriveseq[mdriveacttest][3]) != "continuous" and str(mdriveseq[mdriveacttest][1]) == "forwards" and str(mdriveseq[mdriveacttest][0]) == "M2":
                    lcddisp("** M2 motor **", "fwd " + str((mdriveseq[mdriveacttest][3]) + "s"), 0.1)
                    Aforward_pwm( int(mdriveseq[mdriveacttest][2]) )
                    sleep( int(mdriveseq[mdriveacttest][3]) )
                    Astop_pwm()

                elif str(mdriveseq[mdriveacttest][3]) != "continuous" and str(mdriveseq[mdriveacttest][1]) == "forwards" and str(mdriveseq[mdriveacttest][0]) == "M1":
                    lcddisp("** M1 motor **", "fwd " + str((mdriveseq[mdriveacttest][3]) + "s"), 0.1)
                    Bforward_pwm( int(mdriveseq[mdriveacttest][2]) )
                    sleep( int(mdriveseq[mdriveacttest][3]) )
                    Bstop_pwm()

                elif str(mdriveseq[mdriveacttest][3]) != "continuous" and str(mdriveseq[mdriveacttest][1]) == "backwards" and str(mdriveseq[mdriveacttest][0]) == "M2":
                    lcddisp("** M2 motor **", "back " + str((mdriveseq[mdriveacttest][3]) + "s"), 0.1)
                    Abackward_pwm( int(mdriveseq[mdriveacttest][2]) )
                    sleep( int(mdriveseq[mdriveacttest][3]) )
                    Astop_pwm()
                    # stop any sounds that might be playing
                    player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print ("omxplayer killed")

                elif str(mdriveseq[mdriveacttest][3]) != "continuous" and str(mdriveseq[mdriveacttest][1]) == "backwards" and str(mdriveseq[mdriveacttest][0]) == "M1":
                    lcddisp("** M1 motor **", "back " + str((mdriveseq[mdriveacttest][3]) + "s"), 0.1)
                    Bbackward_pwm( int(mdriveseq[mdriveacttest][2]) )
                    sleep( int(mdriveseq[mdriveacttest][3]) )
                    Bstop_pwm()
                    # stop any sounds that might be playing
                    player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    print ("omxplayer killed")

                else:
                    lcddisp("* drive motor *", "action " +str(mdriveacttest) + " not OK", 3)

                lcddisp("mdrive object #"+str(mdriveselnum), "action#" + str(mdriveacttest) + " tested!", 1)

                # 'just in case' stop the audio from playing so that any subsequent tests get a 'clean' start for any sounds
                player = subprocess.Popen(["omxplayer", "q" ], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

                mdrivecopy_objects = mdrive_obj_transform()  # use a local copy of the mdrive_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: mdrive object action test",
                    'description' : "mechatronic: maintenance - mdrive object management",
                    'warnweb' : webwarning,
                    'mdriveobjs' : mdrive_number,
                    'selmdriveobj' : mdriveselnum,
                    'selmdriveact' : mdriveactsel,
                    'lenmdriveact' : mdriveactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_mdrive.html', **template_data, mdrivecopy_objects = mdrivecopy_objects, mdriveseq = mdriveseq)


            elif maintain_option == 'obj_mdrive_action_addnew':
                print (" - in maintain_option: obj_mdrive_action_addnew")
                #print ("mdrive_objects at obj_mdrive_action_addnew")
                #print (mdrive_objects)

                # get the the new action insertion point from the browser returned value
                actinsertnum = int(request.args.get('newactnum'))  # input from browser

                # display the mdrive object add new action text on the LCD
                print ("displaying the mdrive object add new action text")
                lcddisp("mdrive object #"+str(mdriveselnum), "insert new action#" +str(actinsertnum), 1)

                webwarning = "INSERTED: drive motor object " +str(mdriveselnum) + " - " + str(mdrive_objects[mdriveselnum][0])+ " / new action " +str(actinsertnum)

                ## insert the action line selected from the URL responses and resave the file
                #print ("mdriveseq before insert:")
                #print (mdriveseq)
                mdriveactlen = mdriveactlen + 1
                new_action_row = np.array(["-", "-", "-", "-", "-", "-", "-"])
                # add a new row at the end of the actions array
                tempseq = np.vstack( (mdriveseq, new_action_row) )
                mdriveseq = tempseq
                #print ("mdriveseq after new row added at end:")
                #print (mdriveseq)

                # roll forward the existing actions into the new space unless the insertion is at the end in which case it is already done
                if actinsertnum != mdriveactlen:
                    for i in range (mdriveactlen-1, actinsertnum-1, -1):
                        #print ("i=" + str(i))
                        for j in range (0,7):
                            mdriveseq[i,j] = mdriveseq[i-1,j]
                    # populate the 'old' actinsertnum row with dummy values to be the new row
                    for j in range (0,7):
                        mdriveseq[actinsertnum,j] = "-"

                #print ("mdriveseq after insertion completion:")
                #print (mdriveseq)

                #print ("new action row inserted - length now: " + str(len(mdriveseq)) )
                #print ("mdriveactlen increased to: " + str(mdriveactlen) )

                # resave the complete action file
                np.savetxt(action_folder+str(mdrive_objects[mdriveselnum][2]), mdriveseq, fmt="%s", delimiter="  ")
                print ("selected mdrive object action file resaved")

                mdrivecopy_objects = mdrive_obj_transform()  # use a local copy of the mdrive_objects with underscores removed from description field

                template_data = {
                    'title' : "mechatronic: mdrive object action update",
                    'description' : "mechatronic: maintenance - mdrive object management",
                    'warnweb' : webwarning,
                    'mdriveobjs' : mdrive_number,
                    'selmdriveobj' : mdriveselnum,
                    'selmdriveact' : mdriveactsel,
                    'lenmdriveact' : mdriveactlen,
                    'build' : hardware,

                }
                return render_template('obj_type_mdrive.html', **template_data, mdrivecopy_objects = mdrivecopy_objects, mdriveseq = mdriveseq)


            # --------------------------------------------------------------------------------------


            elif maintain_option == 'sound_list':
                print (" - in maintain_option: sound_list")
                # stop any earlier sounds that might be playing
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")
                # display the web control select text on the LCD
                print ("displaying the web control select text")
                lcddisp("maintenance......", "sounds list", 1)

                webwarning = "" 
                page_title = "mechatronic: sound management "

                # get the current sound files loaded into the sound_folder if it has not already been read
                if soundfolder_read != "yes":
                    soundfiles = [f for f in listdir(sound_folder) if isfile(join(sound_folder, f))]
                    soundfiles_num = len(soundfiles)
                    soundfile_read = "yes"
                    for i in range(soundfiles_num):
                        print ("file " + str(i) + " - " + str(soundfiles[i]) )

                template_data = {
                    'title' : "mechatronic: sound management",
                    'description' : "mechatronic: maintenance - sound management",
                    'warnweb' : webwarning,
                    'numsoundfiles' : soundfiles_num,
                    'selsoundfile' : soundfile_sel,

                }
                return render_template('sound_options.html', **template_data, soundfiles = soundfiles)


            elif maintain_option[0:12] == 'sound_output':
                print (" - in maintain_option: sound_output")
                # nothing should be playing but just in case stop any earlier sounds that might be playing
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")

                if len(maintain_option) == 12:     # just at the initial choice stage, so no change of output made 
                    audio_num = 99
                    webwarning = ""
                    if audio_out == "local":
                        audiobox = "local analog port"
                    elif audio_out == "hdmi":
                        audiobox = "HDMI cable"
                    else:
                        audiobox = "undefined"

                else:  # a 0 or 1 choice has been made so make changes accordingly
                    audio_num = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the number from the passed URL
                    if audio_num == 0:    # this option sets the audio out to be the local analog port
                        print ("sound output is local analog port")
                        audio_out = "local"
                        audiobox = "local analog port"
                        webwarning = ""
                        lcddisp("*sound output*", "**local analog**", 1)
                    elif audio_num == 1:    # this option sets the audio out to be HDMI
                        print ("sound output is HDMI")
                        audio_out = "hdmi"
                        audiobox = "HDMI cable"
                        webwarning = ""
                        lcddisp("*sound output*", "*** HDMI ***", 1)
                    else:
                        print ("sound output choice invalid: so stays as local analog port")
                        audio_out = "local"
                        audiobox = "local socket"
                        webwarning ="WARNING: selected sound output invalid - set as local analog"
                        lcddisp("*sound output*", "**stays local**", 1)

                template_data = {
                    'title' : "mechatronic: sound output selection",
                    'description' : "mechatronic: maintenance - sound management",
                    'warnweb' : webwarning,
                    'numsoundfiles' : soundfiles_num,
                    'selsoundfile' : soundfile_sel,
                    'boxaudio' : audiobox,

                }
                return render_template('sound_output.html', **template_data)


            elif maintain_option[0:12] == 'sound_choose':
                print (" - in maintain_option: sound_choose")
                # stop any earlier sounds that might be playing
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")
                soundfile_sel = int(''.join(filter(str.isdigit, maintain_option)))  #  extract the sound file number from the passed URL
                webwarning = ""
                if soundfile_sel > 0 and soundfile_sel <= soundfiles_num:
                    print ("sound# selected: " + str(soundfile_sel))
                    webwarning = "SELECTED: sound file " + str(soundfile_sel) + " - " + str(soundfiles[soundfile_sel-1])
                    lcddisp("maintenance......", "sound selection", 1)
                else:
                    servoselnum = 0
                    webwarning ="WARNING selected servo object# is out of range"
                    lcddisp("*sound selected*", "**out of range**", 1)

                template_data = {
                    'title' : "mechatronic: sound file selection",
                    'description' : "mechatronic: maintenance - sound management",
                    'warnweb' : webwarning,
                    'numsoundfiles' : soundfiles_num,
                    'selsoundfile' : soundfile_sel,

                }
                return render_template('sound_options.html', **template_data, soundfiles = soundfiles)

            elif maintain_option == 'sound_play':
                print (" - in maintain_option: sound_play")
                # stop any earlier sounds that might be playing
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")
                if soundfile_sel > 0 and soundfile_sel <= soundfiles_num:
                    print ("sound# playing: " + str(soundfile_sel))
                    webwarning = "PLAYING: sound file " + str(soundfile_sel) + " - " + str(sound_folder)+str(soundfiles[soundfile_sel-1])
                    lcddisp("sound playing", "sound file: " +str(soundfile_sel), 1)
                    play_sound(str(soundfiles[soundfile_sel-1]), "all", "once")  # start sound as a background process 

                else:
                    servoselnum = 0
                    webwarning ="WARNING: cannot play - no sound file selected"
                    lcddisp("can't play sound", "no file selected", 1)

                template_data = {
                    'title' : "mechatronic: sound file selection",
                    'description' : "mechatronic: maintenance - sound management",
                    'warnweb' : webwarning,
                    'numsoundfiles' : soundfiles_num,
                    'selsoundfile' : soundfile_sel,

                }
                return render_template('sound_options.html', **template_data, soundfiles = soundfiles)


            elif maintain_option == 'sound_stop':
                print (" - in maintain_option: sound_stop")
                lcddisp("sound management", "**sound stopped**", 1)
                # stop any sounds that might be playing
                player = subprocess.Popen(["killall", "omxplayer.bin"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print ("omxplayer killed")
                webwarning = "STOPPED playing sound file" 
                template_data = {
                    'title' : "mechatronic: sound file selection",
                    'description' : "mechatronic: maintenance - sound management",
                    'warnweb' : webwarning,
                    'numsoundfiles' : soundfiles_num,
                    'selsoundfile' : soundfile_sel,

                }
                return render_template('sound_options.html', **template_data, soundfiles = soundfiles)


            elif maintain_option == 'sound_upload':
                print (" - in maintain_option: sound_upload")
                lcddisp("sound management", "sound upload", 1)
                webwarning = "UPLOADING sound file" 

                if request.method == 'POST':
                    # check if the post request has the file part
                    if 'file' not in request.files:
                        webwarning = "file 'reference' not found in 'upload' request" 
                        template_data = {
                            'title' : "mechatronic: playing sound file",
                            'description' : "mechatronic: maintenance - sound management/file playing",
                            'warnweb' : webwarning,
                            'numsoundfiles' : soundfiles_num,
                            'selsoundfile' : soundfile_sel,
                        }
                        return render_template('sound_options.html', **template_data, soundfiles = soundfiles)

                    # get the file name/details
                    file = request.files['file']
                    if file.filename == '':
                        print ("File name is blank")
                        lcddisp("sound upload", "file name blank", 1)
                        webwarning = "File name is 'blank' in the request"
                        template_data = {
                            'title' : "mechatronic: playing sound file",
                            'description' : "mechatronic: maintenance - sound management/file playing",
                            'warnweb' : webwarning,
                            'numsoundfiles' : soundfiles_num,
                            'selsoundfile' : soundfile_sel,
                        }
                        return render_template('sound_options.html', **template_data, soundfiles = soundfiles)

                    # check that file name 'allowed' and is 'secure'
                    if file and allowed_file(file.filename):
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(sound_folder, filename))
                        print ("File successfully uploaded")
                        lcddisp("sound management", "*upload done OK*", 1)
                        webwarning = "File successfully uploaded"
                        template_data = {
                            'title' : "mechatronic: playing sound file",
                            'description' : "mechatronic: maintenance - sound management/file playing",
                            'warnweb' : webwarning,
                            'numsoundfiles' : soundfiles_num,
                            'selsoundfile' : soundfile_sel,
                        }
                        return render_template('sound_options.html', **template_data, soundfiles = soundfiles)

                    else:
                        webwarning = "File name not allowed or not secure"
                        print ("File name not allowed or not secure")
                        lcddisp("sound upload", "*file name BAD*", 1)
                        template_data = {
                            'title' : "mechatronic: playing sound file",
                            'description' : "mechatronic: maintenance - sound management/file playing",
                            'warnweb' : webwarning,
                            'numsoundfiles' : soundfiles_num,
                            'selsoundfile' : soundfile_sel,
                        }
                        return render_template('sound_options.html', **template_data, soundfiles = soundfiles)

            # --------------------------------------------------------------------------------------

            elif maintain_option == 'sw_upgrade':
                print (" - in maintain_option: sw_upgrade")
                # display the web control select text on the LCD
                print ("displaying the web control select text")
                lcddisp("maintenance......", "software upgrade", 1)

                webwarning = "SORRY: this activity is not yet programmed" 
                page_title = "mechatronic: software upgrade"

                template_data = {
                    'title' : "mechatronic: software upgrade",
                    'description' : "mechatronic: maintenance - software upgrade",
                    'warnweb' : webwarning,


                }
                return render_template('sw_upgrade.html', **template_data)

            template_data = {
                'title' : "mechatronic: maintenance",
                'description' : "mechatronic: maintenance",
                'warnweb' : webwarning,
                'selservoobj' : servoselnum,
                'selstepobj' : stepselnum,
                'servoobjs' : object_number,
                'stepperobjs' : sopt_number,
                'build' : hardware,

            }
            return render_template('maintain.html', **template_data, cust_objects = cust_objects, servo_channels = servo_channels)


        ##################################################################################
        # the code below is the last code in the web part of the system
        ##################################################################################
        print ("starting web server")
        if __name__ == "__main__":
            mechatronic_app01.run(host='0.0.0.0', port=80, debug=False, threaded=True)   # 0.0.0.0 means any device on the network can access the web app


except AssertionError:
    print ("Exception routine")
    print ("AssertionError made as an exception and now ending the Try loop")
    pass

finally:  
    print ("Cleaning up at the end of the program")
    print(" ") 
    print(" ")
    print(" ")
    GPIO.cleanup()
    print("  ")
    print("*******************************************************")
    print("program end")
    print("*******************************************************")
    print("  ")
    mylcd.lcd_clear()
    mylcd.backlight(0)

