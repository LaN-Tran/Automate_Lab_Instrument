import csv
import pandas as pd
import matplotlib.animation as animation
import matplotlib.pyplot as plt

def read_from_file_and_plot (_, file_path):
    # global file_path
    data = pd.read_csv(file_path)
    x = data['time']
    y = data['i']

    plt.cla()
    plt.plot(x, y)



file_path = "C:/Users/20245580/LabCode/Automate_Lab_Instrument/20250605/output_exp3.csv"
    
ani = animation.FuncAnimation(plt.gcf(), read_from_file_and_plot, interval= 1000, fargs= (file_path, ))
plt.show()

