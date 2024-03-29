# pingtool

Pingtool is a program used to ping multiple ip address at the same time. It displays the output of multiple ping commands on the same screen. It also generates a plot of the ping response time for each ip address which updates in real time.

Pingtool was developed in **Python 3.8.10** and **3.10.6** for **Linux** and **Windows** respectively.

## Main Modules
- Multiprocessing
- subprocess
- pythonping (windows only)
- curses
- pandas
- matplotlib
- tkinter
- ipaddress

# Using pingtool
Clone repository:

&nbsp;&nbsp;&nbsp;&nbsp;`git clone https://github.com/maneskull/pingtool.git`

Create virtual environment (venv):

&nbsp;&nbsp;&nbsp;&nbsp;`cd pingtool`

&nbsp;&nbsp;&nbsp;&nbsp;`mkdir venv`

&nbsp;&nbsp;&nbsp;&nbsp;`python -m venv venv`

Activate virtual environment (venv):

&nbsp;&nbsp;&nbsp;&nbsp;Linux:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`source venv/bin/activate`

&nbsp;&nbsp;&nbsp;&nbsp;Windows:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`venv\Scripts\activate`
 
Install main modules. Some additional modules will need to be installed.

Run script:

&nbsp;&nbsp;&nbsp;&nbsp;`python ping.py`

# Operation
<p align="center" width="100%">
    <img width="698" alt="flow_chart" src="https://user-images.githubusercontent.com/101291172/199759577-f97ae49c-5752-4322-a6b1-e0f327919b2b.png">
    <p align="center">Figure 1: Simplified flow chart showing the operation of the pingtool program.</p>
</p>
 

The flow chart in fig. 1 shows a simplified operation of the pingtool program which is further discussed in the following sections.

## Input Option
When pingtool starts, it prompts the user to enter either option 1 or option 2 as depicted in fig. 2 below.

<p align="center" width="100%">
    <img width="596" alt="img1" src="https://user-images.githubusercontent.com/101291172/199762806-c30cbdf5-a45b-4ff0-8cc9-37db0eb93f24.png">
    <p align="center">Figure 2: pingtool prompting the user to select either option 1 or option 2.</p>
</p>

If option 1 is selected, the ip addresses are entered manually line by line. The user types “done” when they are finished.

If option 2 is selected, a text file with the ip addresses can be loaded. If the pingtool program is ran in an environment with a display present, a window will open which allows the user to navigate to the text file. If no display is present, the user has to enter the full path to the text file. The program checks for any file errors or issues with the file and exits if necessary. The ip addresses in the text file should be listed one by one separated by a new line. Any line that starts with “#” is considered a comment and is ignored by the program. The file “ip_address.txt” shows an example of how the text file should be formatted.

In both cases for options 1 and 2, the program checks for valid ip address entered. If it encounters an invalid ip address, it notifies the user and is asked to enter it again.

## Enter Packet Size

After the user specifies the ip addresses they wish to ping, they are prompted to enter the packet size. The default size is 56 bytes and only integers are allowed. After the packet size is entered, the program shows the list of ip addresses it is going to ping along with the packet size and prompts the user to press enter to continue. This is depicted in fig. 3 below.

<p align="center" width="100%">
    <img width="576" alt="img2" src="https://user-images.githubusercontent.com/101291172/199763731-7f47baeb-db40-4549-a43b-0f6ef1871908.png">
    <p align="center">Figure 3: pingtool showing ip addresses to be pinged.</p>
</p>

Once the user presses enter, the pingtool begins displaying the output of ping responses.

## Display

After the ip addresses to be pinged are specified, the screen shows the ping responses from each ping in windows laid out across the screen. The following happens:

Multiple concurrent ping processes runs which pings the ip addresses specified by the user. There is one process for each ip address to be pinged, Ex: 4 ip = 4 ping processes. This is handled by the multiprocessing library. The ping response from each ping in stored in a queue.

While the concurrent ping processes are pinging the ip address, the main process configures and opens up a curses screen to display the results of the ping response for each ip address. The curses library supplies a terminal-independent screen painting and keyboard handling facility for text based terminals [1].

The curses terminal screen is configured with multiple windows where each window contains the ping response from each ip address pinged (number of windows = number of ip address to be pinged). The program goes into a loop reading the latest ping response placed in each queue by the ping process and displays the response from top of the window. Responses are displayed line by line and once the height of the window is reached, the window is refreshed and responses are displayed from the top again. Example terminal screen is shown in fig. 4.

The program attempts to fit as many windows on the screen as possible which is dependent on the number of ip addresses to be pinged and the size (max width and height) of the terminal screen. The program may crash if it can’t fit all windows on the terminal screen so the user may have to ping fewer ip addresses.

<p align="center" width="100%">
    <img width="1053" alt="img3" src="https://user-images.githubusercontent.com/101291172/199763849-6de8bf86-40df-473d-9db8-0b35224193ae.png">
    <p align="center">Figure 4: pingtool output showing the ping responses of ip addresses that are pinged.</p>
</p>

The program also generates a matplotlib plot of the ping response time (ms) for each ip address which updates in real time. It reads the ping response time from the ping response message for each ip and stores the value in a csv file (ping_response_times.csv). This csv file is read by a plot function which plots the response times. The matplotlib animate function is used to create the real time aspect of the plot by calling the plot function every second. Every time the plot function is called, all the ping response times are read from the csv file and plotted.

## Important Note

On windows, pingtool uses the **pythonping** library to execute ping commands and on Linux, it uses the OS command **ping**.

# Create Executable

If you wish to convert the pingtool source code (ping.py and pingutils.py) to an executable, do the following steps.

Install pyinstaller:

&nbsp;&nbsp;&nbsp;&nbsp; `pip install pyinstaller`

Execute the following command:

&nbsp;&nbsp;&nbsp;&nbsp;`pyinstaller --onefile ping.py`

pyinstaller will create two directories, build and dist. The executable can be found in dist. Run the executable and the program should run!

# References

[1] https://docs.python.org/3/howto/curses.html
