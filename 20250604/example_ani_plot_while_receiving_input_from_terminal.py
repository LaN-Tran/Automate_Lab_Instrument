"""
    Reference:
        [1] the code below is the exact copy from: https://stackoverflow.com/questions/53060711/matplotlib-cant-manipulate-plot-while-script-is-waiting-for-input
"""

import queue
import numpy as np  # just used for mocking data, not necessary
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
animation_queue = queue.Queue()
update_rate_ms = 50

xdata = np.linspace(0, 2 * np.pi, 256)
ydata = np.sin(xdata)
zdata = np.cos(xdata)

def normal_plot_stuff():
    """Some run of the mill plotting."""
    ax.set_title("Example Responsive Plot")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.plot(xdata, ydata, "C0", label="sin")
    ax.plot(xdata, zdata, "C1", label="cos")
    ax.legend(loc="lower right")

def animate(_, q):
    """Define a callback function for the matplotlib animation. 
       This reads messages from the queue 'q' to adjust the plot.
    """
    while not q.empty():
        message = q.get_nowait()
        q.task_done()
        x0 = float(message)
        ax.set_xlim([x0, x0 + 5])

def mainloop():
    """The main loop"""
    _ = FuncAnimation(fig, animate, interval=update_rate_ms, fargs=(animation_queue,))
    normal_plot_stuff()
    plt.show(block=False)
    while True:
        try:
            uinput = input("Type starting X value or 'q' to quit: ")
            if uinput == "q":
                break
            animation_queue.put_nowait(float(uinput))
        except ValueError:
            print("Please enter a valid number.")

mainloop()