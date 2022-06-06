import argparse
import os
import re
import shutil
import csv
from datetime import datetime
from pathlib import Path
import itertools


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def generate_test_date(path_structure, prod_list, sequence_list, shot_list, department_list, version_list, SEQ_list, extension_list):
    """
    Generate a hierarchy of test data with given names for the different parts
    :param prod_list: Names of productions
    :param sequence_list: Names of sequences
    :param shot_list: Names of shots
    :param department_list: Names of departments
    :param version_list: Names of versions
    :param SEQ_list: Names of SEQ
    :param extension_list: Names of extensions
    """
    paths = list(itertools.product(
        *[prod_list, sequence_list, shot_list, department_list, version_list, SEQ_list, extension_list]))
    for keyword in paths:
        path = Path(
            path_structure + "/mnt/prod/{prod}/sequence/{sequence}/{shot}/{department}/render/{shot}-{department}-v{version}".format(
                prod = keyword[0], sequence = keyword[1], shot = keyword[2], department = keyword[3],
                version = keyword[4]))
        Path(path).mkdir(mode = 0o777, parents = True, exist_ok = True)
        touch(path / "{shot}-{department}-v{version}.{SEQ}.{extension}".format(shot = keyword[2],
                                                                               department = keyword[3],
                                                                               version = keyword[4],
                                                                               SEQ = keyword[5],
                                                                               extension = keyword[6]))


def clean(path, generate_data = True):
    """
    Look trough directory hierarchy and find the last directories with version number, keep only the last 3 versions
    for each folder hierarchy

    :param path: The path where to look for the data structure
    :param generate_data: If generate data is necessary
    """

    # Create the folder struture up to mnt/prod/ if not existing
    folder_path = str(Path(path + "/mnt/prod/"))
    if os.path.isdir(folder_path):
        pass
    else:
        os.mkdir(folder_path)

    # Generate the data if wanted with premade names
    if generate_data is True:
        generate_test_date(path, ["prod1", "prod2"], ["seq1", "seq2"], ["shot"], ["depart1", "depart2"],
                           ["001", "002", "003", "004", "005"], ["0003", "0001", "0005"], ["txt"])

    directories = []
    full_directories_path = []
    previous_dir = ''

    # Go search for last directories with the version number and gather all the versions of a given path into a list to
    # keep the last 3 ones and move the rest to a clean version of the folder hierarchy
    for root, dirs, files in os.walk(folder_path):
        if not dirs:
            if "clean" not in root:
                full_directories_path.append(root)
                if previous_dir != []:
                    root_path = root.split("-v")[0]
                    previous_dir = [root_path + '-v' + x.split("-v")[1] for x in previous_dir]
                    directories.append(previous_dir)
        previous_dir = dirs

    # Prepare CSV file header
    header = ['Date', 'Source Path', 'Destination Path']

    # Open CSV File
    with open(Path(folder_path) / 'track.csv', 'w', encoding = 'UTF8', newline = '') as f:
        writer = csv.writer(f)  # write the header
        writer.writerow(header)

        # Go through the versions directories and sort them, then move the first ones to the clean folder
        for dir in directories:

            # Sort by version number
            sorted_directories = sorted(dir, key = lambda x: (int(re.findall(r'\d+', x)[0])), reverse = True)[3:]
            for dir in sorted_directories:

                # Create a folder clean version structure similar to the original one to avoid having all files in a
                # single clean folder because of potential similar names
                dir_clean = Path(dir.replace('sequence', 'clean/sequence'))
                Path(dir_clean).mkdir(mode = 0o777, parents = True, exist_ok = True)

                # Move to clean directory the old versions
                shutil.move(dir, dir_clean)

                # Write to csv file informations
                writer.writerow([datetime.now().strftime("%d/%m/%Y %H:%M:%S"), dir, dir_clean])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "List folders")
    parser.add_argument("--path", type = str, required = True)
    parser.add_argument("--create_data", type = bool, required = True)
    args = parser.parse_args()
    clean(args.path)
