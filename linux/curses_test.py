import curses
from curses import wrapper
import time


#test = 1
'''
def main(stdscr, test):
    
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

    BLUE_YELLOW = curses.color_pair(1)
    GREEN_BLACK = curses.color_pair(2)

    #counter_win = curses.newwin(20, 20, 0, 0)
    #counter_win1 = curses.newwin(20, 20, 0, 30)

    #for i in range(100):
    stdscr.clear()
    #counter_win.clear()
    #counter_win1.clear()
    color = BLUE_YELLOW
    stdscr.addstr(str(test), BLUE_YELLOW)
    #if i % 2 == 0:
     #   color = GREEN_BLACK
    
    #stdscr.addstr(f"Count: {i}", color)
    #counter_win.addstr("Hello world!\n", color)
    #counter_win1.addstr("hey wassup", GREEN_BLACK)
    stdscr.refresh()
    #counter_win.refresh()
    #counter_win1.refresh()
    
    time.sleep(0.1)
    stdscr.getch()
    #counter_win.getch()
'''
def main(stdscr):
    #stdscr.scrollok(1)
    try:
        while True:
            #with open('/tmp/install-report.json') as json_data:
            #beta = json.load(json_data)
            stdscr.clear()
            stdscr.addstr("\nStatus Report for Install process\n=========\n\n")
            for a1 in range(100):
                stdscr.addstr("{0}\n".format(a1))
                stdscr.refresh()
                time.sleep(0.1)
                
            ignore = stdscr.getch()  # wait at most 1msec, then ignore it
        
    finally:
        curses.endwin()
        #wrapper(main, 1235)
        #print("hello")

if __name__ == "__main__":
    '''
    w=curses.initscr()
    w.scrollok(1) # enable scrolling
    w.timeout(1)  # make 1-millisecond timeouts on `getch`

    try:
        while True:
            #with open('/tmp/install-report.json') as json_data:
            #beta = json.load(json_data)
            w.erase()
            w.addstr("\nStatus Report for Install process\n=========\n\n")
            for a1 in range(100):
                w.addstr("{0}\n".format(a1))
                w.refresh()
                time.sleep(0.1)
                
            ignore = w.getch()  # wait at most 1msec, then ignore it
        
    finally:
        curses.endwin()
    '''
    wrapper(main)
        #print("hello")