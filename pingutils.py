import ipaddress
import sys

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
