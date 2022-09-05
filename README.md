# ping_test

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
  
Create and activate virtual environment which will be stored in venv:
  `python -m venv venv`

Activate the virtual environment:
  `source venv/bin/activate`
  
or on windows:
   `venv/Scripts/activate
   
Install the above modules

Run script:
  `python ping.py`
