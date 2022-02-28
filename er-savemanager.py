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


def getFiles(folder):
    pathlib.Path(PROGRAMDIRECTORY + os.path.sep + extractIdFromPath(folder)).mkdir(
        exist_ok=True
    )
    backupFolder = PROGRAMDIRECTORY + os.path.sep + extractIdFromPath(folder)
    backupFiles = [f for f in listdir(backupFolder) if isfile(join(backupFolder, f))]
    return backupFiles, backupFolder


def getFileChoice(backupFiles):
    for i in range(int(len(backupFiles) / 2)):
        print(str(i) + ": " + backupFiles[i])
    print(str(int(len(backupFiles) / 2)) + ". Cancel")
    while True:
        choice = input("Please select backup to rename: ")
        if not choice.isnumeric():
            continue
        choice = int(choice)
        if choice == len(backupFiles) / 2:
            return -1
        if choice >= 0 and choice < len(backupFiles) / 2:
            break
    return choice


def choices():
    print("===================================")
    print("Please select one of the following: ")
    print("1. Backup save")
    print("2. Replace save with backup")
    print("3. Rename sackup")
    print("4. Delete sackup")
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
    if choice == 3:
        return waitForBackupOrReplace()
    else:
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
        saveFileBakBackup = (
            PROGRAMDIRECTORY
            + os.path.sep
            + extractIdFromPath(folder)
            + os.path.sep
            + "Replaced Backup"
            + os.path.sep
            + SAVEFILEBAK
            + ".0000.replacedbackup"
        )
        shutil.copyfile(folder + os.path.sep + SAVEFILE, saveFileBackup)
        shutil.copyfile(folder + os.path.sep + SAVEFILEBAK, saveFileBakBackup)
    else:
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
        shutil.copyfile(folder + os.path.sep + SAVEFILE, saveFileBackup)
        shutil.copyfile(folder + os.path.sep + SAVEFILEBAK, saveFileBakBackup)
    print("Succesfully backed up files")
    return 0


def replace(folder):
    print("===================================")

    backupFiles, backupFolder = getFiles(folder)
    # have list of backups available, SAVEFILE's come first, SAVEFILEBAK's come last
    choice = getFileChoice(backupFiles)
    if choice == -1:
        return

    # have choice now
    backupSaveFile = backupFolder + os.path.sep + backupFiles[choice]
    backupSaveFileBak = (
        backupFolder + os.path.sep + backupFiles[choice + int(len(backupFiles) / 2)]
    )
    print(
        "Backing up existing save, can be found in ./Elden Ring Backups/Replaced Backup/STEAM ID"
    )
    backup(folder, replaceBackup=True)
    print("Replacing existing save with chosen backup")
    shutil.copyfile(backupSaveFile, folder + os.path.sep + SAVEFILE)
    shutil.copyfile(backupSaveFileBak, folder + os.path.sep + SAVEFILEBAK)
    print("Succesfully replaced files")
    return 0


def rename(folder):
    print("===================================")
    backupFiles, backupFolder = getFiles(folder)
    # have list of backups available, SAVEFILE's come first, SAVEFILEBAK's come last
    choice = getFileChoice(backupFiles)
    if choice == -1:
        return
    # have choice now
    renameSaveFile = backupFolder + os.path.sep + backupFiles[choice]
    renameSaveFileBak = (
        backupFolder + os.path.sep + backupFiles[choice + int(len(backupFiles) / 2)]
    )
    tempRenameFile = renameSaveFile.split(".")
    tempRenameBak = renameSaveFileBak.split(".")
    if not tempRenameFile[-1].isnumeric():
        renameSaveFileNew = (
            tempRenameFile[0] + "." + tempRenameFile[1] + "." + tempRenameFile[2]
        )
        renameSaveFileBakNew = (
            tempRenameBak[0]
            + "."
            + tempRenameBak[1]
            + "."
            + tempRenameBak[2]
            + "."
            + tempRenameBak[3]
        )
    else:
        renameSaveFileNew = renameSaveFile
        renameSaveFileBakNew = renameSaveFileBak
    newName = "." + input("Please enter a name for the backup: ")
    newNameSaveFile = renameSaveFileNew + newName
    newNameSaveFileBak = renameSaveFileBakNew + newName

    shutil.move(renameSaveFile, newNameSaveFile)
    shutil.move(renameSaveFileBak, newNameSaveFileBak)
    print("Succesfully renamed files")
    return 0


def delete(folder):
    print("===================================")
    backupFiles, backupFolder = getFiles(folder)
    # have list of backups available, SAVEFILE's come first, SAVEFILEBAK's come last
    choice = getFileChoice(backupFiles)
    if choice == -1:
        return
    # have choice now
    deleteSaveFile = backupFolder + os.path.sep + backupFiles[choice]
    deleteSaveFileBak = (
        backupFolder + os.path.sep + backupFiles[choice + int(len(backupFiles) / 2)]
    )
    try:
        os.remove(deleteSaveFile)
        os.remove(deleteSaveFileBak)
    except:
        print("Error deleting backups")
        return
    print("Successfully deleted backups")
    return 0


def main():
    # adjust program directory
    global PROGRAMDIRECTORY
    PROGRAMDIRECTORY = PROGRAMDIRECTORY + os.path.sep + "Elden Ring Backups"
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
