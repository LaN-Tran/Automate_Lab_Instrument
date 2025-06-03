"""
   Automation Keithley 2602B measurement
   Author:  Tran Le Phuong Lan.
   Created:  2025-06-03

   Requires:                       
       Python 2.7, 3
"""

# Libs
import pyvisa
import time
from  keithley2600 import Keithley2600, ResultTable
import threading
import logging


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

# EXP 2 (copy from ../20250602/intro_lab_auto.ipnb - section **Keitley 2600..** - **EXP 2**)
def keithely_actions_exp_2(keithley_instrument, stime, stop):

    # global tst_global
    while True:
        logging.info(f"inside keithley inf loop")
        time.sleep(1)
        if stop():
            break

    # PAGE 2-14
    # ======
    # Configure smub as only voltmeter
    # ======

    # # Clear buffer 1.
    # keithley_instrument.smub.nvbuffer1.clear()

    # # reset the channel
    # keithley_instrument.smub.reset()

    # # (step 1) Select the current source function.
    # keithley_instrument.smub.source.func = keithley_instrument.smub.OUTPUT_DCAMPS

    # # (step 2)
    # ## source side
    # # Set the bias current to 0 A. (source level)
    # keithley_instrument.smub.source.leveli = 0.0
    # # Set the source range to lowest (resolution): 100 nA
    # keithley_instrument.smub.source.rangei = 100e-9
    # # Set the current limit (safety) to MUST BE higer than in the expected measurement
    # keithley_instrument.smub.source.limiti = 1e-3

    # ## measure side
    # # ? When selecting as current source, 
    # # the instrument channel is automatically thought of as voltage meter ?

    # # Select measure voltage autorange.
    # keithley_instrument.smub.measure.autorangev = keithley_instrument.smub.AUTORANGE_ON

    # # Enable 2-wire.
    # keithley_instrument.smub.sense = keithley_instrument.smub.SENSE_LOCAL

    # # page 3-8
    # # ======
    # # Configure smua as source v, measure i
    # # ======

    # # Restore 2600B defaults.
    # keithley_instrument.smua.reset()

    # # Select channel A display.
    # keithley_instrument.display.screen = keithley_instrument.display.SMUA

    # # Display current.
    # keithley_instrument.display.smua.measure.func = keithley_instrument.display.MEASURE_DCAMPS

    # # Select measure I autorange.
    # keithley_instrument.smua.measure.autorangei = keithley_instrument.smua.AUTORANGE_ON

    # # Select ASCII data format.
    # # smu.write('format.data = format.ASCII')

    # # Clear buffer 1.
    # keithley_instrument.smua.nvbuffer1.clear()

    # # Select the source voltage function.
    # keithley_instrument.smua.source.func = keithley_instrument.smua.OUTPUT_DCVOLTS

    # # Set the bias voltage to 0 V.
    # keithley_instrument.smua.source.levelv = 0.0

    # # Turn on the voltmeter on.
    # keithley_instrument.smub.source.output = keithley_instrument.smub.OUTPUT_ON

    # # Turn on the output source on.
    # keithley_instrument.smua.source.output = keithley_instrument.smua.OUTPUT_ON

    # for v in range(1, 10):

    #     value = v * 0.01

    #     logging.info(f"source v from channel A: {value=} [V]")
    #     keithley_instrument.smua.source.levelv = value

    #     time.sleep(stime)

    #     i_a = keithley_instrument.smua.measure.i()
    #     logging.info(f"measured i at channel A: {i_a=} [V]")
    #     # print(f"current measured at A: {i_a}")
        
    #     v_a = keithley_instrument.smua.measure.v()
    #     logging.info(f"measured v at channel A: {v_a=} [V]")
    #     # print(f"voltage measured at A: {v_a}")

    #     v_b = keithley_instrument.smub.measure.v()
    #     logging.info(f"measured v at channel B: {v_b=} [V]")
    #     # print(f"voltage measured at B: {v_b}")
        

    #     time.sleep(1)

    #     logging.info(f"after 1s delay measure:")

    #     i_a_2 = keithley_instrument.smua.measure.i()
    #     logging.info(f"measured i at channel A: {i_a_2=} [V]")
    #     # print(f"current measured at A: {i_a}")
        
    #     v_a_2 = keithley_instrument.smua.measure.v()
    #     logging.info(f"measured v at channel A: {v_a_2=} [V]")
    #     # print(f"voltage measured at A: {v_a}")

    #     v_b_2 = keithley_instrument.smub.measure.v()
    #     logging.info(f"measured v at channel B: {v_b_2=} [V]")
    #     # print(f"voltage measured at B: {v_b}")

    #     logging.info(f"{'='*5}")

    #     # tst_global = tst_global + 1
    
    # keithley_instrument.smua.source.output = keithley_instrument.smua.OUTPUT_OFF   # turn off SMUA
    # keithley_instrument.smub.source.output = keithley_instrument.smub.OUTPUT_OFF   # turn off SMUB

if __name__ == "__main__":
    
    # tst_global = 1

        # init logger
    format = "%(asctime)s: %(message)s"
    log_file_path = 'example.log'
    logging.basicConfig(format=format, level=logging.INFO,  
                        datefmt="%H:%M:%S", filename= log_file_path)

        # init the instrument handle
    # k = Keithley2600('USB0::0x05E6::0x2602::4522205::INSTR', visa_library = 'C:/windows/System32/visa64.dll')
    k = 2

    stime = 1 
    # keithely_actions_exp_1(k, 0.1) # stime [s]

    # print(f"{tst_global=}")

        # Input from the terminal

    # print(f"input somthing: ")

    # input_str = str(input())

    # if input_str == "main_stop":
    #     print(f"OK")
    # else:
    #     print(f"NOT OK")

    logging.info("Main    : Prepare measurement")
    stop_threads = False
    x = threading.Thread(target=keithely_actions_exp_2, args=(k, stime, lambda: stop_threads,))
    logging.info("Main    : Run measurement")
    x.start()

    while True:
        logging.info("Main    : inside the input inf loop")
        
            # input from terminal read-in
        print(f"input 'main_stop' or 'thread_stop': ")

        input_str = str(input())

        if input_str == "main_stop" and (stop_threads == True):
            break
            
        if input_str == 'thread_stop':        
            stop_threads = True

    logging.info("Main    : EXIT")










