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

# EXP 1 (copy from ../20250602/intro_lab_auto.ipnb - section **Keitley 2600..** - **EXP 2**)
def keithely_actions_exp_1(keithley_instrument, stime):

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
    keithley_instrument.smub.source.limiti = 1e-3

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

    for v in range(1, 10):

        value = v * 0.01

        logging.info(f"source v from channel A: {value=} [V]")
        keithley_instrument.smua.source.levelv = value

        time.sleep(stime)

        i_a = keithley_instrument.smua.measure.i()
        logging.info(f"measured i at channel A: {i_a=} [V]")
        # print(f"current measured at A: {i_a}")
        
        v_a = keithley_instrument.smua.measure.v()
        logging.info(f"measured v at channel A: {v_a=} [V]")
        # print(f"voltage measured at A: {v_a}")

        v_b = keithley_instrument.smub.measure.v()
        logging.info(f"measured v at channel B: {v_b=} [V]")
        # print(f"voltage measured at B: {v_b}")
        

        time.sleep(1)

        logging.info(f"after 1s delay measure:")

        i_a_2 = keithley_instrument.smua.measure.i()
        logging.info(f"measured i at channel A: {i_a_2=} [V]")
        # print(f"current measured at A: {i_a}")
        
        v_a_2 = keithley_instrument.smua.measure.v()
        logging.info(f"measured v at channel A: {v_a_2=} [V]")
        # print(f"voltage measured at A: {v_a}")

        v_b_2 = keithley_instrument.smub.measure.v()
        logging.info(f"measured v at channel B: {v_b_2=} [V]")
        # print(f"voltage measured at B: {v_b}")

        logging.info(f"{'='*5}")

        # tst_global = tst_global + 1
    
    keithley_instrument.smua.source.output = keithley_instrument.smua.OUTPUT_OFF   # turn off SMUA
    keithley_instrument.smub.source.output = keithley_instrument.smub.OUTPUT_OFF   # turn off SMUB

# EXP 2 (STDP measurement)
# def keithely_actions_exp_2(keithley_instrument, stime, file_path, stop):
def keithely_actions_exp_2(keithley_instrument, arduino_board, file_path):

    # pulsewidth of the pre-synapse or post-synpse >> 24 ms (due to limit of the communication = code)

    number_of_measurements = 20
    # after the configuration
    settle_time = 100e-3 # s
    # during the measurement
    after_transition_settling_time = 50e-3 # s
    pulsewidth = 1000e-3 # s
    delta_t = 400e-3 # s
    rest_time = 1 # s

    # arduino bin
    pre_arduino_bin = 10
    post_arduino_bin = 9
    
    field_names = ['time', 'i', 'v']

    with open(file_path, 'w') as file:
        file_writer = csv.DictWriter(file, fieldnames=field_names)
        file_writer.writeheader()

    # while True:
    with open(file_path, 'a') as file:

            file_writer = csv.DictWriter(file, fieldnames=field_names)

            # PAGE 2-14
            # ======
            # Configure smub as only voltmeter
            # ======

                # reset the channel
            keithley_instrument.smub.reset()
            
                # Clear buffer 1.
            keithley_instrument.smub.nvbuffer1.clear()

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

            # # page 3-8
            # # ======
            # # Configure smua as source v, measure i
            # # ======

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

                # Set the bias voltage to 0 V. (Drain/ Source voltage)
            keithley_instrument.smua.source.levelv = -0.1

            # # ======
            # # Open all switches
            # # ======
            # For the relay board: HIGH = OFF = OPEN // LOW = ON = CLOSE
                # post-synapse
            arduino_board.digital[post_arduino_bin].write(1)
                # pre-synapse 
            arduino_board.digital[pre_arduino_bin].write(1)

            # wait for the open transition to tbe stable
            time.sleep(0.5)

            # # ======
            # # Measuring
            # # ======

                # Turn on the voltmeter.
            keithley_instrument.smub.source.output = keithley_instrument.smub.OUTPUT_ON

                # Turn on the output source.
            keithley_instrument.smua.source.output = keithley_instrument.smua.OUTPUT_ON

                # Settling time
            time.sleep(settle_time)

                # start measurement
            start_time = time.time()
            logging.info(f"starting the measurement process")
                    # For loop (number of measurements)
            for i in range(0, number_of_measurements):
                        # start the pre-synapse phase = close the pre-synapse switch
                arduino_board.digital[pre_arduino_bin].write(0)
                        # settling time of the presynapse phase
                time.sleep(after_transition_settling_time)
                        # mark the measurement moment
                time_when_measure = time.time() - start_time
                        # measure the current through channel (save to file)
                measured_i_channel = keithley_instrument.smua.measure.i()
                        # measure the voltage at the gate (save to file)
                measured_v_gate = keithley_instrument.smub.measure.v()
                        # save the time when receiving the measurement (save to file)
                measured_t = time.time() - start_time
                info = {
                            'time': measured_t,
                            'i': measured_i_channel,
                            'v': measured_v_gate
                        }
                        # finish the pre-synapse phase
                logging.info(f"duration of query {measured_t - time_when_measure=}")
                time.sleep(pulsewidth - after_transition_settling_time - (measured_t - time_when_measure))
                        # end the pre-synapse phase = open the pre-synapse switch
                arduino_board.digital[pre_arduino_bin].write(1)
                        # delta_t = t_pre_spike - t_post_spike (case pre_spike before post_spike)
                time.sleep(delta_t)
                        # start post-synapse phase
                arduino_board.digital[post_arduino_bin].write(0)
                time.sleep(pulsewidth)
                        # end of post-synapse phase
                arduino_board.digital[post_arduino_bin].write(1)
                        # rest after a measurement
                # good moment to save to file without affecting the critical process
                file_writer.writerow(info) 
                logging.info(f"write {info} to csv")
                time.sleep(rest_time)

    # # ======
    # # Open all switches
    # # ======
    # For the relay board: HIGH = OFF = OPEN // LOW = ON = CLOSE
            # post-synapse
    arduino_board.digital[post_arduino_bin].write(1)
            # pre-synapse 
    arduino_board.digital[pre_arduino_bin].write(1)

    keithley_instrument.smua.source.output = keithley_instrument.smua.OUTPUT_OFF   # turn off SMUA
    keithley_instrument.smub.source.output = keithley_instrument.smub.OUTPUT_OFF   # turn off SMUB

def read_from_file_and_plot (_, file_path):
    # global file_path
    data = pd.read_csv(file_path)
    x = data['time']
    y = data['i']

    plt.cla()
    plt.plot(x, y)


def try_arduino_board(board):
    while True:
        print(f"HIGH")
        # For the relay board: HIGH = OFF
        board.digital[9].write(1) # digital pin 13 = built-in LED
        board.digital[10].write(1) # digital pin 13 = built-in LED
        time.sleep(1) # second
        # print(f"LOW")
        # # For the relay board: LOW = ON
        # board.digital[9].write(0)
        # board.digital[10].write(0)
        # time.sleep(1)

        
if __name__ == "__main__":

        # init logger
    format = "%(asctime)s: %(message)s"
    log_file_path = 'example.log'
    logging.basicConfig(format=format, level=logging.INFO,  
                        datefmt="%H:%M:%S", filename= log_file_path, filemode= 'w')

        # init the instrument handle
    k = Keithley2600('USB0::0x05E6::0x2636::4480001::INSTR', visa_library = 'C:/windows/System32/visa64.dll')
        # init the arduino board
    board = pyfirmata.Arduino('COM8')
    # # ======
    # # Open all switches
    # # ======
    # For the relay board: HIGH = OFF = OPEN // LOW = ON = CLOSE
            # post-synapse
    board.digital[9].write(1)
            # pre-synapse 
    board.digital[10].write(1)

        # path to the measurement record
    file_path = "C:/Users/20245580/LabCode/Automate_Lab_Instrument/20250605/output_exp3.csv"

    logging.info("Main    : Prepare measurement")

    stop_keithley_write_threads = False
    xw = threading.Thread(target=keithely_actions_exp_2 ,daemon= True, args=(k, board, file_path))


    logging.info("Main    : Run measurement")
    xw.start()

    ani = animation.FuncAnimation(plt.gcf(), read_from_file_and_plot, interval= 2000, fargs= (file_path, ))
    plt.show()



        # Trial
            ## 3
        # init the arduino board
    # board = pyfirmata.Arduino('COM8')
    # xw = threading.Thread(target=try_arduino_board ,daemon= True, args=(board,))


    # logging.info("Main    : Run measurement")
    # xw.start()

    # time.sleep(5)

            ## 2
    # while True:
    #     board.digital[10].write(1) # digital pin 13 = built-in LED
    #     time.sleep(5) # second
    #     board.digital[10].write(0)
    #     time.sleep(5)






