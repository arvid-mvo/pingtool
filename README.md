# ping_test

**IMPORTANT** !!!
Still in development with bugs to be fixed and other features to add.

Python tool for viewing the output of a ping command on multiple ip addresses at the same time.

The tool uses the curses library in python to generate a screen where the ping results are displayed. Multiprocessing is used to get the output of each ping result which is sent to the curses screen.

Example output of ping_test:
![Screenshot from 2022-09-05 19-46-36](https://user-images.githubusercontent.com/101291172/188507322-0cb28f2f-6c22-42da-9a34-d305c4ecdf3d.png)


Version for both windows and Linux.

Python Version 3.8.10

## Modules
- Multiprocessing (Process, and Queue)
- subprocess
- curses
- curses (wrapper)
- time
- ipaddress
- sys
- pythonping (for windows only)

# Python Script

Clone repository:

  `git clone https://github.com/maneskull/ping_test.git`
  
Change directory to either Linux or Windows:

  `cd linux`

or

  `cd windows`
  
Create virtual environment (venv):

`python -m venv venv`

Activate the virtual environment (venv):

`source venv/bin/activate`
  
or on windows:

`venv/Scripts/activate`
   
Install the above modules

Run script:

`python ping.py`

## Operation

When the script is executed, it prompts the user to enter the IP addresses they wish to ping either manually or reading from a file. Basic checking is done on the ip addresses entered to verify they are of correct format and the script will notfiy the user of any errors.

Once the IP addresses has been entered, the script verifys to the user the ip addresses to ping and then prompts the user to enter the packet size. Once the packet size is entered, the script begins to display the output of the ping results to the curses screen.

Example output of the execution of the script:
![Screenshot from 2022-09-06 13-49-27](https://user-images.githubusercontent.com/101291172/188652472-97abc5e3-47f2-41d2-bc6f-87bc3ce1614b.png)


Please note there are some differences in the Linux and Windows versions and some issues which are to be fixed.
