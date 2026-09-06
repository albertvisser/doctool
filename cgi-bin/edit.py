#! /usr/bin/env python3

import shared
from main.logic.edit_main import edit

def main():
    form = shared.get_input()
    fout, regels = edit({x: form.getfirst(x) for x in form.keys()})
    if fout:
        shared.procude_output(regels)
    else:
        wat  = form.getfirst("hWhat", '')
        cat  = form.getfirst("hCat", '')
        proj = form.getfirst("hProj", '')
        welk = form.getfirst("hWhich", '')
        shared.redirect(f"show.py?type=item&amp;what={wat}&amp;proj={proj}"
                        f"&amp;cat={cat}&amp;which={welk}&amp;edit=1")

if __name__ == '__main__':
  	main()
