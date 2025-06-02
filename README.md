# How to automate all types of Lab instruments 

Lab instruments, for example, are SMUs, Power Generator, Oscilloscope from different manufacturer (e.g NI, R&S, Tek, Keysight, etc)

## Good introduction videos (References)

[1] [General view of how to automate any lab instrument](https://youtu.be/XhUGKqORBGM?si=BX07TIo6VFKKHIwB)

[2] [More introduction about VISA (Virtual Instrument Software Architecture), pyvisa](https://www.youtube.com/watch?v=1HQxnz3P9P4)

## What are requirements to use python script to communicate with any Lab instrument?

- refer to [1] (above)

- 1. The lab instrument needs to have port supported by VISA: such as LAN, GPIB, USB.

- 2. In the computer which runs the python script to interact with the instrument: 

  - 2.1 Install VISA driver (free driver) from NI (National Instrument) (a backend)

  - 2.2 Install pyvisa package (a library to communicate with backend)

  - 2.3 Search for instrument reference document to know what types of commands should be send through the pyvisa to communicate with the instrument.

    - 2.3.1 For example, in case of Keithley 2602B SMU, the reference manual is in the [link](https://www.tek.com/en/keithley-source-measure-units/smu-2600b-series-sourcemeter-manual-8); or [their python library](https://pypi.org/project/keithley2600/), they say the **TSP** commands are used to communicate with their Keithley 2600B series instruments. That means we just copy paste the needed **TSP** commands in their reference manual into the pyvisa command to communicate (i.e using the instrument) through python script in the computer.

    - 2.3.2 refer to [2] (above), **SCPI** command works for any instrument through the VISA driver. That means, besides **TSP** commands of Keithley 2600B series, **SCPI** could be used as an alternative. 