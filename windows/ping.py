# OS: Ubuntu 20.04.4 LTS (Focial Fossa)
# Python: 3.8.10

from multiprocessing import Process, Queue
import subprocess
from curses import wrapper
import curses
import time
import ipaddress
import sys

def ping_response(queue, command=[]):
    while True:
        #out = subprocess.check_output(command)
        p = subprocess.Popen(command, stdout=subprocess.PIPE)
        out,err = p.communicate()
        out = out.decode()
        #print(out)
        #print("\n\n\n\n")
        out_list = out.split("\n")  
        queue.put(out_list[2])
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

def main(stdscr, queues, ip_addresses, packet_size):
    
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
        win = curses.newwin(max_rows, message_width, begin_y, begin_x)
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

if __name__ == "__main__":

    ip_addresses = []    
    
    while True:
        # Ask user to either enter ip addresses manually or read a file with ipaddresses
        print("Please select option 1 or 2 below:")
        print("1. Enter ip addresses manually?")
        print("2. Read text file with ip addresses?")
        option = input()

        print("\n")
        
        if int(option) == 1:
            ip_addresses = read_ipaddress_manually()
            break
        elif int(option) == 2:
            ip_addresses = read_ipaddress_file()    
            break
        else:
            print("Invalid option. Please select again.")
            print("\n\n")

    print("\nPinging the following ip addresses:")
    for idx, ip_addr in enumerate(ip_addresses):
        print(f"{idx + 1}. {ip_addr}")

    exit(0)
    # Enter packet size
    # Default is 56 bytes
    packet_size = input("\nEnter packet size(bytes):")

    # List for processes
    procs = []
    # List for queues
    queues = []
    
    #ip_addr = ["172.17.103.13", "172.17.103.14", "172.17.103.11"]
    #ip_addr = ["172.17.103.13", "172.17.103.14", "172.17.106.1"]

    for ip in ip_addresses:
        #command = ["ping", "-s", str(packet_size), "-c", str(count), ip]
        command = ["ping", "-l", str(packet_size), "-n", "1", ip]
        my_queue = Queue()
        proc = Process(target=ping_response, args=(my_queue, command))
        queues.append(my_queue)
        procs.append(proc)
        proc.start()

    try:
        wrapper(main, queues, ip_addresses, packet_size)
        '''
        while True:
            for q in queues:
                if q.empty():
                    continue
                
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

