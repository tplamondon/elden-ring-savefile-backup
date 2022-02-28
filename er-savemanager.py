import os, sys
from os import listdir
from os.path import isfile, join
import argparse
from posixpath import split
import pathlib
import shutil
from datetime import datetime

#! CONSTANTS
# required for pyintaller --onefile to work
if getattr(sys, "frozen", False):
    PROGRAMDIRECTORY = os.path.dirname(sys.executable)
elif __file__:
    PROGRAMDIRECTORY = str(pathlib.Path(__file__).parent.resolve())
PATH = os.getenv("APPDATA") + os.path.sep + "EldenRing"
# this gives %appdata%/EldenRing
SAVEFILE = "ER0000.sl2"
SAVEFILEBAK = "ER0000.sl2.bak"

# The following function was taken from here:
# https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
# I believe the following licence applies to this function https://creativecommons.org/licenses/by-sa/3.0/
def get_immediate_subdirectories(a_dir):
    return [
        name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))
    ]


def getIdFolder():
    folders = get_immediate_subdirectories(PATH)
    # have a list of steam id's, ask user for which one
    print("===================================")
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


def choices():
    print("===================================")
    print("Please select one of the following: ")
    print("1. Backup Save")
    print("2. Replace Save")
    print("3. Select a new steam id")
    print("4. Exit Program")
    while True:
        choice = input()
        if not choice.isnumeric():
            continue
        choice = int(choice)
        if choice >= 1 and choice <= 4:
            break
    if choice == 4:
        quit()
    return choice


def waitForBackupOrReplace():
    folder = getIdFolder()
    choice = choices()
    if choice == 3:
        return waitForBackupOrReplace()
    else:
        return folder, choice


def extractIdFromPath(folder):
    splitString = folder.split(os.path.sep)
    return splitString[-1]


def backup(folder):
    now = datetime.now()
    strTime = "." + now.strftime("%Y%m%d%H%M%S")
    saveFileBackup = (
        PROGRAMDIRECTORY
        + os.path.sep
        + extractIdFromPath(folder)
        + os.path.sep
        + SAVEFILE
        + strTime
    )
    saveFileBakBackup = (
        PROGRAMDIRECTORY
        + os.path.sep
        + extractIdFromPath(folder)
        + os.path.sep
        + SAVEFILEBAK
        + strTime
    )
    # create backup folder if needed
    pathlib.Path(PROGRAMDIRECTORY + os.path.sep + extractIdFromPath(folder)).mkdir(
        exist_ok=True
    )
    shutil.copyfile(folder + os.path.sep + SAVEFILE, saveFileBackup)
    shutil.copyfile(folder + os.path.sep + SAVEFILEBAK, saveFileBakBackup)
    print("Succesfully backed up files")
    return 0


def replace(folder):
    print("===================================")
    pathlib.Path(PROGRAMDIRECTORY + os.path.sep + extractIdFromPath(folder)).mkdir(
        exist_ok=True
    )
    backupFolder = PROGRAMDIRECTORY + os.path.sep + extractIdFromPath(folder)
    backupFiles = [f for f in listdir(backupFolder) if isfile(join(backupFolder, f))]
    # have list of backups available, SAVEFILE's come first, SAVEFILEBAK's come last
    for i in range(int(len(backupFiles) / 2)):
        print(str(i) + ": " + backupFiles[i])
    while True:
        choice = input("Please select backup to replace save file with: ")
        if not choice.isnumeric():
            continue
        choice = int(choice)
        if choice >= 0 and choice < len(backupFiles) / 2:
            break

    # have choice now
    backupSaveFile = backupFolder + os.path.sep + backupFiles[choice]
    backupSaveFileBak = (
        backupFolder + os.path.sep + backupFiles[choice + int(len(backupFiles) / 2)]
    )
    shutil.copyfile(backupSaveFile, folder + os.path.sep + SAVEFILE)
    shutil.copyfile(backupSaveFileBak, folder + os.path.sep + SAVEFILEBAK)
    print("Succesfully replaced files")
    return 0


def main():
    folder, choice = waitForBackupOrReplace()
    while True:
        if choice == 1:
            backup(folder)
        elif choice == 2:
            replace(folder)
        elif choice == 3:
            folder = getIdFolder()
        choice = choices()


if __name__ == "__main__":
    main()
