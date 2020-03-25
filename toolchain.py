#!/usr/bin/python3

import sys
import csv
import time
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def get_unique_urls(dataset):
    print("extract project urls ...")
    unique_urls_lst = []
    with open(dataset, "r") as file:
        csv_reader = csv.reader(file, delimiter=",") 
        for row in csv_reader:
            if row[0] not in unique_urls_lst:
                print("add: " + row[0])
                time.sleep(0.1)
                unique_urls_lst.append(row[0])
    return unique_urls_lst


def clone(url):
    print(bcolors.OKBLUE + "start cloning " + bcolors.ENDC + bcolors.BOLD + url + bcolors.ENDC)

    bash_cmd = "git clone " + url + ".git"
    os.system(bash_cmd)

    print(bcolors.OKGREEN + "clone successful" + bcolors.OKGREEN)


def clone_projects(project_urls, proj_dir):
    print("Start cloning projects to " + proj_dir)
    os.chdir(proj_dir)
    for url in project_urls:
        clone(url)
    os.chdir("../")

def get_projects(proj_dir):
    pass

if __name__ == "__main__":
    print("start toolchain script ...")
    
    if len(sys.argv) != 2:
        raise Exception(f"{bcolors.FAIL}one file (data) argument is needed{bcolors.FAIL}")

    # clone all projects specified in csv file

    # iterate over projects
    #   iterate over all commits (based on dataset) of the current project
    #       build project
    #       iterate 10 times
    #           run test suite with java agent and mark the specific flaky test
    #           serialize the collected metrics and store into file (one file with 10 entries for each entry in the flaky dataset)


    # PARAMETERS
    DATASET = sys.argv[1]
    PROJ_DIR = "./projects-clones/"
    RESET_PROJ_DIR = True

    if RESET_PROJ_DIR:
        os.system("rm -rf " + PROJ_DIR)
        os.system("mkdir " + PROJ_DIR)

    project_urls = get_unique_urls(DATASET)
    clone_projects(project_urls, PROJ_DIR)

    projects = get_projects(PROJ_DIR)



