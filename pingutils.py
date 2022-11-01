import ipaddress
import sys
from sys import platform
import math
import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import tkinter as tk
from tkinter import filedialog

'''
read_ipaddress_file():

Args:
    have_display: Bool type varialble which states whether a display is present or not.
                  True: display present.
                  False: display not present.

This function reads a text file with ipaddresses to ping.
The text file is formatted as follows:
    172.17.106.1
    172.17.106.2
    172.17.106.3
    #172.17.106.4
    #172.17.106.5
    172.17.106.6
Any ipaddress leading with # character is considered a comment and is ignored.
The function also checks whether the ipaddresses entered are correct or not.
Upon encountering an invalid ipaddress, the program will Exit. Fix the wrong ipaddress and run program again.

The function will open a window for the user to navigate to the ipaddress text file they wish to open.
This will only be done if the program is being ran with a display present.
Example:
        Linux os with display present
        Windows os with display present
In a situation where there is no display present, if using ssh, the user is required to enter the path to the ipaddress text file manually.

Return Value:
    ip_addr_list: List of ipaddresses to ping
'''
def read_ipaddress_file(have_display):

    # Open window to read text file with ipaddresses.
    # This window will only open if a graphical display is present on linux.
    # For windows, the graphical display will be present.
    #
    # If no graphical display is present, we maybe running the pingtool from ssh.
    # In that case, enter the path to ipaddresses text file manually.
    if (platform == "linux" and have_display) or platform == "win32":
        root = tk.Tk()
        root.withdraw()
        ipaddress_filename = filedialog.askopenfilename()
    else:
        ipaddress_filename = input("Please enter path to ip address file:\n")

    # Read file with ipaddresses.
    # If file not found, program will Exit.
    #   Create file with ipaddress to ping.
    print(f"Reading file {ipaddress_filename}\n")
    try:
        fp = open(ipaddress_filename, "r")
    except FileNotFoundError:
        print(f"Error: Please create a file '{ipaddress_filename}' and enter the ip addresses you wish to ping.")
        sys.exit()
    
    # Get ipaddress and store in list.
    ip_addr_list = []
    for ip_addr in fp:
        # Check for comments.
        # Comments begin with #
        if "#" in ip_addr.rstrip():
            continue
        # Check for valid ipaddresses.
        # If any ipaddress is not valid, exit program.
        try:
            ipaddress.ip_address(ip_addr.rstrip())
            ip_addr_list.append(ip_addr.rstrip())
        except ValueError:
            print(f"Error: IP address '{ip_addr.rstrip()}' was not entered correctly. Exiting..... ")
            sys.exit()
    # Close file.
    fp.close()

    # Return list if ipaddresses.
    return ip_addr_list

'''
read_ipaddress_manually():

Args:

This function reads ipaddresses entered by the user manually, one by one.
The function also checks whether the ipaddresses entered are correct or not.

The user types 'done' when they are finished entering ipaddress to ping.

Return Value:
    ip_addr_list: List of ipaddresses to ping
'''
def read_ipaddress_manually():
    
    ip_addr_list = []
    ip_addr = ""
    
    print("\nPlease enter ip addresses. Type done when finished.")
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

'''
windows_per_row():

Args:
    screen_maxwidth: Maximum width of the curses screen.
    window_width: Width of the window where messages are displayed.
    window_spacing: Spacing between each window.

This function calcuates how many windows we can fit on one row across the curses screen given the follwing:
    1. Maximum width of the curses screen (screen_maxwidth).
    2. Wdith of the window (window_width).
    3. Spacing between each window on a row (window_spacing).

Return Value:
    windows_per_row: Number of windows that can fit across the curses screen.
'''
def windows_per_row(screen_maxwidth, window_width, window_spacing):
    
    windows_per_row = screen_maxwidth/(window_width + window_spacing)
    if (math.ceil(windows_per_row) * (window_width + window_spacing)) > screen_maxwidth:
        windows_per_row = int(windows_per_row)
    else:
        windows_per_row = math.ceil(windows_per_row) 

    return windows_per_row

'''
get_ping_time()

Args:
    response: ping response after pinging a ipaddress.

This function gets the ping response time from the response message after a ipaddress is pinged.

On windows, a successfull ping resposne is as follows:
    Reply from 172.17.106.6, 84 bytes in 1.32ms
The function will get 1.32 ms as the ping response time from the response message.
Pythonping library is used to perform ping command on windows.

On Linux

Return Value:
    ping_response_time: Response time of a ping command.
'''
def get_ping_time(response):
    if platform == "win32":
        if response == "Request timed out":
            return ""
        else:
            response = response.split(" ")
            response_time = response[-1]
            response_time = response_time.split("ms")
            return response_time[0]

    else:
        response_list = response.split(" ")
        if response_list[-1] != "ms":
            return ""
        else:
            response_time = response_list[len(response_list) - 2]
            response_time = response_time.split("=")
            return response_time[1]
'''
setup_save_response_csv():

Args:
    filename: Name of csv file the program writes ping response times to.

This function opens a csv file (ping_response_times.csv) in append mode for writing ping response times to.

Return Value:
    f: File pointer to ping response time csv file.
'''
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

'''
animate():

Args:

This function plots the ping response times from every ipaddress pinged by the program.

The ping response times are read from the csv file: ping_response_times.csv

Return Value:
'''
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

'''
plot()

Args:

This function uses the matplotlib FuncAnimation to call the animate function every second to update the ping reponse time plot in real time.

Return Value:
'''
def plot():
    #animate(1)
    ani = FuncAnimation(plt.gcf(), animate, interval=1000)

    plt.tight_layout()
    plt.show()
