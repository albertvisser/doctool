import os
import shutil
from xml.etree.ElementTree import ElementTree, Element, SubElement
from doctool_data_common import datapad
relatiesfile = os.path.join(datapad, "relaties.xml") # naam van het xml bestand
backupfile = relatiesfile + '.old' # naam van de backup van het xml bestand

class Relaties(object):
    "lijst alle gegevens van een bepaald item"
    def __init__(self,soort,item):
        self.fn = relatiesfile
        self.fno = backupfile
        self.search_soort = soort
        self.search_item = item
        self.exists = os.path.exists(self.fn)
        self.relvan = {}
        self.relnaar = {}

    def read(self):
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        for x in rt.findall("relatie"):
            vantype = x.get('vantype')
            van = x.get('van')
            naartype = x.get('naartype')
            naar = x.get('naar')
            if vantype == self.search_soort and van == self.search_item:
                if self.relnaar.has_key(naartype):
                    self.relnaar[naartype].append(naar)
                else:
                    self.relnaar[naartype] = [naar]
            if naartype == self.search_soort and naar == self.search_item:
                if self.relvan.has_key(vantype):
                    self.relvan[vantype].append(van)
                else:
                    self.relvan[vantype] = [van]

    def write(self,soort, item, remove=False):
        shutil.copyfile(self.fn, self.fno)
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        if remove:
            for y in rt.findall("relatie"):
                vantype = y.get('vantype')
                van = y.get('van')
                naartype = y.get('naartype')
                naar = y.get('naar')
                if vantype == self.search_soort and van == self.search_item and \
                        naartype == soort and naar == item:
                    rt.remove(y)
        else:
            h = SubElement(rt, "relatie", vantype=self.search_soort,
                naartype=soort, van=self.search_item, naar=item)
        ElementTree(rt).write(self.fn)

    def add_relatie(self, soort, item):
        if self.relnaar.has_key(soort):
            self.relnaar[soort] = [item]
        else:
            self.relnaar[soort].append(item)
        self.write(soort, item)

    def rem_relatie(self, soort, item):
        if self.relnaar.has_key(soort):
            try:
                self.relnaar[soort].remove(item)
            except:
                pass
            else:
                self.write(soort, item, remove=True)

    def wijzig_relatie(self, soort, item1, item2):
        self.rem_relatie(soort, item1)
        self.add_relatie(soort, item2)

    def toon_relaties(self):
        for x in self.relnaar.keys():
            print ("relaties vanuit hier naar de volgende %ss:" % x)
            print "\t",
            for y in self.relnaar[x]:
                print y,
            print
        for x in self.relvan.keys():
            print ("relaties vanuit de volgende %ss naar hier:" % x)
            print "\t",
            for y in self.relvan[x]:
                print y,
            print
