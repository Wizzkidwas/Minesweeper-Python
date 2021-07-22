import tkinter, configparser, random, os, tkinter.messagebox, tkinter.simpledialog, _tkinter
from tkinter import *


flags = 0
rows = 10
cols = 10
mines = 10

field = []
buttons = [] # Setting default values to prevent any errors in case of missing data in config.ini

colours = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000'] # For the numebers

gameover = False
customsizes = []

def mainMenu():
    global window, menu, enterusername
    menu = tkinter.Tk() # Unique window just for main menu
    menu.title("Main Menu")
    welcome = tkinter.Label(menu, text="Welcome to Minesweeper!").grid(row=0, column=0,columnspan=3) 
    menubutton = tkinter.Button(menu, text="Let's play!", command=startGame).grid(row=2, column=0, columnspan=6, pady=10)
    frame_entry = Frame(menu)
    frame_entry.grid(row = 1, column = 0, columnspan = 2, padx = 25, pady = 10)
    Label(frame_entry, text = "Username: ").grid(row = 0, column = 0, padx = 10) # Allows entry of username to be stored
    enterusername = Entry(frame_entry, width = 15, bg = "White")
    enterusername.grid(row = 0, column = 1, padx = 5, pady = 5)

def menuWarp():
    global window
    window.destroy() # Destroys existing game window, as both game window main menu cannot be open at the same time
    mainMenu() # Loads the main menu

def startGame():
    global enterusername, menu, username, gameover
    username = enterusername.get() # Retrieves whatever was entered in the username field and stores it
    menu.destroy() # Destroys menu window, as game window and menu window cannot be open at the same time
    prepareWindow() 
    createMenu()
    prepareGame()
    gameover = False # Bug fix, now buttons can be clicked on if starting a game just after a game over

def createMenu():
    global window
    menubar = tkinter.Menu(window) # Makes a menu bar at the top of the game window
    menusize = tkinter.Menu(window, tearoff=0)
    menusize.add_command(label="Small (10x10 with 10 mines)", command=lambda: setSize(10, 10, 10))
    menusize.add_command(label="Medium (20x20 with 40 mines)", command=lambda: setSize(20, 20, 40))
    menusize.add_command(label="Big (35x35 with 120 mines)", command=lambda: setSize(35, 35, 120))
    menusize.add_command(label="Massive (50x50 with 200 mines)", command=lambda: setSize(50, 50, 200))
    menusize.add_command(label="Minimum (10x10 with 1 mine)", command=lambda: setSize(10, 10, 1))
    menusize.add_command(label="Maximum (50x50 with 2499 mines)", command=lambda: setSize(50, 50, 2499)) # Preset size options for the player to quickly load and play
    menusize.add_command(label="Set Custom Size", command=setCustomSize) # Allows setting of a custom size
    menusize.add_separator()
    for x in range(0, len(customsizes)): # Shows 5 most recent custom setups saved (Still buggy? But it's cool)
        menusize.add_command(label=str(customsizes[x][0])+"x"+str(customsizes[x][1])+" with "+str(customsizes[x][2])+" mines", command=lambda customsizes=customsizes: setSize(customsizes[x][0], customsizes[x][1], customsizes[x][2]))
    menubar.add_cascade(label="Settings", menu=menusize)
    window.config(menu=menubar)

def setCustomSize():
    global customsizes, window
    r = tkinter.simpledialog.askinteger("Custom size", "Enter number of rows between 10 and 50") # Asks for No.rows, forces integer
    while r < 10:
        r = tkinter.simpledialog.askinteger("Custom size", "Inputted value was below 10.\nNumber of rows must be an integer that is between 10 and 50.\n\nEnter a valid number of rows.")
    while r > 50:
        r = tkinter.simpledialog.askinteger("Custom size", "Inputted value was above 50.\nNumber of rows must be an integer that is between 10 and 50.\n\nEnter a valid number of rows.") # If below 10 or over 50, asks th user to input a valid value
    c = tkinter.simpledialog.askinteger("Custom size", "Enter number of columns between 10 and 50")
    while c < 10:
        c = tkinter.simpledialog.askinteger("Custom size", "Inputted value was below 10.\nNumber of columns must be an integer that is between 10 and 50.\n\nEnter a valid number of columns.")
    while c > 50:
        c = tkinter.simpledialog.askinteger("Custom size", "Inputted value was above 50.\nNumber of columns must be an integer that is between 10 and 50.\n\nEnter a valid number of columns.") # If below 10 or over 50, asks th user to input a valid value
    m = tkinter.simpledialog.askinteger("Custom size", "Minimum number of mines is: 1\nMaximum number of mines for this board size is: " + str((r*c)-1) + "\nEnter number of mines")
    while m >= r*c:
        m = tkinter.simpledialog.askinteger("Custom size", "Inputted value was too large.\nMinimum number of mines is: 1\nMaximum number of mines for this board size is: " + str((r*c)-1) + "\n\nEnter a valid number of mines.") # Prevents the entire board from being mines, forces at least one non-mine space
    while m <= 0:
        m = tkinter.simpledialog.askinteger("Custom size", "Inputted value was too low.\nMinimum number of mines is: 1\nMaximum number of mines for this board size is: " + str((r*c)-1) + "\n\nEnter a valid number of mines.") # Forces at least one mine
    customsizes.insert(0, (r,c,m)) # Saves into menubar for quick access
    customsizes = customsizes[0:5]
    setSize(r,c,m) # Sets that custom size
    createMenu() # Updates menu

def setSize(r,c,m):
    global rows, cols, mines, window
    rows = r
    cols = c
    mines = m # Transfers set values to be used for making the board
    saveConfig() # Saves into config file
    restartGame() # Loads with new board size

def saveConfig():
    global rows, cols, mines, window
    # Saves the current config in config.ini. If file does not exist, creates a new one
    config = configparser.SafeConfigParser()
    config.add_section("game")
    config.set("game", "rows", str(rows))
    config.set("game", "cols", str(cols))
    config.set("game", "mines", str(mines))
    config.add_section("sizes")
    config.set("sizes", "amount", str(min(5,len(customsizes))))
    for x in range(0,min(5,len(customsizes))):
        config.set("sizes", "row"+str(x), str(customsizes[x][0]))
        config.set("sizes", "cols"+str(x), str(customsizes[x][1]))
        config.set("sizes", "mines"+str(x), str(customsizes[x][2]))
    with open("config.ini", "w") as file:
        config.write(file)

def loadConfig():
    global rows, cols, mines, customsizes, window
    # Loads config.ini and loads the values stored within
    config = configparser.SafeConfigParser()
    config.read("config.ini")
    rows = config.getint("game", "rows")
    cols = config.getint("game", "cols")
    mines = config.getint("game", "mines")
    amountofsizes = config.getint("sizes", "amount")
    for x in range(0, amountofsizes):
        customsizes.append((config.getint("sizes", "row"+str(x)), config.getint("sizes", "cols"+str(x)), config.getint("sizes", "mines"+str(x))))

def prepareGame():
    global rows, cols, mines, field, window, buttons
    field = []
    for x in range(0, rows):
        field.append([])
        for y in range(0, cols):
            # Adds button and init value for the game
            field[x].append(0)
    # Generate mines on field
    for _ in range(0, mines):
        x = random.randint(0, rows-1)
        y = random.randint(0, cols-1)
        # Prevents mines spawning on top of each other
        while field[x][y] == -1:
            x = random.randint(0, rows-1)
            y = random.randint(0, cols-1)
        field[x][y] = -1
        if x != 0:
            if y != 0:
                if field[x-1][y-1] != -1:
                    field[x-1][y-1] = int(field[x-1][y-1]) + 1
            if field[x-1][y] != -1:
                field[x-1][y] = int(field[x-1][y]) + 1
            if y != cols-1:
                if field[x-1][y+1] != -1:
                    field[x-1][y+1] = int(field[x-1][y+1]) + 1
        if y != 0:
            if field[x][y-1] != -1:
                field[x][y-1] = int(field[x][y-1]) + 1
        if y != cols-1:
            if field[x][y+1] != -1:
                field[x][y+1] = int(field[x][y+1]) + 1
        if x != rows-1:
            if y != 0:
                if field[x+1][y-1] != -1:
                    field[x+1][y-1] = int(field[x+1][y-1]) + 1
            if field[x+1][y] != -1:
                field[x+1][y] = int(field[x+1][y]) + 1
            if y != cols-1:
                if field[x+1][y+1] != -1:
                    field[x+1][y+1] = int(field[x+1][y+1]) + 1
    for x in range(0, rows):
            for y in range(0, cols):
                buttons[x][y]["state"] = "normal" # Allows buttons to be clickable (Might be redundant now)
                
def prepareWindow():
    global rows, cols, buttons, flags, window, menu, enterusername, username
    window = tkinter.Tk()
    window.title(username) # Unique game window, makes the inputted username the title of the window
    createMenu() # Loads the menubar
    Restart = tkinter.Button(window, text="Restart", command=restartGame).grid(row=rows+1, column=0, columnspan=cols, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E) # Sets the buttons
    MenuWarp = tkinter.Button(window, text="Main Menu", command=menuWarp).grid(row=0, column=0, columnspan=cols-4, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    flags=0
    flagcount = tkinter.Label(window, text=flags).grid(row=0, column=cols-1, columnspan=1, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    flaglabel = tkinter.Label(window, text="Flags used:").grid(row=0, column=cols-4,columnspan=3, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E) # Places the flag counter in the corner
    buttons = []
    # Sets up the buttons
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            b = tkinter.Button(window, text=" ", width=2, command=lambda x=x,y=y: clickOn(x,y))
            b.bind("<Button-3>", lambda e, x=x, y=y:onRightClick(x, y))
            b.grid(row=x+1, column=y, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            buttons[x].append(b)

def restartGame():
    global gameover, window
    gameover = False
    # Destroys everything, possibly preventing a memory leak
    for x in window.winfo_children():
        if type(x) != tkinter.Menu:
            x.destroy()
    window.destroy()
    prepareWindow() # Loads a new window and game
    prepareGame()

def clickOn(x,y):
    global field, buttons, window, colours, gameover, rows, cols
    if gameover:
        return # Ignores click if gameover
    buttons[x][y]["text"] = str(field[x][y])
    buttons[x][y].config(disabledforeground=colours[field[x][y]], background='light grey') # Sets a different colour for clicked blocks to distinguish them
    if field[x][y] == -1:
        buttons[x][y]["text"] = "◉"
        buttons[x][y].config(background='red', disabledforeground='black')
        gameover = True
        # Shows all other mines
        for _x in range(0, rows):
            for _y in range(cols):
                if field[_x][_y] == -1:
                    buttons[_x][_y]["text"] = "◉"
        tkinter.messagebox.showinfo("Game Over", "You have lost.\nYou can choose to restart or play with different settings.")
        # Ends game and allows user to see all mines. They are left on the screen to either start a new game or go back to the menu.
    else:
        buttons[x][y].config(disabledforeground=colours[field[x][y]])
    if field[x][y] == 0:
        buttons[x][y]["text"] = " "
        # Repeats for all buttons nearby which are 0
        autoClickOn(x,y)
    buttons[x][y]['state'] = 'disabled' # They can't be clicked on again
    buttons[x][y].config(relief=tkinter.SUNKEN)
    checkWin() # After each click, checks if game is won

 
def autoClickOn(x,y):
    global field, buttons, colours, window, rows, cols
    if buttons[x][y]["state"] == "disabled":
        return # Ignores if button is disabled
    if field[x][y] != 0:
        buttons[x][y]["text"] = str(field[x][y])
        buttons[x][y].config(disabledforeground=colours[field[x][y]], background='light grey') # Displays number and makes background lighter than blank spaces
    else:
        buttons[x][y]["text"] = " "
        buttons[x][y].config(background='grey') # Empty spaces are made the darkest possible to discern them more easily
    buttons[x][y].config(disabledforeground=colours[field[x][y]])
    buttons[x][y].config(relief=tkinter.SUNKEN)
    buttons[x][y]['state'] = 'disabled' # Disables all the clicked buttons
    if field[x][y] == 0:
        if x != 0 and y != 0:
            autoClickOn(x-1,y-1)
        if x != 0:
            autoClickOn(x-1,y)
        if x != 0 and y != cols-1:
            autoClickOn(x-1,y+1)
        if y != 0:
            autoClickOn(x,y-1)
        if y != cols-1:
            autoClickOn(x,y+1)
        if x != rows-1 and y != 0:
            autoClickOn(x+1,y-1)
        if x != rows-1:
            autoClickOn(x+1,y)
        if x != rows-1 and y != cols-1:
            autoClickOn(x+1,y+1) # Checking all surrounding buttons

def onRightClick(x,y):
    global buttons, flags, window
    if gameover:
        return
    if buttons[x][y]["text"] == "⚑":
        buttons[x][y]["text"] = " "
        buttons[x][y]["state"] = "normal"
        flags = flags - 1   # Removes flag if flag is there
        tkinter.Label(window, text=flags).grid(row=0, column=cols-1, columnspan=1, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E) # Updates flag label to display correct number of flags
    elif buttons[x][y]["text"] == " " and buttons[x][y]["state"] == "normal":
        buttons[x][y]["text"] = "⚑"
        buttons[x][y]["state"] = "disabled"
        flags = flags + 1   # Adds flag if flag isn't there
        tkinter.Label(window, text=flags).grid(row=0, column=cols-1, columnspan=1, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E) # Updates flag label to display correct number of flags

def checkWin():
    global buttons, field, rows, cols, window
    win = True # Defaults to true
    for x in range(0, rows):
        for y in range(0, cols):
            if field[x][y] != -1 and buttons[x][y]["state"] == "normal":
                win = False # If there is an unclicked button that isn't a mine, sets it to false
    if win:
        tkinter.messagebox.showinfo("Victory!", "You have won.\nYou will be returned to the main menu.")
        window.destroy()
        mainMenu() # Kicks player back to main menu

if os.path.exists("config.ini"):
    loadConfig() # If file exists, load it
else:
    saveConfig() # If file doesn't exist, make it

mainMenu() # Opens main menu on startup
