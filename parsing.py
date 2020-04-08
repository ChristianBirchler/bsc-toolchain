#!/usr/bin/python3

import xml.etree.ElementTree as ET
import re


def get_namespace(element):
    tag = element.tag
    match = re.match(r"^{.*}", tag)
    namespace = match.group(0)
    return namespace


def get_surefire_plugin(tree):
    root = tree.getroot()
    namespace = get_namespace(root)

    plugins = None
    for el in root.iter():
        if el.tag == namespace+"plugins": plugins = el

    plugin_lst = plugins.findall(namespace+"plugin")
    
    for plugin in plugin_lst:
        if plugin.find(namespace+"artifactId").text ==  "maven-surefire-plugin":
            return plugin



if __name__ == "__main__":
    file = "pom1.xml"
        
    namespace = get_namespace(ET.parse(file).getroot())
    print(namespace)
    ET.register_namespace('', namespace[1:-1])

    tree = ET.parse(file)
    root = tree.getroot()

    has_argline = False

    for el in tree.iter(namespace+"argLine"):
        has_argline = True
        print(el.text)
        el.text = "-javaagent:/myAgent.jar " + el.text
        print(el.text)
        


    # surefire_plugin = None
    # has_config = False
    # for el in tree.iter(namespace+"plugin"):
    #     if el.find(namespace+"artifactId").text == "maven-surefire-plugin":
    #         surefire_plugin = el
    #         if el.find(namespace+"configuration") != None:
    #             has_config = True
        
    # print(surefire_plugin)
    # print(has_config)


    tree.write("new_pom.xml")



 

    # surefire_plugin = get_surefire_plugin(tree)
    # print(surefire_plugin)



    # surefire_artifactId = None
    # for el in root.iter(namespace+"artifactId"):
    #     if el.text == "maven-surefire-plugin":
    #         surefire_artifactId = el
    #         break




    # build = root.find(namespace+"build")
    # plugins = build.find(namespace+"plugins")
    # plugin_lst = plugins.findall(namespace+"plugin")
    # #print(plugin_lst)




    # # find surefire plugin
    # surefire_plugin = None
    # for plugin in plugin_lst:
    #     if plugin.find(namespace+"artifactId").text == "maven-surefire-plugin":
    #         surefire_plugin = plugin
    #         break
    
    # surefire_config = surefire_plugin.find(namespace+"configuration")
    # surefire_argline = surefire_config.find(namespace+"argLine")

    # print(surefire_argline.text)

    # surefire_argline.text = "-javaagent:/path/to/agent.jar " + surefire_argline.text
    
    

    # res = root.find(namespace+"plugin")
    # print(res)

# <artifactId>maven-surefire-plugin</artifactId>

