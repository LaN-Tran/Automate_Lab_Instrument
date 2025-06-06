"""
    Automation Keithley 2602B measurement
    STDP experiment
    Author:  Tran Le Phuong Lan.
    Created:  2025-06-05

    Requires:                       
       Python 2.7, 3
    Reference:

    [1] [live plotting data](https://www.youtube.com/watch?v=Ercd-Ip5PfQ&t=563s)
    
    [2] [closing event of matplotlib window](https://matplotlib.org/stable/gallery/event_handling/close_event.html)

    [3] [python timer to track time](https://stackoverflow.com/questions/70058132/how-do-i-make-a-timer-in-python)
"""

# Libs
import pyvisa
import time
from  keithley2600 import Keithley2600, ResultTable
import threading
import logging
import pyfirmata
import time
import json
import numpy as np
import os
import matplotlib.pyplot as plt
import multiprocessing, time, signal
import csv
import pandas as pd
import matplotlib.animation as animation

# check the instrument (e.g Keithley 2602B) VISA address
# rm = pyvisa.ResourceManager('C:/windows/System32/visa64.dll')
# print(rm.list_resources())

# EXP 1 (measuring current and voltage through a single resistor)
def keithely_actions_exp_1(keithley_instrument, stime, file_path, stop):


    field_names = ['time', 'i', 'va', 'vb']

    with open(file_path, 'w') as file:
        file_writer = csv.DictWriter(file, fieldnames=field_names)
        file_writer.writeheader()


    # global tst_global

    # PAGE 2-14
    # ======
    # Configure smub as only voltmeter
    # ======

    # Clear buffer 1.
    keithley_instrument.smub.nvbuffer1.clear()

    # reset the channel
    keithley_instrument.smub.reset()

    # (step 1) Select the current source function.
    keithley_instrument.smub.source.func = keithley_instrument.smub.OUTPUT_DCAMPS

    # (step 2)
    ## source side
    # Set the bias current to 0 A. (source level)
    keithley_instrument.smub.source.leveli = 0.0
    # Set the source range to lowest (resolution): 100 nA
    keithley_instrument.smub.source.rangei = 100e-9
    # Set the current limit (safety) to MUST BE higer than in the expected measurement
    keithley_instrument.smub.source.limiti = 1

    ## measure side
    # ? When selecting as current source, 
    # the instrument channel is automatically thought of as voltage meter ?

    # Select measure voltage autorange.
    keithley_instrument.smub.measure.autorangev = keithley_instrument.smub.AUTORANGE_ON

    # Enable 2-wire.
    keithley_instrument.smub.sense = keithley_instrument.smub.SENSE_LOCAL

    # page 3-8
    # ======
    # Configure smua as source v, measure i
    # ======

    # Restore 2600B defaults.
    keithley_instrument.smua.reset()

    # Select channel A display.
    keithley_instrument.display.screen = keithley_instrument.display.SMUA

    # Display current.
    keithley_instrument.display.smua.measure.func = keithley_instrument.display.MEASURE_DCAMPS

    # Select measure I autorange.
    keithley_instrument.smua.measure.autorangei = keithley_instrument.smua.AUTORANGE_ON

    # Select ASCII data format.
    # smu.write('format.data = format.ASCII')

    # Clear buffer 1.
    keithley_instrument.smua.nvbuffer1.clear()

    # Select the source voltage function.
    keithley_instrument.smua.source.func = keithley_instrument.smua.OUTPUT_DCVOLTS

    # Set the bias voltage to 0 V.
    keithley_instrument.smua.source.levelv = 0.0

    # Turn on the voltmeter on.
    keithley_instrument.smub.source.output = keithley_instrument.smub.OUTPUT_ON

    # Turn on the output source on.
    keithley_instrument.smua.source.output = keithley_instrument.smua.OUTPUT_ON

    
        # start measurement
    start_time = time.time()

    while True:

                with open(file_path, 'a') as file:

                    file_writer = csv.DictWriter(file, fieldnames=field_names)

                    value = 0.1

                    logging.info(f"source v from channel A: {value=} [V]")
                    keithley_instrument.smua.source.levelv = value

                    time.sleep(stime)

                    i_a = keithley_instrument.smua.measure.i()
                    logging.info(f"measured i at channel A: {i_a=} [V]")
                    
                    v_a = keithley_instrument.smua.measure.v()
                    logging.info(f"measured v at channel A: {v_a=} [V]")

                    v_b = keithley_instrument.smub.measure.v()
                    logging.info(f"measured v at channel B: {v_b=} [V]")

                    info = {
                                'time': time.time() - start_time,
                                'i': i_a,
                                'va': v_a,
                                'vb': v_b
                            }
                    
                    file_writer.writerow(info)
                    time.sleep(1)

                    logging.info(f"after 1s delay measure:")

                    i_a_2 = keithley_instrument.smua.measure.i()
                    logging.info(f"measured i at channel A: {i_a_2=} [V]")
                    
                    v_a_2 = keithley_instrument.smua.measure.v()
                    logging.info(f"measured v at channel A: {v_a_2=} [V]")

                    v_b_2 = keithley_instrument.smub.measure.v()
                    logging.info(f"measured v at channel B: {v_b_2=} [V]")

                    info = {
                                'time': time.time() - start_time,
                                'i': i_a_2,
                                'va': v_a_2,
                                'vb': v_b_2
                            }
                    
                    logging.info(f"{'='*5}")
                    file_writer.writerow(info)

                if stop():
                     break

                # tst_global = tst_global + 1
    
    keithley_instrument.smua.source.output = keithley_instrument.smua.OUTPUT_OFF   # turn off SMUA
    keithley_instrument.smub.source.output = keithley_instrument.smub.OUTPUT_OFF   # turn off SMUB



        
if __name__ == "__main__":

        # init logger
    format = "%(asctime)s: %(message)s"
    log_file_path = 'example.log'
    logging.basicConfig(format=format, level=logging.INFO,  
                        datefmt="%H:%M:%S", filename= log_file_path, filemode= 'w')

        # init the instrument handle
    k = Keithley2600('USB0::0x05E6::0x2636::4480001::INSTR', visa_library = 'C:/windows/System32/visa64.dll')
        # init the arduino board
    
    
    logging.info("Main    : Prepare measurement")
    file_path = "C:/Users/20245580/LabCode/Automate_Lab_Instrument/20250605/output_exp2.csv"
    stop_keithley_write_threads = False
    xw = threading.Thread(target=keithely_actions_exp_1 ,daemon= True, args=(k, 0.1, file_path, lambda: stop_keithley_write_threads))

    logging.info("Main    : Run measurement")
    xw.start()

    while True:
        
         print(f"input 'stop_thread', then 'stop_main':  ")
         input_str = str(input())

         match input_str:
                case "stop_thread":
                   stop_keithley_write_threads = True
                case "stop_main":
                    if stop_keithley_write_threads == True:
                        break
                    else:
                         pass






