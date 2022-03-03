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
PATH = os.getenv("APPDATA") + os.path.sep + "DarkSoulsIII"
# this gives %appdata%/DarkSoulsIII
SAVEFILE = "DS30000.sl2"

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


def getFiles(folder):
    pathlib.Path(PROGRAMDIRECTORY + os.path.sep + extractIdFromPath(folder)).mkdir(
        exist_ok=True
    )
    backupFolder = PROGRAMDIRECTORY + os.path.sep + extractIdFromPath(folder)
    backupFiles = [f for f in listdir(backupFolder) if isfile(join(backupFolder, f))]
    return backupFiles, backupFolder


def getFileChoice(backupFiles, name):
    for i in range(int(len(backupFiles))):
        print(str(i) + ": " + backupFiles[i])
    print(str(int(len(backupFiles))) + ". Cancel")
    while True:
        choice = input("Please select backup to " + name + ": ")
        if not choice.isnumeric():
            continue
        choice = int(choice)
        if choice == len(backupFiles):
            return -1
        if choice >= 0 and choice < len(backupFiles):
            break
    return choice


def choices():
    print("===================================")
    print("Please select one of the following: ")
    print("1. Backup save")
    print("2. Replace save with backup")
    print("3. Rename backup")
    print("4. Delete backup")
    print("5. Select a new steam id")
    print("6. Exit program")
    while True:
        choice = input()
        if not choice.isnumeric():
            continue
        choice = int(choice)
        if choice >= 1 and choice <= 6:
            break
    if choice == 6:
        quit()
    return choice


def waitForBackupOrReplace():
    folder = getIdFolder()
    choice = choices()
    return folder, choice


def extractIdFromPath(folder):
    splitString = folder.split(os.path.sep)
    return splitString[-1]


def backup(folder, replaceBackup=False):
    now = datetime.now()
    strTime = "." + now.strftime("%Y%m%d%H%M%S")
    # create backup folder if needed
    pathlib.Path(PROGRAMDIRECTORY + os.path.sep + extractIdFromPath(folder)).mkdir(
        exist_ok=True
    )

    if replaceBackup == True:
        pathlib.Path(
            PROGRAMDIRECTORY
            + os.path.sep
            + extractIdFromPath(folder)
            + os.path.sep
            + "Replaced Backup"
        ).mkdir(exist_ok=True)
        saveFileBackup = (
            PROGRAMDIRECTORY
            + os.path.sep
            + extractIdFromPath(folder)
            + os.path.sep
            + "Replaced Backup"
            + os.path.sep
            + SAVEFILE
            + ".0000.replacedbackup"
        )
        shutil.copyfile(folder + os.path.sep + SAVEFILE, saveFileBackup)
    else:
        saveFileBackup = (
            PROGRAMDIRECTORY
            + os.path.sep
            + extractIdFromPath(folder)
            + os.path.sep
            + SAVEFILE
            + strTime
        )

        shutil.copyfile(folder + os.path.sep + SAVEFILE, saveFileBackup)
    print("Succesfully backed up files")
    return 0


def replace(folder):
    print("===================================")

    backupFiles, backupFolder = getFiles(folder)
    # have list of backups available
    choice = getFileChoice(backupFiles, "replace")
    if choice == -1:
        return

    # have choice now
    backupSaveFile = backupFolder + os.path.sep + backupFiles[choice]
    print(
        "Backing up existing save, can be found in ./Dark Souls 3 Backups/Replaced Backup/STEAM ID"
    )
    backup(folder, replaceBackup=True)
    print("Replacing existing save with chosen backup")
    shutil.copyfile(backupSaveFile, folder + os.path.sep + SAVEFILE)
    print("Succesfully replaced files")
    return 0


def rename(folder):
    print("===================================")
    backupFiles, backupFolder = getFiles(folder)
    # have list of backups available, SAVEFILE's come first
    choice = getFileChoice(backupFiles, "rename")
    if choice == -1:
        return
    # have choice now
    renameSaveFile = backupFolder + os.path.sep + backupFiles[choice]
    tempRenameFile = renameSaveFile.split(".")
    if not tempRenameFile[-1].isnumeric():
        renameSaveFileNew = (
            tempRenameFile[0] + "." + tempRenameFile[1] + "." + tempRenameFile[2]
        )
    else:
        renameSaveFileNew = renameSaveFile
    newName = "." + input("Please enter a name for the backup: ")
    newNameSaveFile = renameSaveFileNew + newName

    shutil.move(renameSaveFile, newNameSaveFile)
    print("Succesfully renamed files")
    return 0


def delete(folder):
    print("===================================")
    backupFiles, backupFolder = getFiles(folder)
    # have list of backups available
    choice = getFileChoice(backupFiles, "delete")
    if choice == -1:
        return
    # have choice now
    deleteSaveFile = backupFolder + os.path.sep + backupFiles[choice]
    try:
        os.remove(deleteSaveFile)
    except:
        print("Error deleting backup")
        return
    print("Successfully deleted backup")
    return 0


def main():
    # adjust program directory
    global PROGRAMDIRECTORY
    PROGRAMDIRECTORY = PROGRAMDIRECTORY + os.path.sep + "Dark Souls 3 Backups"
    # create backup folder if needed
    pathlib.Path(PROGRAMDIRECTORY).mkdir(exist_ok=True)
    folder, choice = waitForBackupOrReplace()
    while True:
        if choice == 1:
            backup(folder)
        elif choice == 2:
            replace(folder)
        elif choice == 3:
            rename(folder)
        elif choice == 4:
            delete(folder)
        elif choice == 5:
            folder = getIdFolder()

        choice = choices()


if __name__ == "__main__":
    main()
