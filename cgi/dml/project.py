# -*- coding: iso-8859-1 -*-
from os.path import exists
from xml.etree.ElementTree import ElementTree,Element,SubElement
from doctool_data_globals import *
#~ datapad = "Z:/pythoneer/doctool/data/"
fnaam = datapad + "Project.xml"

class ProjectList:
    "lijst met gegevens van een selectie van items"
    def __init__(self, show=[], search={}):
        self.fn =  fnaam  # naam van het xml bestand
        self.Items = []
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        for x in rt.findall("project"):
            selectThis = False
            if len(search) == 0:
                selectThis = True
            selectItem = [x.get("id"),x.get("naam")]
            kort = ''
            h = x.find('kort')
            if h is not None and h.text is not None:
                kort = h.text
                if search.has_key('kort'):
                    z = search['kort'].upper()
                    s = kort.upper()
                    if s.find(z) >= 0:
                        selectThis = True
            oms = ''
            h = x.find('oms')
            if h is not None and h.text is not None:
                oms = h.text
                if search.has_key('oms'):
                    z = search['oms'].upper()
                    s = oms.upper()
                    if s.find(z) >= 0:
                        selectThis = True
            start = ''
            h = x.find('start')
            if h is not None and h.text is not None:
                start = h.text
                if search.has_key('start'):
                    z = search['start'].upper()
                    s = start.upper()
                    if s.find(z) >= 0:
                        selectThis = True
            fysloc = ''
            h = x.find('fysloc')
            if h is not None and h.text is not None:
                fysloc = h.text
                if search.has_key('fysloc'):
                    z = search['fysloc'].upper()
                    s = fysloc.upper()
                    if s.find(z) >= 0:
                        selectThis = True
            status = ''
            h = x.find('status')
            if h is not None and h.text is not None:
                status = h.text
                if search.has_key('status'):
                    z = search['status'].upper()
                    s = status.upper()
                    if s.find(z) >= 0:
                        selectThis = True
            if selectThis:
                if 'kort' in show:
                    selectItem.append(kort)
                if 'oms' in show:
                    selectItem.append(oms)
                if 'start' in show:
                    selectItem.append(start)
                if 'fysloc' in show:
                    selectItem.append(fysloc)
                if 'status' in show:
                    selectItem.append(status)
                self.Items.append(selectItem)

class Project:
    "lijst alle gegevens van een bepaald item"
    def __init__(self, id):
        self.Id = id
        self.fn =  fnaam  # naam van het xml bestand
        self.fno = fnaam + ".old" # naam van de backup van het xml bestand
        self.found = False
        self.fout = ''
        self.Naam = ''
        self.Kort = ''
        #~ self.Oms = []
        self.Oms = ''
        self.Start = ''
        self.Fysloc = ''
        #~ self.Status = []
        self.Status = ''
        if self.Id == "0" or self.Id == 0:
            if exists(self.fn):
                self.Id = self.findlaatste()
            else:
                self.Id = "1"

    def findlaatste(self):
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        i = 0
        for x in rt.findall("project"):
            h = int(x.get("id"))
            if  h > i:
                i = h
        return str(i + 1)

    def read(self):
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()
        i = 0
        for x in rt.findall("project"):
            h = int(x.get("id"))
            if h == int(self.Id):
                self.found = True
                break
        if self.found:
            h = x.get("naam")
            if h is not None: self.Naam = h
            h = x.find('kort')
            if h is not None:
                self.Kort = h.text
                if self.Kort is None:
                    self.Kort = ''
            h = x.find('oms')
            if h is not None:
                self.Oms = h.text
                if self.Oms is None:
                    self.Oms = ''
            h = x.find('start')
            if h is not None:
                self.Start = h.text
                if self.Start is None:
                    self.Start = ''
            h = x.find('fysloc')
            if h is not None:
                self.Fysloc = h.text
                if self.Fysloc is None:
                    self.Fysloc = ''
            h = x.find('status')
            if h is not None:
                self.Status = h.text
                if self.Status is None:
                    self.Status = ''

    def write(self):
        if not exists(self.fn):
            fh = open(self.fn,"w")
            fh.write('<?xml version="1.0" encoding="iso-8859-1"?>\n')
            fh.write('<projecten>\n')
            fh.write('</projecten>\n')
            fh.close()
        from shutil import copyfile
        copyfile(self.fn,self.fno)
        tree = ElementTree(file=self.fn)
        rt = tree.getroot()

    # gebruik dit om het Project "in-place" te wijzigen:
    #~ To access the subelements, you can use ordinary list (sequence) operations.
    #~ This includes len(element) to get the number of subelements, element[i] to fetch the i'th subelement,
    #~ and using the for-in statement to loop over the subelements:
        #~ for node in root:
            #~ print node
    #~ The element type also supports slicing (including slice assignment), and the standard append, insert and remove methods:
        #~ nodes = node[1:5]
        #~ node.append(subnode)
        #~ node.insert(0, subnode)
        #~ node.remove(subnode)

        for x in rt.findall("project"):
            gevonden = False
            if int(x.get("id")) == int(self.Id):
                gevonden = True
                x.set("naam",self.Naam)
                for y in x:
                    if y.tag == 'kort':
                        y.text = self.Kort
                    elif y.tag == 'oms':
                        #~ for z in self.Oms:
                            #~ s = SubElement(y,'regel')
                            #~ s.text = z
                        y.text = self.Oms
                    elif y.tag == 'start':
                        y.text = self.Start
                    elif y.tag == 'fysloc':
                        y.text = self.Fysloc
                    elif y.tag == 'status':
                        #~ for z in self.Status:
                            #~ s = SubElement(y,'regel')
                            #~ s.text = z
                        y.text = self.Status
                break
        if not gevonden:
            h = SubElement(rt,"project",id=self.Id,naam=self.Naam)
            s = SubElement(h,'kort')
            s.text = self.Kort
            s = SubElement(h,'oms')
            s.text = self.Oms
            s = SubElement(h,'start')
            s.text = self.Start
            s = SubElement(h,'fysloc')
            s.text = self.Fysloc
            s = SubElement(h,'status')
            s.text = self.Status
        tree = ElementTree(rt)
        tree.write(self.fn)
        self.exists = True

    def setAttr(self,naam,waarde):
        ok = True
        if naam == "naam":
            self.Naam = waarde
        elif naam == "kort":
            self.Kort = waarde
        elif naam == "oms":
            self.Oms = waarde
        elif naam == "start":
            self.Start = waarde
        elif naam == "fysloc":
            self.Fysloc = waarde
        elif naam == "status":
            self.Status = waarde
        else:
            ok = False
        return ok

if __name__ == '__main__':
    #~ test = 1
    #~ ih = Project(test)
    #~ ih.read()
    #~ if ih.found:
        #~ print ih.__class__
        #~ print "Project",ih.Id,":",ih.Naam
        #~ print 'Korte kenschets:',ih.Kort
        #~ print 'Omschrijving:',ih.Oms
        #~ print 'Main executable: ', ih.Start
        #~ print 'Fysieke locatie: ', ih.Fysloc
        #~ print 'Voortgang: ', ih.Status
    lh = ProjectList(show=['kort'],search={'kort': 'jcl'}) # show=['kort']
    for x in lh.Items:
        print x
