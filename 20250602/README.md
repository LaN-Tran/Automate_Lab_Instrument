# Folder description

- 1. **intro_lab_auto.ipynb** follows the intro steps in videos **../README.md** - section **Good introduction videos (References)**

# Report

- in **../2600BS-901-01F_2600B_Reference_Aug2021.pdf** - page (2-50)- section SPEED:

  - _reading rate_ is determined by the _integration time_ (i.e _measurment aperture_, time step of the instrument ADC).

- good reference: 

  - [1] [Tu Graz- pyvisa](http://lampz.tugraz.at/~hadley/semi/ch9/instruments/Keithley26xx/KeithleyV15.py)

  - [2] [Keithley 2600 python library](https://keithley2600.readthedocs.io/en/stable/api/keithley_driver.html) 
    
    - [2.1] [keithley 2600 soruce code](https://github.com/OE-FET/keithley2600/blob/master/keithley2600/keithley_driver.py#L173)

  - [3] [NI-VISA, PyVisa](https://pyvisa.readthedocs.io/en/1.8/getting_nivisa.html)

  - [4] [Keithley TSP Toolkit](https://tm-devices.readthedocs.io/latest/reference/tm_devices/drivers/source_measure_units/smu26xx/smu2602b/)
  
# Problem

See section **Solution** below to have the corresponding answer to each problem

- 1. after installing `pyvisa` package, there error: `ValueError: Could not locate a VISA implementation. Install either the IVI binary or pyvisa-py.` when running

```
rm = pyvisa.ResourceManager()
print(rm.list_resources())
```

- 2. using the **LAN connection** to Keithley 2602B has problem: the **NI-MAX app** - **My system** - **Devices and interfaces** detects **NOTHING** OR/AND the code below:

```
rm = pyvisa.ResourceManager()
print(rm.list_resources())
```
return **NOTHING**

- 3. **VisaIOError: VI_ERROR_TMO (-1073807339): Timeout expired before operation completed.** when query "*IDN?\n" in **NI-MAX app** - **My system** - **Devices and interfaces** - the connected device (for example, `USB0::0x05E6::0x2602::4522205::INSTR`) - **Open VISA test Panel** OR/AND the code below:

```
smu = rm.open_resource('USB0::0x05E6::0x2602::4522205::INSTR')
print(smu.query("*IDN?"))
```

# Solution

- 1. check whether any VISA server/backend available:

  - step 1: in the terminal (git bash in VScode), run: `pyvisa-info`, at the end of the message if see:

  ```
  Backends:
   ivi:
      Version: 1.15.0 (bundled with PyVISA)
      Binary library: Not found
  ```

  That means there is no VISA backend installed

  - step 2: install VISA backend from NI-VISA

  - step 3: repeat step 1, the message should be:

  ```
  Backends:
   ivi:
      Version: 1.15.0 (bundled with PyVISA)
      #1: C:\windows\System32\visa32.dll:
         found by: auto
         architecture:
            ('x86', 64)
         Vendor: National Instruments
         Impl. Version: 26215168
         Spec. Version: 7340544
      #2: C:\windows\System32\visa64.dll:
         found by: auto
         architecture:
            ('x86', 64)
         Vendor: National Instruments
         Impl. Version: 26215168
         Spec. Version: 7340544
  ```

- 2. change **LAN connection** to **USB connection** (in the back of the Keithley 2602B, usb symbol).  

- 3. Restart (TURN OFF, then ON) the Keithley 2602B again. (? is it because the LAN setting in the beginning raises the **Problem** - **3.** above)
