#!/usr/bin/python3

import sys
import csv
import time
import os
import re

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_unique_urls_names(dataset):
    print("extract project urls ...")
    unique_urls_lst = []
    with open(dataset, "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            if row[0] not in unique_urls_lst:
                print("add: " + row[0])
                time.sleep(0.1)
                match = re.match(r".*/(.*$)", row[0])
                if match:
                    unique_urls_lst.append((row[0],match.group(1)))
    return unique_urls_lst[1:]


def clone(url, proj_dir):
    print(bcolors.OKBLUE + "start cloning " + bcolors.ENDC + bcolors.BOLD + url + bcolors.ENDC)
    os.chdir(proj_dir)
    bash_cmd = "git clone " + url + ".git"
    os.system(bash_cmd)
    os.chdir("../")
    print(bcolors.OKGREEN + "clone successful" + bcolors.ENDC)


def delete_projects(proj_dir):
    print("delete projects in " + proj_dir)
    os.system("rm -rf "+proj_dir+"*")
    

def get_project_names(project_urls):
    print("extract project names ...")
    proj_names = []
    for url in project_urls:
        name = re.match(r".*/(.*$)", url).group(1)
        proj_names.append(name)
        print("name: " + name)
    return proj_names


def run_metric_gathering_on(proj_dir, proj_name):
    print("run metric gathering on " + bcolors.UNDERLINE + proj_name + bcolors.ENDC)
    os.chdir(proj_dir+proj_name)

    

    os.chdir(ROOT)
    







if __name__ == "__main__":
    print("start toolchain script ...")
    
    if len(sys.argv) != 2:
        raise Exception(f"{bcolors.FAIL}one file (data) argument is needed{bcolors.FAIL}")


    # iterate over projects
    #   clone project
    #   iterate over all commits (based on dataset) of the current project
    #       build project
    #       iterate 10 times
    #           run test suite with java agent and mark the specific flaky test
    #           serialize the collected metrics and store into file (one file with 10 entries for each entry in the flaky dataset)
    #   delete project to save space


    # PARAMETERS
    DATASET = sys.argv[1]
    ROOT = os.getcwd()
    PROJ_DIR = "./projects-clones/"
    RESET_PROJ_DIR = False
    KEEP_ALL_PROJ_IN_LOOP = True

    if RESET_PROJ_DIR:
        os.system("rm -rf " + PROJ_DIR)
        os.system("mkdir " + PROJ_DIR)

    project_urls_names = get_unique_urls_names(DATASET)
    #project_names = get_project_names(project_urls)

    for i in range(len(project_urls_names)):
        if RESET_PROJ_DIR:
            clone(project_urls_names[i][0], PROJ_DIR)
        
        run_metric_gathering_on(PROJ_DIR, project_urls_names[i][1])

        if not KEEP_ALL_PROJ_IN_LOOP:
            delete_projects(PROJ_DIR)



