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

  `git clone https://github.com/maneskull/pingtool.git`
  
Create virutal environment (venv):

  `cd pingtool

  `mkdir venv`
  
  `python -m venv venv`

Activate virutal environment (venv):

Linux:

   `source venv/bin/activate`

Windows:
	
   `venv/Scripts/activate`
 
Install main modules. Some additional modules will need to be installed.

Run script:
  
  `python ping.py`

 
## Operation

When the script is executed, it prompts the user to enter the IP addresses they wish to ping either manually or reading from a file. Basic checking is done on the ip addresses entered to verify they are of correct format and the script will notfiy the user of any errors.

Once the IP addresses has been entered, the script verifys to the user the ip addresses to ping and then prompts the user to enter the packet size. Once the packet size is entered, the script begins to display the output of the ping results to the curses screen.

Example output of the execution of the script:
![Screenshot from 2022-09-06 13-49-27](https://user-images.githubusercontent.com/101291172/188652472-97abc5e3-47f2-41d2-bc6f-87bc3ce1614b.png)


Please note there are some differences in the Linux and Windows versions and some issues which are to be fixed.
