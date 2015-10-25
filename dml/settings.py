import os
from xml.etree.ElementTree import ElementTree, Element, SubElement
from doctool_data_globals import datapad

class DataError(Exception):
    pass

class Settings(object):
    def __init__(self):
        self.fn = datapad + "settings.xml"
        self.fno = self.fn + ".old"
        self.exists = False
        if os.path.exists(self.fn):
            self.read()
        else:
            self.nieuw()

    def nieuw(self):
        self.root = Element("settings")

    def read(self):
        tree = ElementTree(file=self.fn)
        self.root = tree.getroot()

    def write(self):
        tree = ElementTree(self.root)
        tree.write(self.fn)

    def get_schermtitel(self,wat,cat):
        h = ""
        for x in self.root.findall("section"):
            if x.get("name") == wat:
                for y in x.findall("cat"):
                    if y.get("name") == cat:
                        h = y.find("schermtitel").text
        return h

    def get_nieuwe_titel(self,wat,cat):
        h = ""
        for x in self.root.findall("section"):
            if x.get("name") == wat:
                for y in x.findall("cat"):
                    if y.get("name") == cat:
                        h = y.find("nieuwtitel").text
        return h
