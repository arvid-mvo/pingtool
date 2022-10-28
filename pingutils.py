import ipaddress
import sys
import math
from sys import platform
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def read_ipaddress_file():

    ipaddress_filename = input("Please enter path to ip address file:\n")
    # Read file with IP addresses
    print(f"Reading file {ipaddress_filename}\n")
    try:
        fp = open(ipaddress_filename, "r")
    except FileNotFoundError:
        print(f"Error: Please create a file '{ipaddress_filename}' and enter the ip addresses you wish to ping.")
        sys.exit()
    
    ip_addr_list = []
    # Get ip address and store in list
    for ip_addr in fp:
        # Check for comments
        # Comments begin with #
        if "#" in ip_addr.rstrip():
            continue
        # Check for valid ip addresses.
        # If any ipaddress is not valid, exit program
        try:
            ipaddress.ip_address(ip_addr.rstrip())
            ip_addr_list.append(ip_addr.rstrip())
        except ValueError:
            print(f"Error: IP address '{ip_addr.rstrip()}' was not entered correctly. Exiting..... ")
            sys.exit()
    # Close file
    fp.close()

    # Return list if ip addresses
    return ip_addr_list

def read_ipaddress_manually():
    
    ip_addr_list = []
    ip_addr = ""
    
    print("Please enter ip addresses. Type done when finished.")
    while True:
        ip_addr = input()
        if ip_addr == "done":
            break
        try:
            ipaddress.ip_address(ip_addr.rstrip())
            ip_addr_list.append(ip_addr.rstrip())
        except ValueError:
            print("Error: Invalid ip enetered.")

    return ip_addr_list

def windows_per_row(screen_maxwidth, window_width, window_spacing):
    
    windows_per_row = screen_maxwidth/(window_width + window_spacing)
    if (math.ceil(windows_per_row) * (window_width + window_spacing)) > screen_maxwidth:
        windows_per_row = int(windows_per_row)
    else:
        windows_per_row = math.ceil(windows_per_row) 

    return windows_per_row

def get_ping_time(response):
    if response == "Request timed out":
        return ""
    else:
        response = response.split(" ")
        response_time = response[-1]
        response_time = response_time.split("ms")
        return response_time[0]

def setup_save_response_csv(filename):
    # get current working directory
    cwd = os.path.abspath(os.getcwd())
    # check if os is win or linux
    if platform == "win32":
        path = (cwd + "\\" + filename)
    else:
        path = (cwd + "/" + filename)

    if os.path.exists(path):
        os.remove(path)
        f = open(path, "a")
    else:
        f = open(path, "a")

    return f

def animate(i):
    x_data = []
    y_data_list = []

    while True:
        try:
            data = pd.read_csv("ping_response_times.csv")
            break
        except FileNotFoundError:
            continue
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

def plot():
    #animate(1)
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.tight_layout()
    plt.show()
