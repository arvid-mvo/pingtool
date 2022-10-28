import random
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('fivethirtyeight')


def animate(i):
    x_data = []
    y_data_list = []

    data = pd.read_csv("ping_response_times.csv.csv")
    #print(data.columns)
    #print(data)
    for i in range(len(data[data.columns[0]])):
        x_data.append(i)

    #print(len(x))
    for col in data.columns:
        y_data_list.append(data[col])
        #print(len(data[col]))

    
    plt.cla()
    #print(len(x_data))
    #print(len(y_data_list[0]))
    #print(len(x_data))
    for i, y in enumerate(y_data_list):
        plt.plot(x_data, y, linewidth=2, label=data.columns[i])
    
    plt.legend(loc="upper left")
    plt.xlabel("Count (s)")
    plt.ylabel("Ping Response Time (ms)")
    plt.title("Ping Response Time (ms) from Pinging IP Addresses using the Ping Tool Program.")
    #plt.cla()
    #plt.plot(x_vals, y_vals)
    

#animate(1)
ani = FuncAnimation(plt.gcf(), animate, interval=1000)

plt.tight_layout()
plt.show()
