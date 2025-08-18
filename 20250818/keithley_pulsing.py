"""
    Automation Keithley 2602B
    Keithley pulse drain (smuA) and pulse gate (smuB) 
    Author:  Tran Le Phuong Lan.
    Created:  2025-08-18

    Requires:                       
       Python 2.7, 3
       pyvisa
       pyusb
       Keithley2600
    Reference:

"""

import pyvisa
from  keithley2600 import Keithley2600
import time
import logging
import csv
import os
from datetime import datetime

    # # ======
    # # Logger
    # # ======
# init logger
format = "%(asctime)s: %(message)s"
log_file_path = 'example.log'
logging.basicConfig(format=format, level=logging.INFO,  
                        datefmt="%H:%M:%S", filename= log_file_path, filemode= 'w')

    # # ======
    # # Keithley
    # # ======
# init logger
keithley_instrument = Keithley2600('USB0::0x05E6::0x2636::4480001::INSTR', visa_library = 'C:/windows/System32/visa64.dll', timeout = 100000)
keithley_instrument.smua.source.output = keithley_instrument.smua.OUTPUT_OFF
keithley_instrument.smub.source.output = keithley_instrument.smub.OUTPUT_OFF

 
#-- Reset SourceMeter instrument to default conditions.
keithley_instrument.reset()
# -- Generate a single pulse with the following characteristics:
# -- * Bias (idle) level = 0 V
# -- * Pulse level = 5 V
# -- * Pulse width = 500 us
# -- Configure the source function.
keithley_instrument.smua.source.func = keithley_instrument.smua.OUTPUT_DCVOLTS
#-- Set the voltage source range and the idle or bias source level and limit.
keithley_instrument.smua.source.rangev = 5
keithley_instrument.smua.source.levelv = 0
keithley_instrument.smua.source.limiti = 0.1
#-- Configure the trigger-timer parameters to output a single 500 us pulse.
keithley_instrument.trigger.timer[1].delay = 0.0005
keithley_instrument.trigger.timer[1].count = 1
keithley_instrument.trigger.timer[1].passthrough = False # timers does not trigger an event when it is triggered.
# -- Start the timer when the SMU moves from the ARM layer to the TRIGGER layer.
keithley_instrument.trigger.timer[1].stimulus = keithley_instrument.smua.trigger.ARMED_EVENT_ID
# -- Configure the trigger model to execute a single-point voltage pulse list sweep.
# -- No measurements are made.
keithley_instrument.smua.trigger.source.listv({5})
keithley_instrument.smua.trigger.source.action = keithley_instrument.smua.ENABLE
keithley_instrument.smua.trigger.measure.action = keithley_instrument.smua.DISABLE
# -- Set the trigger source limit to the same value as the bias limit.
keithley_instrument.smua.trigger.source.limiti = keithley_instrument.smua.LIMIT_AUTO
keithley_instrument.smua.measure.rangei = 0.1
# -- Configure the source action to start immediately.
keithley_instrument.smua.trigger.source.stimulus = 0
# -- Configure the endpulse action to achieve a pulse.
keithley_instrument.smua.trigger.endpulse.action = keithley_instrument.smua.SOURCE_IDLE
keithley_instrument.smua.trigger.endpulse.stimulus = keithley_instrument.trigger.timer[1].EVENT_ID
# -- Set the appropriate counts for the trigger model.
keithley_instrument.smua.trigger.arm.count = 1
keithley_instrument.smua.trigger.count = 1
# -- Turn on the SMU output and initiate the trigger model to output a single pulse.
keithley_instrument.smua.source.output = smua.OUTPUT_ON
keithley_instrument.smua.trigger.initiate()
# -- Wait for the sweep to complete.
keithley_instrument.waitcomplete()
# -- Turn off SMU output.
# smua.source.output = smua.OUTPUT_OFF


# -- Generate a 10-point pulse train with the following characteristics:
# -- * Bias (Idle) Level = 0 V
# -- * Pulse Level = 5 V
# -- * Pulse Width = 600 us
# -- * Pulse Period = 5 ms
# -- Configure the source function.
keithley_instrument.smua.source.func = keithley_instrument.smua.OUTPUT_DCVOLTS
# -- Set the voltage source range and the bias source level and limit.
keithley_instrument.smua.source.rangev = 5
keithley_instrument.smua.source.levelv = 0
keithley_instrument.smua.source.limiti = 0.1
# -- Use trigger timer 1 to control the period and trigger timer 2 to control the 
# -- pulse width. Alias the timers for convenience and clarity.
period_timer = keithley_instrument.trigger.timer[1]
pulsewidth_timer = keithley_instrument.trigger.timer[2]
# -- Configure the period timer to output 10 total trigger events.
period_timer.delay = 0.005
# -- The effective count is 10 because the passthrough setting is true.
period_timer.count = 9
# -- Configure the timer to immediately output a trigger event when it is started.
keithley_instrument.period_timer.passthrough = True
# -- Start the timer when the SMU moves from the ARM layer to the TRIGGER layer.
period_timer.stimulus = keithley_instrument.smua.trigger.ARMED_EVENT_ID
# -- Configure the pulse width timer to output one trigger event for each period.
pulsewidth_timer.delay = 0.0006
pulsewidth_timer.count = 1
# -- Do not immediately output a trigger event when pulse width timer is started.
pulsewidth_timer.passthrough = False
# -- Start the pulse width timer with the period timer output trigger event.
pulsewidth_timer.stimulus = period_timer.EVENT_ID
# -- Configure the trigger model to execute a 10-point fixed-level voltage pulse 
# -- train. No measurements are made.
keithley_instrument.smua.trigger.source.listv({5})
keithley_instrument.smua.trigger.source.action = keithley_instrument.smua.ENABLE
keithley_instrument.smua.trigger.measure.action = keithley_instrument.smua.DISABLE
# -- Set the trigger source limit, which can be different than the bias limit.
# -- This is an important setting for pulsing in the extended operating area.
keithley_instrument.smua.trigger.source.limiti = 1
keithley_instrument.smua.measure.rangei = 1
# -- Trigger SMU source action with the period timer event.
keithley_instrument.smua.trigger.source.stimulus = period_timer.EVENT_ID
# -- Configure the endpulse action to achieve a pulse.
keithley_instrument.smua.trigger.endpulse.action = keithley_instrument.smua.SOURCE_IDLE
# -- Trigger the SMU end pulse action with a pulse width timer event.
keithley_instrument.smua.trigger.endpulse.stimulus = pulsewidth_timer.EVENT_ID
# -- Set the trigger model count to generate one 10-point pulse train.
keithley_instrument.smua.trigger.arm.count = 1
keithley_instrument.smua.trigger.count = 10
# -- Turn on the SMU output and initiate the trigger model to output the pulse train.
keithley_instrument.smua.source.output = keithley_instrument.smua.OUTPUT_ON
keithley_instrument.smua.trigger.initiate()
# -- Wait for the sweep to complete.
keithley_instrument.waitcomplete()
# -- Turn off SMU output.
# smua.source.output = smua.OUTPUT_OFF

    # -- Temporary variables used by this function. 

    # local l_j, l_tonwm 

 

#-- Clear the front panel display then prompt for input parameters if missing. 
keithley_instrument.display.clear() 

 
bias = 0
    # if bias == nil then 

    #     bias = display.prompt(l_volts_fmt, " Volts", "Enter BIAS Voltage.", 0, -l_max_volts, l_max_volts) 

    #     if bias == nil then 

    #         -- Abort if Exit key pressed 

    #         AbortScript(l_d_screen) 

    #     end 

    # end 
pulse_voltage = 0.2
    # if level == nil then 

    #     level = display.prompt(l_volts_fmt, " Volts", "Enter PULSE Voltage.", 1, -l_max_volts, l_max_volts) 

    #     if level == nil then 

    #         -- Abort if Exit key pressed 

    #         AbortScript(l_d_screen) 

    #     end 

    # end 
ton = 0.2 # [s], pulse on time

    # if ton == nil then 

    #     ton = display.prompt("00.000E+00", " Seconds", "Enter pulse ON time.", 20E-3, 0, 20) 

    #     if ton == nil then 

    #         -- Abort if Exit key pressed 

    #         AbortScript(l_d_screen) 

    #     end 

    # end 
toff = 0.8 # [s], pulse off time
    # if toff == nil then 

    #     toff = display.prompt("00.000E+00", " Seconds", "Enter pulse OFF time.", 20E-3, 0, 20) 

    #     if toff == nil then 

    #         -- Abort if Exit key pressed 

    #         AbortScript(l_d_screen) 

    #     end 

    # end 
n_pulses = 20 
    # if points == nil then 

    #     points = display.prompt("0000", " Pulses", "Enter number of pulses", 10, 1, 1000) 

    #     if points == nil then 

    #         -- Abort if Exit key pressed 

    #         AbortScript(l_d_screen) 

    #     end 

    # end 


# -- Update display with test info. 

keithley_instrument.display.settext("PulseVMeasureI")  #-- Line 1 (20 characters max) 

 

#-- Configure source and measure settings (drain). 

keithley_instrument.smua.source.output = keithley_instrument.smua.OUTPUT_OFF 

if abs(pulse_voltage) > abs(bias):

    keithley_instrument.smua.source.rangev = pulse_voltage 

else: 

    keithley_instrument.smua.source.rangev = bias 


keithley_instrument.smua.source.levelv = bias 
keithley_instrument.smua.source.func = keithley_instrument.smua.OUTPUT_DCVOLTS 
keithley_instrument.smua.measure.autozero = keithley_instrument.smua.AUTOZERO_OFF 
keithley_instrument.smua.enable = keithley_instrument.smua.FILTER_OFF 

keithley_instrument.smua.measure.nplc = 1
l_tonwm = ton - (keithley_instrument.smua.measure.nplc/keithley_instrument.localnode.linefreq) - 250E-6 

 

#-- Setup a buffer to store the result(s) in and start testing. 

smu.nvbuffer1.clear() 

smu.nvbuffer1.appendmode = 1 

smu.nvbuffer1.collecttimestamps = 1 

smu.nvbuffer1.collectsourcevalues = 1 

 

#-- Configure triggering. 

smu.trigger.arm.stimulus = 0 

trigger.timer[1].reset() 

trigger.timer[1].delay = l_tonwm 

trigger.timer[1].count = 1 

trigger.timer[1].stimulus = smu.trigger.SOURCE_COMPLETE_EVENT_ID 

smu.trigger.measure.stimulus = trigger.timer[1].EVENT_ID 

trigger.timer[2].reset() 

trigger.timer[2].delay = ton 

trigger.timer[2].count = 1 

trigger.timer[2].stimulus = smu.trigger.SOURCE_COMPLETE_EVENT_ID 

smu.trigger.endpulse.stimulus = trigger.timer[2].EVENT_ID 

trigger.timer[3].reset() 

trigger.timer[3].delay = toff 

trigger.timer[3].count = 1 

trigger.timer[3].stimulus = smu.trigger.PULSE_COMPLETE_EVENT_ID 

smu.trigger.source.stimulus = trigger.timer[3].EVENT_ID 

 

smu.trigger.source.linearv(level, level, 1) 

smu.trigger.source.action = smu.ENABLE 

smu.trigger.measure.i(smu.nvbuffer1) 

smu.trigger.measure.action = smu.ENABLE 

smu.trigger.endpulse.action = smu.SOURCE_IDLE 

smu.trigger.arm.count = 1 

smu.trigger.count = points 

 

#-- Initiate the pulses 

smu.source.output = smu.OUTPUT_ON 

smu.trigger.initiate() 

delay(toff) 

smu.trigger.source.set() 

waitcomplete() 

delay(toff) 

smu.source.output = smu.OUTPUT_OFF 

 

#-- Update the front panel display and restore modified settings. 

display.setcursor(2,1) 

display.settext("Test complete.")  -- Line 2 (32 characters max) 

smu.source.levelv = 0 

smu.source.rangev = l_s_rangev 

smu.source.autorangev = l_s_autorangev 

smu.source.func = l_s_func 

smu.source.levelv = l_s_levelv 

smu.measure.autozero = l_m_autozero 

smu.measure.filter.enable = l_m_filter 

delay(2) 

display.clear() 

display.screen = l_d_screen  