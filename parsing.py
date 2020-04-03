#!/usr/bin/python3

import xml.etree.ElementTree as ET
import re


def get_namespace(element):
    tag = element.tag
    match = re.match(r"^{.*}", tag)
    namespace = match.group(0)
    return namespace



if __name__ == "__main__":
    file = "pom1.xml"
    tree = ET.parse(file)
    root = tree.getroot()
    namespace = get_namespace(root)
    print(namespace)

    for el in root.iter(namespace+"plugin"):
        print(el)
    
    # res = root.find(namespace+"plugin")
    # print(res)



