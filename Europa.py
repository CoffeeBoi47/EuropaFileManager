#!python3
#Imports
import os, shutil
from os.path import expanduser
from tkinter import *

#Init Tfkinter
root = Tk()
root.minsize(1200,1000)
root.title("Europa")
root.call('encoding', 'system', 'utf-8')
root.configure(bg='black')

#Gets the home Directory
path = expanduser("~")
path = path + '/'


#GUI Init
def MainBegin(path):
    global Menu, Files, DirLabel, v, canvas, Type
    v = StringVar()
    DirLabel = Label(root, textvariable=v, bg='black', fg="white")
    v.set(path)
    SearchLabel = Label(root, text='Search:', bg='black', fg="white").grid(row=0)
    Search = Entry(root, bg="black", fg="white")
    Files = Listbox(root, selectmode='single', bg='black', fg="white")
    Menu = Listbox(root, selectmode=SINGLE, bg='black', fg="white")
    Type = Listbox(root, selectmode=SINGLE, bg='black', fg="white")
    Size = Listbox(root, selectmode=SINGLE, bg='black', fg="white")
    Menu.bind('<<ListboxSelect>>', onselectMenu)


    Files.bind("<Button-3>", preClick)
    Files.bind("<Button-1>", onLeft)
    Files.bind('<Double-1>', OpenDir)


    Files.bind("<Button-5>", lambda event: OnMouseWheel(event, "down"))
    Type.bind("<Button-5>", lambda event: OnMouseWheel(event, "down"))
    Files.bind("<Button-4>", lambda event: OnMouseWheel(event, "up"))
    Type.bind("<Button-4>", lambda event: OnMouseWheel(event, "up"))
    Size.bind("<Button-4>", lambda event: OnMouseWheel(event, "up"))
    Size.bind("<Button-5>", lambda event: OnMouseWheel(event, "down"))
    Files.bind("<Button-3>")


    Copy = Button(root, text='Copy')
    Search.grid(row=1, column=0)
    DirLabel.grid(row=1, column=1)
    Menu.grid(row=2, column=0)
    Files.grid(row=2, column=1)
    Type.grid(row=2, column=2)
    Type.config(width=14, height=50)
    Menu.config(width=20, height=50)
    Files.config(width=70, height=50)
    Size.grid(row=2, column=3)
    Size.config(width=12, height=50)


    path = expanduser("~") + "/"
    Files.delete(0, 'end')
    Type.delete(0, 'end')
    listfiles(path)
    FavMenuInit(path, Menu)

#Closes popup menus if you click away from them
def popupFocusOut(Box):
        Box.destroy()

#Gets the Favorited Folders and loads them into the favorites menu
def FavMenuInit(path, Menu):
    global favorites
    path2 = path + '/Europa'

    #Sees if the Europa Folder exsists in the home Directory
    if not os.path.exists(path2):
        #Makes a Europa folder if there is no Europa folder
        os.makedirs(path2)

    filename = "Favorites.txt"
    #Opens the Favorites.txt if it exsists
    if os.path.exists(path2 + '/Favorites.txt'):
        favorites = open(os.path.join(path2, filename), 'r')
    #Makes a Favorites.txt and adds the defualt Menu Folders if there is not a Favorites.txt
    else:
        with open(os.path.join(path2, filename), 'w') as favorites:
            favorites.write("Home\n Downloads\n Desktop\n")
            favorites.write(f" {path}\n {path}/Downloads/\n {path}/Desktop\n")
            favorites.close()
            favorites = open(os.path.join(path2, filename), 'r')

    #Adds the Folders from Favorites.txt to the Favorites Menu
    favorites = favorites.read().split(" ")
    y = -1
    for i in range(int(len(favorites) / 2)):
        try:
            y = y + 1
            Menu.insert(END, favorites[y].replace(":", ""))
        except:
            break

#Adds files from selected Directory to the Files Listbox
def listfiles(path):
    #Gets all folders in specified Directory and adds them to the files listbox
    wts = Seek(path, 'folders')
    for x in wts:
        Files.insert(END, x)
        Type.insert(END, 'Type: FOLDER')
    #Gets all files in specified Directory and then assigns it a type based on the kind then adds them to the files listbox
    wts = Seek(path, 'files')
    for x in wts:
        if x.endswith(".mp3"):
            Files.insert(END, x)
            Type.insert(END, 'Type: MP3')
        elif x.endswith(".jpeg"):
            Files.insert(END, x)
            Type.insert(END, 'Type: JPG')
        elif x.endswith(".png"):
            Files.insert(END, x)
            Type.insert(END, 'Type: PNG')
        elif x.endswith(".py"):
            Files.insert(END, x)
            Type.insert(END, 'Type: PYTHON')
        elif x.endswith(".jar"):
            Files.insert(END, x)
            Type.insert(END, 'Type: JAVA')
        elif x.endswith(".txt"):
            Files.insert(END, x)
            Type.insert(END, 'Type: TEXT')
        elif x.endswith(".log"):
            Files.insert(END, x)
            Type.insert(END, 'Type: LOG')
        elif x.endswith(".htm") or x.endswith(".html"):
            Files.insert(END, x)
            Type.insert(END, 'Type: HTML')
        elif x.endswith(".css"):
            Files.insert(END, x)
            Type.insert(END, 'Type: CSS')
        elif x.endswith(".js"):
            Files.insert(END, x)
            Type.insert(END, 'Type: JS')
        elif x.endswith(".desktop"):
            Files.insert(END, x)
            Type.insert(END, 'Type: DEKSTOP')
        else:
            Files.insert(END, x)
            Type.insert(END, 'Type: FILE')



#Adds the files from the selected favorite folder into the files listbox
def onselectMenu(evt):
    global path
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    path = favorites[index + int(len(favorites) / 2)].strip() + "/"
    Files.delete(0, 'end')
    Type.delete(0, 'end')
    v.set(path)
    listfiles(path)

#Changes listed files in the files listbox to the Directory specified
def OpenDir(evt):
    global path
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    #Sees if current selected item is a folder or not
    if value.startswith("Type: File       "):
        return None
    #If current selected item is a folder clear files listbox and add the files from the new specified Directory
    else:
        path = path + value.replace("Type: Folder       ", "") + '/'.strip()
        dirs = Seek(path, "folders")
        Files.delete(0, 'end')
        Type.delete(0, 'end')
        v.set(path)
        dist = 35
        listfiles(path)

#Returns a array of Files/Folders in a specified Directory
def Seek(path, options):
    i = 0
    for (path, dirs, files) in os.walk(path):
        #If selection is folders return a array of folders in the specified Directory
        if options == "folders":
            return dirs
        #If selection is files return a array of files in the specified Directory
        elif options == "files":
            return files
        else:
            print("Please specify either [folders] or [files]")
        break

#Scrolls the File Type Listbox and Files Listbox together
def OnMouseWheel(event, di):
    #If scrolled up
    if di == "up":
        delta = -2
    #If scrolled down
    elif di == 'down':
        delta = 2

    #Closes a context menu if there is one
    onLeft()
    #Scroll both Listboxes either up or down depending on wether you scrolled up or down
    Files.yview_scroll(delta,'units')
    Type.yview_scroll(delta,'units')
    #Stops the Listbox your hovering over from scrolling from you input so it doesnt scroll down twice
    return "break"


def onRight(event):
    Files.selection_clear(0, END)
    Files.selection_set(Files.nearest(event.y))
    Files.activate(Files.nearest(event.y))

    #Gets the X and Y coordinates slightly below the mouse so the menu pops up below the cursor instead of above it
    cursorx = int(root.winfo_pointerx() - root.winfo_rootx())
    cursory = int(root.winfo_pointery() - root.winfo_rooty())

    # Now we define our right click menu canvas
    onRight.menu = Canvas(root, width=150, height=50, highlightbackground="gray", highlightthickness=1)
    # And here is where we use our X and Y variables, to place the menu where our cursor is,
    # That's how right click menus should be placed.
    onRight.menu.place(x=cursorx, y=cursory)
    # This is for packing our options onto the canvas, to prevent the canvas from resizing.
    # This is extremely useful if you split your program into multiple canvases or frames
    # and the pack method is forcing them to resize.
    onRight.menu.pack_propagate(0)
    # Here is our label on the right click menu for deleting a row, notice the cursor
    # value, which will give us a pointy finger when you hover over the option.
    delLabel = Label(onRight.menu, text="Test Button", cursor="hand2", anchor="w")
    delLabel.pack(side="top", padx=1, pady=1, fill="x")

    # This function is for removing the canvas when an option is clicked.
    def destroy():
        onRight.menu.place_forget()

    # This is the function that removes the selected item when the label is clicked.
    def delete(*args):
        print("Test button on the right click menu has been clicked!")
        destroy()

    delLabel.bind("<Button-1>", delete)

# This is to prevent infinite right click menus; it sees if there is an existing menu
# and removes it, bringing it out in a new position.
def preClick(event):
    try:
        onRight.menu.place_forget()
        onRight(event)
    except Exception:
        onRight(event)

# Hide menu when left clicking
def onLeft(*args):
    try:
        onRight.menu.place_forget()
    except Exception:
        pass


#CMD LINE VERSION COMMANDS, DEBRICATED!

def Help(path, inp):
    x = 1
    ree = x in range(-len(inp), len(inp))
    if ree == False:
        listCmd = True
    elif inp[1] == '':
        listCmd = True
    elif inp[1] == "cd":
        listCmd = False
        print("""Command: cd
Function: Changes the Current Working Directory
Usage: cd [Directory/Folder in the current Directory]""")
        Cmd(path)
    try:
        if listCmd == True:
            print("""Type [help 'command'] for info on that command.
Commands:
[cd] [list] [del] [help] [copy] [make]""")
            Cmd(path)
    except:
        print("Please Enter a valid help command")
        Cmd(path)

def Del(path, inp):
    try:
        os.remove(path + inp[1])
        print("Deleted " + path + inp[1])
        Cmd(path)
    except:
        print("Unable to delete " + path + inp[1])
        Cmd(path)


def cd(path, inp):
    try:
        if os.path.isdir(inp[1]) == True:
            path = path + inp[1] + "/"
            print("Changed Directory to " + path)
            Cmd(path)
        elif os.path.isdir(path + inp[1]) == True and inp[1] != "":
            path = path + inp[1] + '/'
            print("Changed Directory to " + path)
            Cmd(path)
        elif inp[1] == '':
            path = "/home/john/"
            Cmd(path)
        else:
            print(path + inp[1] + " is not a Directory!")
            Cmd(path)
    except:
        path = "/home/john/"

def Make(path, inp):
    if inp[1] == "folder":
        os.mkdir(path + inp[2])
    else:
        f = open(path + inp[2] + "." + inp[1], 'w')
        f.close()

def Rename(path, inp):
    try:
        os.rename(path + inp[1], path + inp[2])
        print("Renamed " + path + inp[1] + " to " + path + inp[2])
    except:
        print("Unable to rename file")

def Copy(path, inp):
    try:
        shutil.copyfile(path + inp[1], inp[2] + "/" + inp[1])
    except:
        print("Unable to copy " + path + inp[1] + " to " + inp[2])



def Open(path, inp):
    try:
        os.startfile(inp[1], 'open')
    except:
        try:
            os.startfile(path + inp[1], 'open')
        except:
            print("Unable to open file")


MainBegin(path)
root.mainloop()
