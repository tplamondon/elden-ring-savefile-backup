import os
from os import listdir
from os.path import isfile, join
import argparse
from posixpath import split


# https://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
def get_immediate_subdirectories(a_dir):
    return [
        name for name in os.listdir(a_dir) if os.path.isdir(os.path.join(a_dir, name))
    ]


def main():
    PATH = os.getenv("APPDATA")
    PATH = PATH + os.path.sep + "EldenRing"
    # this gives %appdata%/EldenRing
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
    print(id)


if __name__ == "__main__":
    main()
