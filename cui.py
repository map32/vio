import curses

def initialize(vios):
    for v in vios:
        v['added'] = True
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)
    vios = draw_menu(stdscr,vios)
    curses.nocbreak()
    stdscr.keypad(0)
    curses.echo()
    curses.endwin()
    return vios

def draw_menu(stdscr,vios):
    k = 0
    tIndex = 0
    granted = len(vios)
    cursor_x = 0
    cursor_y = 0

    # Clear and refresh the screen for a blank canvas
    stdscr.clear()
    stdscr.refresh()

    # Start colors in curses
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_WHITE)
    curses.init_pair(4, curses.COLOR_RED, curses.COLOR_WHITE)

    # Loop where k is the last character pressed
    while (k != ord('q')):

        # Initialization
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        if k == curses.KEY_DOWN:
            cursor_y = cursor_y + 1
            tIndex += 1
        elif k == curses.KEY_UP:
            cursor_y = cursor_y - 1
            tIndex -= 1
        elif k == curses.KEY_RIGHT:
            cursor_x = cursor_x + 1
            vios[tIndex]['added'] = not vios[tIndex]['added']
            if vios[tIndex]['added']:
                granted += 1
            else:
                granted -= 1
        elif k == curses.KEY_LEFT:
            cursor_x = cursor_x - 1
            vios[tIndex]['added'] = not vios[tIndex]['added']
            if vios[tIndex]['added']:
                granted += 1
            else:
                granted -= 1

        cursor_x = max(0, cursor_x)
        cursor_x = min(width-1, cursor_x)

        cursor_y = max(0, cursor_y)
        cursor_y = min(height-1, cursor_y)

        tIndex = max(0, tIndex)
        tIndex = min(len(vios)-1, tIndex)
        
        # Declaration of strings
        title = str(vios[0])[:width-1]
        subtitle = 'yes i made this'[:width-1]
        keystr = "Last key pressed: {}".format(k)[:width-1]
        statusbarstr = "Press 'q' to exit | STATUS BAR | Pos: {}, {}".format(cursor_x, cursor_y)
        if k == 0:
            keystr = "No key press detected..."[:width-1]

        # Centering calculations
        start_x_title = int((width // 2) - (len(title) // 2) - len(title) % 2)
        start_x_subtitle = int((width // 2) - (len(subtitle) // 2) - len(subtitle) % 2)
        start_x_keystr = int((width // 2) - (len(keystr) // 2) - len(keystr) % 2)
        start_y = int((height // 2) - 2)

        for i in range(0,min(len(vios)-tIndex,height-1)):
            if i == 0:
                stdscr.attron(curses.A_BOLD)
                if vios[i+tIndex]['added'] == True:
                    stdscr.attron(curses.color_pair(3))
                else:
                    stdscr.attron(curses.color_pair(4))
            else:
                if vios[i+tIndex]['added'] == True:
                    stdscr.attron(curses.color_pair(1))
                else:
                    stdscr.attron(curses.color_pair(2))
                    
            stdscr.addstr(i+1,0, vios[i+tIndex]['vid'][:width-1])

            if i == 0:
                stdscr.attroff(curses.A_BOLD)
                if vios[i+tIndex]['added'] == True:
                    stdscr.attroff(curses.color_pair(3))
                else:
                    stdscr.attroff(curses.color_pair(4))
            else:
                if vios[i+tIndex]['added'] == True:
                    stdscr.attroff(curses.color_pair(1))
                else:
                    stdscr.attroff(curses.color_pair(2))

        stdscr.addstr(1,10,vios[tIndex]['vid'][:width-10])
        stdscr.addstr(2,10,vios[tIndex]['name'][:width-10])
        stdscr.addstr(3,10,vios[tIndex]['address'][:width-10])
        stdscr.addstr(4,10,vios[tIndex]['date'][:width-10])
        for i in range(0,int(len(vios[tIndex]['desc'])/(width-10.))+1):
            stdscr.addstr(5+i,10,vios[tIndex]['desc'][i*(width-10):i*(width-10)+width-10])

        stdscr.attron(curses.color_pair(4))
        s = '%d printing | %d skipping | %d total | press q to print' % (granted, len(vios)-granted, len(vios))[:width]
        stdscr.addstr(height-1,0,(s+' '*(width-len(s)-1)))
        stdscr.attroff(curses.color_pair(4))

            
        # Refresh the screen
        stdscr.refresh()

        # Wait for next input
        k = stdscr.getch()

    return vios
