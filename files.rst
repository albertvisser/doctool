Files in this directory
=======================

.hgignore
    ignore list voor version tool
cgi-bin
-------
    cgi scripts

    edit.py
        document aanpassen en doorlinken naar show.py
        gebruikt cgi
        importeert globals
            edit_main uit edit_main
    doctool_globals.py
        algemeen bruikbare constanten, o.a. pad naar programmatuur
    nieuw.py
        nieuw document opvoeren en doorlinken naar edit.py
        gebruikt cgi
        importeert globals
            nieuw_main uit nieuw_main
    show.py
        tonen document
        gebruikt cgi
        importeert globals
            show_main uit show_main

dml
---
    data manipulatie routines, aangeroepen door verwerkingsroutines

    docitems.py
        definieert class DataError, LaatsteWijz, ItemList, DocItem
            DocItem is de base class voor de diverse entiteiten
        gebruikt xml.etree
        importeert datapad uit doctool_data_globals
    docobj.py
        definieert de manipulatie classes voor de diverse documenten (toch een
        aanpassing op basis van herschrijven in Django want eerder zat het in
        aparte modules)
        importeert DocItem uit docitems
    doctool_data_common.py
        algemeen bruikbare constanten, o.a. pad naar data
    relaties.py
        definieert class Relaties tbv leggen relaties tussen entiteiten
        gebruik xml.sax
        importeert uit doctool_data_globals
    settings.py
        application settings
    to_django.py
        conversieprogramma tbv overzetten naar django sqlite db

dml/dtd
-------
    beschrijvingen hoe de data eruit moet zien

    Funcdata.dtd
    Funcproc.dtd
    Functask.dtd
    Generator.dtd
    Library.dtd
    listindex.dtd
    Procedure.dtd
    Procproc.dtd
    project.dtd
    Relaties.dtd
    Techdata.dtd
    Techproc.dtd
    Techtask.dtd
    userspec.dtd

html
----
    err_page.html
        html om te sturen bij een fout in de aanroep
    favicon.ico
        site icon
    index.html
        startpagina (ontwerpversie?)
    input_funcdata.html
        edit pagina voor object
    input_funcdocs.html
        edit pagina voor object
    Input_funcproc.html
        edit pagina voor object
    input_functask.html
        edit pagina voor object
    Input_procproc.html
        edit pagina voor object
    input_project.html
        edit pagina voor object
    Input_techproc.html
        edit pagina voor object
    Input_techtask.html
        edit pagina voor object
    input_userdocs.html
        edit pagina voor object
    input_userspec.html
        edit pagina voor object
    input_userwijz.html
        edit pagina voor object
    menu.html
        invulsource voor menu
    menu.js
        bijbehorende javascript
    nieuw.html
        invulsource voor opvoeren nieuw document
    start.html
        invulsource voor startpagina
    start.js
        bijbehorende javascript
    start_proj.html
    start_proj_0.html
        invulsourcedeel algemene startpagina
    start_proj_other.html
        invulsource startpagina project
    template.html
        code voor javascript, header, footer

html/images
-----------
    doctool.png
        homepage preview voor op de redirect pagina

html/style
----------
    doctool.css
        styling info

main_logic
----------
    verwerkingsroutines, aangeroepen vanuit cgi scripts
    deze vullen de html sources verder in aan de hand van de opgehaalde gegevens

    common.py
        pad naar data
        standaard instellingen/variabelen
    edit_main.py
        genereren source edit pagina's
        importeert types, doctool_globals,
            Project, Userspec, Userdocs, Userwijz, Funcdocs, Functask, Funcproc,
            Funcdata, Techtask, Techproc, Techdata, en Procproc uit docobj,
            Relaties uit relaties
    nieuw_main.py
        genereren foutmeldingen of opvoeren objecten
        importeert doctool_globals,
            Project, Userspec, Userdocs, Userwijz, Funcdocs, Functask, Funcproc,
            Funcdata, Techtask, Techproc, Techdata, en Procproc uit docobj,
            ItemList uit docitems,
            Relaties uit relaties
    printobject.py
        genereren source raadplegen/nieuw item pagina's
        importeert doctool.globals,
            ItemList uit docitems
            Project, Userspec, Userdocs, Userwijz, Funcdocs, Functask, Funcproc,
            Funcdata, Techtask, Techproc, Techdata, en Procproc uit docobj,
            Relaties uit relaties
    show_main.py
        bepalen te genereren pagina, genereren source algemeen gedeelte
        gebruikt input_<wat><cat>.html, start_proj_xx.html, nieuw.html,
            err_page.html, template.html, menu.html
        importeert doctool_globals,
            ItemList uit docitems
            printHTMLObject, printXMLObject uit printobject

