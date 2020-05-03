#!python3
import os, shutil
from pathlib import Path

path = str(Path.home())
path = path + "/"
print("<=== Europa ===>")

def Cmd(path):
    inp = input(path + ">>")
    inp = inp.split(" ")
    if inp[0] == "list":
        Seek(path, inp[1])
    #Delete Files
    elif inp[0] == "del":
        try:
            os.remove(path + inp[1])
            print("Deleted " + path + inp[1])
            Cmd(path)
        except:
            print("Unable to delete " + path + inp[1])
            Cmd(path)
    #Change Directory
    elif inp[0] == "cd":
        cd(path, inp)
    #Copy
    elif inp[0] == "copy":
        Copy(path, inp)
    #Make Folders/Files cmd
    elif inp[0] == "make":
        Make(path, inp)
    #Help
    elif inp[0] == "help":
        Help(path, inp)
    #Rename
    elif inp[0] == 'rename':
        Rename(path, inp)
    elif inp[0] == "open":
        Open(path, inp)

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
        Cmd(path)

def Make(path, inp):
    if inp[1] == "folder":
        os.mkdir(path + inp[2])
    else:
        f = open(path + inp[2] + "." + inp[1], 'w')
        f.close()
        Cmd(path)

def Rename(path, inp):
    try:
        os.rename(path + inp[1], path + inp[2])
        print("Renamed " + path + inp[1] + " to " + path + inp[2])
        Cmd(path)
    except:
        print("Unable to rename file")
        Cmd(path)

def Copy(path, inp):
    try:
        shutil.copyfile(path + inp[1], inp[2] + "/" + inp[1])
    except:
        print("Unable to copy " + path + inp[1] + " to " + inp[2])
        Cmd(path)


def Seek(path, options):
    i = 0

    for (path, dirs, files) in os.walk(path):
        if options == "all":
            print(path)
            print(dirs)
            print(files)
        elif options == "folders":
            print("[ Folders in " + path + " ]")
            print(dirs)
        elif options == "files":
            print("[ Files in " + path + " ]")
            print(files)
        else:
            print("Error")
        Cmd(path)
        break

def Open(path, inp):
    try:
        os.startfile(inp[1], 'open')
        Cmd(path)
    except:
        try:
            os.startfile(path + inp[1], 'open')
            Cmd(path)
        except:
            print("Unable to open file")
            Cmd(path)

Cmd(path)
