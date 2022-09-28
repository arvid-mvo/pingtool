# OS: Ubuntu 20.04.4 LTS (Focial Fossa)
# Python: 3.8.10

from multiprocessing import Process, Queue
import subprocess
from pythonping import ping
from curses import wrapper
import curses
import time
import sys
from sys import platform
import pingutils

# File with ip addresses to ping
ipaddress_filename = "ip_address.txt"

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
def screen(stdscr, queues, ip_addresses, packet_size):

    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    # List of windows
    win_list = []

    # List which contains row position for printing messages in each window
    row_pos_list = []

    # Max rows and columns of the screen
    max_rows, max_cols = stdscr.getmaxyx()

    begin_x = begin_y = 0
    #curses.newwin(nlines:height, ncols:width, begin_y: topside_y_coordinate, begin_x: leftside_x_coordinate)
    
    message_width = 65
    win_offset = 70
    row_start = 2

    # length of queues = number of ip addresses to ping = number of windows to create
    for win in range(len(queues)):
        try:
            win = curses.newwin(max_rows, message_width, begin_y, begin_x)
        except:
            print("Please full screen console window or ping fewer ip addresses.")
            sys.exit()
        win.clear()
        win_list.append(win)
        row_pos_list.append(row_start)
        begin_x = begin_x + win_offset
    
    #header = f"PING ipaddr (ipaddr) {packet_size} bytes of data\n\n"
    try:
        for win_index, win in enumerate(win_list):
            win.addstr(f"PING {ip_addresses[win_index]} with {packet_size} bytes of data\n\n", curses.color_pair(1)) 
            win.refresh()      
        #win.addstr(header)
        while True: 
            for queue_index, queue in enumerate(queues):
                if queue.empty():
                    continue
                win = win_list[queue_index]
                try:
                    win.addstr(row_pos_list[queue_index], 0, f"{queue.get()}")
                    row_pos_list[queue_index] = row_pos_list[queue_index] + 1
                except:
                    row_pos_list[queue_index] = 2
                    win.clear()
                    win.addstr(f"PING {ip_addresses[queue_index]} with {packet_size} bytes of data\n\n", curses.color_pair(1)) 
                    #win.addstr(header)
                win.refresh()
            time.sleep(1)
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

    ip_addresses = []    
    
    while True:
        # Ask user to either enter ip addresses manually or read a file with ipaddresses
        #print("Please select option 1 or 2 below:")
        print("1. Enter ip addresses manually?")
        print("2. Read text file with ip addresses?")
        option = input("Enter either option 1 or 2: ")

        print("\n")
        
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

    # Enter packet size
    # Default is 56 bytes
    packet_size = input("\nEnter packet size (default is 56 bytes):")
    #packet_size = 56
    
    # List for processes
    procs = []
    # List for queues
    queues = []
    
    # Use linux ping command to read output of ping if running on a linux machine
    # Use library pythonping if running on a windows machine
    if platform == "linux":
        launch_process("linux", ip_addresses, packet_size, queues, procs)
    elif platform == "win32":
        launch_process("win32", ip_addresses, packet_size, queues, procs)
    else:
        print(f"Sorry, your current platform {platform} is not supported.")
        sys.exit()

    try:
        wrapper(screen, queues, ip_addresses, packet_size)        
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
    
