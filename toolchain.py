#!/usr/bin/python3

import sys
import csv
import time
import os
import re
import pydriller
import git
import xml.etree.ElementTree as ET

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_unique_urls_and_names(dataset):
    print("extract project urls ...")
    unique_urls_lst = []

    with open(dataset, "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            url = row[0]

            match = re.match(r".*/(.*$)", url) # regex for matching project names
            if match is None: continue

            name = match.group(1) # access the project name

            if (url,name) not in unique_urls_lst:
                print("add: " + url)
                time.sleep(0.1)
                unique_urls_lst.append((url,match.group(1)))

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


def get_project_only_data(dataset, proj_name):
    proj_data = []

    with open(dataset, "r") as file:
        csv_reader = csv.reader(file, delimiter=",")
        for row in csv_reader:
            match = re.match(r".*/(.*$)", row[0])
            if match is None: continue
            
            name = match.group(1)
            if name == proj_name:
                proj_data.append((row[0],row[1],row[2],row[3],row[4],row[5],row[6]))

    return proj_data


def get_namespace(element):
    """
    Return the namespace of the root element
    of the pom.xml. The namespace is usually
    for all elements int the pom the same.
    """
    tag = element.tag
    match = re.match(r"^{.*}", tag)
    namespace = match.group(0)
    return namespace


def add_java_agent_to_pom(agent_path):
    """
    Add "-javaagent:/path/to/agent.jar" inside the sureifre-plugin
    <argLine> tag. If such a tag does not exist then append the
    java agent via Shell command line '-DargLine=...'
    The directory of the shell is already the one of the project.

    return true if pom has <argLine> tag otherwise false
    """
    file = "pom.xml"

    # register namespace otherwise new pom will have 'ns0' namespace
    namespace = get_namespace(ET.parse(file).getroot())
    ET.register_namespace('', namespace[1:-1])

    tree = ET.parse(file)
    root = tree.getroot()
    
    has_argline = False

    for el in tree.iter(namespace+"argLine"):
        has_argline = True
        #print(el.text)
        el.text = "-javaagent:" + agent_path + " " + el.text
        #print(el.text)

    tree.write("pom.xml")

    return has_argline



def run_metric_gathering_on(dataset, parent_proj_dir, proj_name):
    """
    This function run all measurements of one particular project clone.

    """
    print("run metric gathering on " + bcolors.UNDERLINE + proj_name + bcolors.ENDC)
    os.chdir(ROOT)

    # all entries of dataset according to this particular project clone
    project_flaky_data = get_project_only_data(dataset, proj_name)
    
    os.chdir(parent_proj_dir+proj_name) # change PWD to current project's folder   

    # git API
    repo = git.Repo("./") 
    git_cmd = repo.git

    # variable to show if pom has a 'argLine' tag
    has_modified_argline = False

    # iterate over all commits according to the current project
    for i in range(len(project_flaky_data)):
        try:
            git_cmd.checkout(project_flaky_data[i][1])
            has_modified_argline = add_java_agent_to_pom(AGENT_PATH)

            if has_modified_argline:
            os.system("mvn test")
            else:
                os.system("mvn test -DargLine=" + AGENT_PATH)
        except:
            print(bcolors.WARNING + "Could not checkout to " + project_flaky_data[i][1] + bcolors.ENDC)
                 
    git_cmd.checkout("master")
    os.chdir(ROOT)
    







if __name__ == "__main__":
    print("start toolchain script ...")
    
    # if len(sys.argv) != 2:
    #     raise Exception(f"{bcolors.FAIL}one file (data) argument is needed{bcolors.FAIL}")


    # iterate over projects
    #   clone project
    #   iterate over all commits (based on dataset) of the current project
    #       build project
    #       iterate 10 times
    #           run test suite with java agent and mark the specific flaky test
    #           serialize the collected metrics and store into file (one file with 10 entries for each entry in the flaky dataset)
    #   delete project to save space


    # start timer
    t0 = time.time()

    # PARAMETERS
    DATASET = "test_data.csv" #sys.argv[1] # command line argument
    ROOT = os.getcwd()
    PROJ_DIR = "./projects-clones/"
    AGENT_PATH = "/home/christian/Desktop/bsc-agent/build/libs/bytebuddy.jar"
    RESET_PROJ_DIR = False
    KEEP_ALL_PROJ_IN_LOOP = True


    if RESET_PROJ_DIR:
        os.system("rm -rf " + PROJ_DIR)
        os.system("mkdir " + PROJ_DIR)


    project_urls_names = get_unique_urls_and_names(DATASET)
    #project_names = get_project_names(project_urls)

    

    for i in range(len(project_urls_names)):
        if RESET_PROJ_DIR:
            clone(project_urls_names[i][0], PROJ_DIR)
        
        proj_name = project_urls_names[i][1]

        run_metric_gathering_on(DATASET, PROJ_DIR, proj_name)

        if not KEEP_ALL_PROJ_IN_LOOP:
            delete_projects(PROJ_DIR)


    # stop timer
    t1 = time.time()
    te = t1 - t0
    print("toolchain script finished within {} seconds.".format(te))
    print("{} minutes.".format(te/60))
