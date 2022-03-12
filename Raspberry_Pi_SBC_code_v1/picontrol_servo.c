// picontrol_servo.c custom C code for mechatronic activities that use PCA9685 servo functions
// originally developed by Enmore in August 2019
// this Maker Kit variant developed Jan '22

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>   // added so that usleep(microseconds) can be used
#include <PCA9685.h>  // include the PCA9865 custom library
#include "picontrol_servo.h"

// globals
int __fd;    // needed for cleanup()
int __addr;  // needed for cleanup()
int debug = 1;   // set to 1 for more detailed outputs, but when production ready it can be set to 0 and the code recompiled

int fd;
int addr = 0x40;
// Example for a second device. Set addr2 to device address (if set to 0x00 no second device will be used)
int fd2;
int addr2 = 0x00;

int adpt = 1;
int frequency = 50;

int START_REG = 0x06;


// ************************************************************
// this simple 'connection' function included for test purposes
// ************************************************************
void connect_servo()
{
    printf("Connected to the picontrol PCA9685 servo C library...\n");
}


// ***************************
// PWM module clean up routine
// ***************************
void PWMcleanup() {
  // attempt to turn off all PWM
  PCA9685_setAllPWM(__fd, __addr, _PCA9685_MINVAL, _PCA9685_MINVAL);
} // PWMcleanup


// ********************************
// routine to turn off all channels
//*********************************
void intHandler(int dummy) {
  // turn off all channels
  PCA9685_setAllPWM(fd, addr, _PCA9685_MINVAL, _PCA9685_MINVAL);
  exit(dummy);
} // intHndler


// ***********************************
// PCA9685 PWM hardware set up routine
// ***********************************
int PWMsetup(unsigned char mod_addr, unsigned int freq) {

  int ret;     // returned value from PCA9685_dumpAllRegs
  int afd;     // returned 'file descriptor' from PCA9685_openI2C
  int result;  // returned value from PCA9685_initPWM
  
  afd = PCA9685_openI2C(adpt, mod_addr);
  if (debug) {
    printf ("I2C file descriptor is %d  \n ", afd);
  }	// if debug

  result = PCA9685_initPWM(afd, mod_addr, freq);
  if (debug) {
    printf ("PWM set up result is %d  \n ", result);
  } // if debug

  if (debug) {
    // display all used pca registers 
    ret = PCA9685_dumpAllRegs(afd, mod_addr);
    if (ret != 0) {
      fprintf(stderr, "PWMsetup(): PCA9685_dumpAllRegs() returned %d\n", ret);
      return -1;
    } // if ret
  } // if debug

  return afd;
} // PWMsetup

// *****************************
// routine to set a single servo
// *****************************
int setServo(int fd, int channel, int value, int waittime) {
  // fd is the I2C file descriptor - typically 3
  // channel is the servo# 0-15
  // value is the PWM off setting 0-4096 but for a SG90 servo is usually in the range 160-560
  // waittime is a time in ms to wait after the servo is set - usually zero
  int uwait = waittime*1000; // convert ms to microseconds for the usleep function

  // calculate the register# to be set
  int setreg = START_REG+4*channel;
  
  if (debug) {
    printf ("parameters for setting a single servo \n ");
	printf ("passed thru I2C file descriptor is %d  \n ", fd);
	printf ("channel being set is %d  \n ", channel);
	printf ("=>register being set is %d  \n ", setreg); 
	printf ("off value being set is %d  \n ", value); 
  } // if debug

  // just use the standard PCA9685_setPWMVal function with set/default values
  PCA9685_setPWMVal(fd, addr, setreg, 0, value);
  usleep(uwait);  //wait after setting each servo - typically used to slow down for debug to see what is happening
  
}

