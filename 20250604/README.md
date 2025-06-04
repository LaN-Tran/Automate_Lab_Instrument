# Folder description

- 1. **auto_lab_exp_1.py** an application which runs measurement and live-update from the measurement in animated figure (with function `keithely_actions_exp_2` and `main`). The function `keithely_actions_exp_1` is used to test only the real measurement with Keithley instrument, to see it works well in python file instead of jupyternotebook. 

- 2. **example_ani_plot_while_receiving_input_from_terminal.py**: copy of an example where `input()` python can be used in parallel with other thread.

# Report

- NOTICE: in this context `main` means the main program which creates other thread to handle task in parallel with `main`.
  
# Problem

- 1. wherever the `input()` function is run (within the `main` or thread created from other functions), it blocks all the threads from continuing until the user input something. 

- 2. Can not plot animated figures (live update data from measurement) in a thread, except for `main`.

# Solution

-