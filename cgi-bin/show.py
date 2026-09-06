#! /usr/bin/env python3

import shared
import types
from main_logic.show_main import Show

def main():
    form = shared.get_input()
    soort = form.getfirst("type", "")
    wat = form.getfirst("what", "")
    project = form.getfirst("proj", "0")
    categorie = form.getfirst("cat", "")
    welk = form.getfirst("which", "")
    edit = True if "edit" in form else False
    l = Show(soort, wat, project, categorie, welk, edit)
    shared.produce_output(l.lines)

if __name__ == '__main__':
    main()
