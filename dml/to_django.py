import os
import xml.etree.ElementTree as et

newroot = et.Element('django-objects',version="1.0")
tree = et.ElementTree(file='projecten.xml')
root = tree.getroot()
for project in root:
    newproj = et.SubElement(newroot,'object',pk=project.get('id'),model='doctool.project')
    s = et.SubElement(newproj,'field',type="CharField", name="naam")
    s.text = project.get('naam')
    for element in project:
        if element.tag in ('kort','start','fysloc'):
            s = et.SubElement(newproj,'field',type="CharField", name=element.tag)
            s.text = element.text
        elif element.tag in ('oms','status'):
            s = et.SubElement(newproj,'field',type="TextField", name=element.tag)
            s.text = element.text
et.ElementTree(newroot).write('to_django.xml')

pad = 'user_spec'
tree = et.ElementTree(file=pad+".xml")
index = tree.getroot()
id = 0
for item in index:
    id += 1
    newspec = et.SubElement(newroot,'object',pk=str(id),model='doctool.userspec')
    s = et.SubElement(newspec,'field',to="doctool.project", name="project", rel="ManyToOneRel")
    s.text = item.get('project')
    s = et.SubElement(newspec,'field',type="CharField", name="naam")
    itemnaam = item.get('titel')
    itemtekst = item.text
    s.text = itemnaam
    tree = et.ElementTree(file=os.path.join(pad,itemnaam + '.xml'))
    root = tree.getroot()
    for element in root:
        if element.tag in ('kort','kosten','baten'):
            s = et.SubElement(newspec,'field',type="CharField", name=element.tag)
            if element.tag == 'kort' and element.text != itemtekst:
                s.text = '\n'.join((itemtekst,element.text))
            else:
                s.text = element.text
        elif element.tag in ('functie','beeld','product','opmerkingen'):
            newname = 'omgeving' if element.tag == 'opmerkingen' else element.tag
            s = et.SubElement(newspec,'field',type="TextField", name=newname)
            tekst = []
            for x in element:
                if x.tag == 'regel' and x.text is not None:
                    tekst.append(x.text)
            s.text = '\n'.join(tekst)
et.ElementTree(newroot).write('to_django.xml')

pad = 'func_task'
tree = et.ElementTree(file=pad+".xml")
index = tree.getroot()
id = 0
for item in index:
    id += 1
    newspec = et.SubElement(newroot,'object',pk=str(id),model='doctool.gebrtaak')
    s = et.SubElement(newspec,'field',to="doctool.project", name="project", rel="ManyToOneRel")
    s = et.SubElement(newspec,'field',to="doctool.userspec", name="spec", rel="ManyToOneRel")
    s = et.SubElement(newspec,'field',to="doctool.userwijz", name="rfc", rel="ManyToManyRel")
    s.text = item.get('project')
    s = et.SubElement(newspec,'field',type="CharField", name="naam")
    itemnaam = item.get('titel')
    itemtekst = item.text
    s.text = itemnaam
    tree = et.ElementTree(file=os.path.join(pad,itemnaam + '.xml'))
    root = tree.getroot()
    for element in root:
        if element.tag == 'doel':
            s = et.SubElement(newspec,'field',type="CharField", name=element.tag)
            if element.text != itemtekst:
                s.text = '\n'.join((itemtekst,element.text))
            else:
                s.text = element.text
        elif element.tag in ('wanneer','wie','condities','waarvoor','beschrijving'):
            s = et.SubElement(newspec,'field',type="TextField", name=element.tag)
            tekst = []
            for x in element:
                if x.tag == 'regel' and x.text is not None:
                    tekst.append(x.text)
            s.text = '\n'.join(tekst)
et.ElementTree(newroot).write('to_django.xml')

pad = 'func_proc'
tree = et.ElementTree(file=pad+".xml")
index = tree.getroot()
id = 0
for item in index:
    id += 1
    newspec = et.SubElement(newroot,'object',pk=str(id),model='doctool.funcproc')
    s = et.SubElement(newspec,'field',to="doctool.project", name="project", rel="ManyToOneRel")
    s = et.SubElement(newspec,'field',to="doctool.userspec", name="spec", rel="ManyToOneRel")
    s = et.SubElement(newspec,'field',to="doctool.userwijz", name="rfc", rel="ManyToManyRel")
    s = et.SubElement(newspec,'field',to="doctool.gebrtaak", name="gt", rel="ManyToManyRel")
    s = et.SubElement(newspec,'field',to="doctool.funcproc", name="bom", rel="ManyToManyRel")
    s.text = item.get('project')
    s = et.SubElement(newspec,'field',type="CharField", name="naam")
    itemnaam = item.get('titel')
    itemtekst = item.text
    s.text = itemnaam
    tree = et.ElementTree(file=os.path.join(pad,itemnaam + '.xml'))
    root = tree.getroot()
    for element in root:
        if element.tag == 'doel':
            s = et.SubElement(newspec,'field',type="CharField", name=element.tag)
            if element.text != itemtekst:
                s.text = '\n'.join((itemtekst,element.text))
            else:
                s.text = element.text
        elif element.tag in ('invoer','uitvoer','beschrijving'):
            s = et.SubElement(newspec,'field',type="TextField", name=element.tag)
            tekst = []
            for x in element:
                if x.tag == 'regel' and x.text is not None:
                    tekst.append(x.text)
            s.text = '\n'.join(tekst)
et.ElementTree(newroot).write('to_django.xml')

pad = 'tech_proc'
tree = et.ElementTree(file=pad+".xml")
index = tree.getroot()
id = 0
for item in index:
    id += 1
    newspec = et.SubElement(newroot,'object',pk=str(id),model='doctool.techproc')
    s = et.SubElement(newspec,'field',to="doctool.project", name="project", rel="ManyToOneRel")
    s = et.SubElement(newspec,'field',to="doctool.funcproc", name="fp", rel="ManyToManyRel")
    s = et.SubElement(newspec,'field',to="doctool.techtask", name="ft", rel="ManyToManyRel")
    s = et.SubElement(newspec,'field',to="doctool.techproc", name="bom", rel="ManyToManyRel")
    s = et.SubElement(newspec,'field',type="TextField", name="omgeving")
    s.text = item.get('project')
    s = et.SubElement(newspec,'field',type="CharField", name="naam")
    itemnaam = item.get('titel')
    itemtekst = item.text
    s.text = itemnaam
    tree = et.ElementTree(file=os.path.join(pad,itemnaam + '.xml'))
    root = tree.getroot()
    for element in root:
        if element.tag == 'doel':
            s = et.SubElement(newspec,'field',type="CharField", name=element.tag)
            if element.text != itemtekst:
                s.text = '\n'.join((itemtekst,element.text))
            else:
                s.text = element.text
        elif element.tag in ('invoer','uitvoer','beschrijving'):
            s = et.SubElement(newspec,'field',type="TextField", name=element.tag)
            tekst = []
            for x in element:
                if x.tag == 'regel' and x.text is not None:
                    tekst.append(x.text)
            s.text = '\n'.join(tekst)
et.ElementTree(newroot).write('to_django.xml')
