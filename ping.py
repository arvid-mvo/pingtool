# OS: Ubuntu 20.04.4 LTS (Focial Fossa)
# Python: 3.8.10

from multiprocessing import Process, Queue
import multiprocessing
import subprocess
from pythonping import ping
from curses import wrapper
import curses
import time
import sys
from sys import platform
import pingutils
import math
import csv
import os
import traceback

# File with ip addresses to ping
ipaddress_filename = "ip_address.txt"

# Name of csv file to store ping response times
ping_response_times_csv = "ping_response_times.csv"
'''
ping_response_linux():

Args:
    queue: queue type object for storing ping responses
    command: command string for subprocess

This function gets the ping response using Linux ping command.
This function will run if the OS running the program is Linux.
'''
def ping_response_linux(queue, command=[]):
    while True:
        #out = subprocess.check_output(command)
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        out,err = p.communicate()
        out = out.decode()
        #print(out)
        #print("\n\n\n\n")
        out_list = out.split("\n")  
        queue.put(out_list[1])
        time.sleep(1)
        #summary_statistics = []
        out_list_count = 0
        '''
        for item in out_list:
            if item == '':
                #print(out_list[list_count+1:len(out_list)])
                ping_statistics = ""
                temp = out_list[out_list_count+2:len(out_list)]
                for item_temp in temp: 
                    ping_statistics = ping_statistics + item_temp + "\n"
                print(ping_statistics)
                queue.put(ping_statistics)
                break
            out_list_count = out_list_count + 1
        '''
        #for item in summary_statistics:
            #print(item)

        #time.sleep(1)

'''
ping_response_win():

Args:
    queue: queue type object for storing ping responses.
    ip: ip address to ping.
    packet_size: size of packet to use in ping.
    packet_count: how many packets to send.
    
This function gets the ping response using the library pythonping.
This function will run if the OS running the program is windows.
'''
def ping_response_win(queue, ip, packet_size, packet_count=1):
    while True:
        ping_response = ping(ip, size=packet_size, count=packet_count, verbose=False)
        for item in ping_response:
            out = item
        
        queue.put(out)
        time.sleep(1)

'''
screen()

Args:
    stdscr:
    queues:
    ip_addresses:
    packet_size:

This function creates the screen to dislay the ping responses using the curses library.
'''
# Curses screen to display ping response
def screen(stdscr, queues, ip_addresses, packet_size, csv_writer, fp):
    #curses.newwin(nlines:height, ncols:width, begin_y: topside_y_coordinate, begin_x: leftside_x_coordinate)
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    # List of windows
    win_list = []

    # List which contains row position for each window which determines the position to start printing messages
    row_pos_list = []

    # Max height and width of the screen
    # height = rows = y
    # width = columns = x
    screen_maxheight, screen_maxwidth = stdscr.getmaxyx()
    #print(f"{screen_maxheight}            {screen_maxwidth}")
    
    # General parameters
    beginx = beginy = 0 # x and y coords for where to position windows within the screen
    if platform == "win32":
        window_width = 55 # window width
    else:
        window_width = 65
    window_height = 0 # window height
    window_height_adjust = 5 # adjust window height when creating new windows
    window_spacing = 5 # horizontal spacing between windows
    row_spacing = 2 # spacing between rows
    row_start = 2 # row position in a window where to begin printing messages

    # Calculate how every window is going to fit on the screen.
    # The number of windows = number of ip addresses to ping.
    # First we calculate how many windows we can fit on one row across the screen which is a function of:
    #   screen max width
    #   window width
    #   window spacing    
    windows_per_row = pingutils.windows_per_row(screen_maxwidth, window_width, window_spacing)
    #print(f"windows per row: {windows_per_row}")
  
    # Calculate number of rows needed to fit all windows.
    num_rows = math.ceil(len(ip_addresses)/windows_per_row)
    #print(f"number of rows: {num_rows}")
    # Window height will be based on number of rows.
    window_height = int(screen_maxheight/num_rows)
    
    # Begin to place each window on the screen.
    for win in range(len(ip_addresses)):
        # This if statement determines when we have to place a new row of windows on the screen.
        # Adjust beginy accordingly and set beginx = 0.
        if (beginx + window_width + window_spacing) > screen_maxwidth:
            beginy = beginy + window_height + row_spacing
            beginx = 0
        try:
            #print(f"{window_height}  {window_width}  {beginy}  {beginx}")
            # Create window and place on screen.
            # Catch any exception, print error message and exit program.
            win = curses.newwin(window_height-window_height_adjust, window_width, beginy, beginx)
        except:
            print("Please check placement of windows. Exiting...")
            sys.exit()
        # Append created windows to a list
        win_list.append(win)
        row_pos_list.append(row_start)
        # Update beginx
        beginx = beginx + window_width + window_spacing

    ip_addresses_temp = ip_addresses
    #ip_addresses_temp.insert(0, "data_value")
    csv_writer.writerow(ip_addresses_temp)
    #fp.flush()
    #exit()
    
    #ignore = stdscr.getch()
    #sys.exit()
    #header = f"PING ipaddr (ipaddr) {packet_size} bytes of data\n\n"
    data_value = 1
    try:
        for win_index, win in enumerate(win_list):
            win.addstr(f"PING {ip_addresses[win_index]} with {packet_size} bytes of data\n\n", curses.color_pair(1)) 
            win.refresh()      
        #win.addstr(header)
        to = 0
        while True:
            ping_response_time_list = [] 
            for queue_index, queue in enumerate(queues):
                if queue.empty():
                    ping_response_time_list.append("")
                    continue
                win = win_list[queue_index]
                try:
                    ping_response = queue.get()
                    #print(ping_response)
                    '''
                    Extract ping time from ping response.
                    Store ping time in csv file.
                    '''
                    #try:
                    ping_response_time = pingutils.get_ping_time(str(ping_response))
                    #except Exception:
                    #    traceback.print_exc()
                    #    break
                    ping_response_time_list.append(ping_response_time)

                    win.addstr(row_pos_list[queue_index], 0, f"{ping_response}")
                    row_pos_list[queue_index] = row_pos_list[queue_index] + 1
                except:
                    row_pos_list[queue_index] = 2
                    win.clear()
                    win.addstr(f"PING {ip_addresses[queue_index]} with {packet_size} bytes of data\n\n", curses.color_pair(1)) 
                    #win.addstr(header)
                win.refresh()
            fp.flush()
            #ping_response_time_list.insert(0, data_value)
            csv_writer.writerow(ping_response_time_list)
            data_value = data_value + 1
            time.sleep(1)
            
            to = to + 1
            #if to == 120:
             #   break
        
        #ignore = stdscr.getch()

    finally:
        curses.endwin()

'''
launch_process()

Args:
    platform:
    ip_addresses:
    packet_size:
    queues:
    procs:

This function launches a process to ping every ip addresses in the list of ipaddresses.
The process is appended to a list of processes.
'''
# Launches processes responsible for pining ip addresses and storing response into a queue
def launch_process(platform, ip_addresses, packet_size, queues, procs):
    for ip in ip_addresses:
        #command = ["ping", "-s", str(packet_size), "-c", str(count), ip]
        #command = ["ping", "-l", str(packet_size), "-n", "1", ip]
        my_queue = Queue()
        
        if platform == "linux":
            command = ["ping", "-s", str(packet_size), "-c", "1", ip]
            args = (my_queue, command)
            target = ping_response_linux
        else:
            args = (my_queue, ip, int(packet_size))
            target = ping_response_win
        
        proc = Process(target=target, args=args)
        queues.append(my_queue)
        procs.append(proc)
        proc.start()

'''
Main Process
'''
def main():
    
    #ip_addresses = ["172.17.106.1", "172.17.106.2", "172.17.106.3", "172.17.106.4", "172.17.106.4"]    
    #ip_addresses = ["172.20.0.10", "172.20.0.11", "172.20.0.10", "172.20.0.11", "172.20.0.10",  "172.20.0.11", "172.20.0.10"]    
    #ip_addresses = ["172.20.0.10", "172.20.0.11", "172.20.0.65", "172.20.0.66", "172.20.0.67", "172.20.0.68"]
    
    while True:
        # Ask user to either enter ip addresses manually or read a file with ipaddresses
        print("Please select option 1 or 2 below:")
        print("1. Enter ip addresses manually?")
        print("2. Read text file with ip addresses?")
        option = input("")
        
        if int(option) == 1:
            ip_addresses = pingutils.read_ipaddress_manually()
            break
        elif int(option) == 2:
            ip_addresses = pingutils.read_ipaddress_file()    
            break
        else:
            print("Invalid option. Please select again.")
            print("\n\n")

    #ip_addresses = read_ipaddress_manually()
    #ip_addresses = ["172.17.106.2"]
    print("\nPinging the following ip addresses:")
    for idx, ip_addr in enumerate(ip_addresses):
        print(f"{idx + 1}. {ip_addr}")

    input("Press enter to continue")
    '''
    # Enter packet size
    # Default is 56 bytes
    packet_size = input("\nEnter packet size (default is 56 bytes):")
    '''
    packet_size = 56
    
    # List for processes
    procs = []
    # List for queues
    queues = []
    
    # Save ping response time to csv file
    fp = pingutils.setup_save_response_csv(ping_response_times_csv)
    csv_writer = csv.writer(fp)

    # Use linux ping command to read output of ping if running on a linux machine
    # Use library pythonping if running on a windows machine
    if platform == "linux":
        launch_process("linux", ip_addresses, packet_size, queues, procs)
    elif platform == "win32":
        launch_process("win32", ip_addresses, packet_size, queues, procs)
    else:
        print(f"Sorry, your current platform {platform} is not supported.")
        sys.exit()

    # Call plot in a separate process to plot ping results
    target = pingutils.plot
    proc = Process(target=target)
    proc.start()

    try:
        wrapper(screen, queues, ip_addresses, packet_size, csv_writer, fp)        
        '''
        while True:
            for q in queues:
                if q.empty():
                    continue
                #print("Am I printing ??")
                print(q.get())
        '''
    except KeyboardInterrupt:
        print("Closing queues....")
        for q in queues:
            q.close()
        print("Terminating ping processes....")
        for proc in procs:
            proc.terminate()
        print("Exiting program.....")

if __name__ == "__main__":
    
    # windows only
    if platform == "win32":
        multiprocessing.freeze_support()
    
    main()
    
