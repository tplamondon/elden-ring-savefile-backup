import os
from os import listdir
from os.path import isfile, join
import argparse
from posixpath import split
import pathlib


#! CONSTANTS
PROGRAMDIRECTORY = pathlib.Path(__file__).parent.resolve()
PATH = os.getenv("APPDATA") + os.path.sep + "EldenRing"
# this gives %appdata%/EldenRing
SAVEFILE = "ER0000.sl2"
SAVEFILEBAK = "ER0000.sl2.bak"

# https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
def get_immediate_subdirectories(a_dir):
    return [
        name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))
    ]


def getIdFolder():
    folders = get_immediate_subdirectories(PATH)
    # have a list of steam id's, ask user for which one
    for i in range(len(folders)):
        print(str(i) + ": " + folders[i])
    while True:
        id = input("Please enter number of steam id you'd like to use: ")
        if not id.isnumeric():
            continue
        id = int(id)
        if id >= 0 and id < len(folders):
            break
    # have id
    usePath = PATH + os.path.sep + folders[id]
    return usePath


def choices(folder):
    print("Please select one of the following: ")
    print("1. Backup Save")
    print("2. Replace Save")
    print("3. Select a new steam id")
    print("4. Exit Program")
    while True:
        choice = input()
        if not choice.isnumeric():
            continue
        id = int(id)
        if id >= 1 and id <= 4:
            break
    if choice == 4:
        quit()
    return choice


def main():
    folder = getIdFolder()
    choice = choices(folder)

    #! CODE


if __name__ == "__main__":
    main()
