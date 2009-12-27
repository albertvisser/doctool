Files in this directory
=======================

cgi\cgi-bin
-----------
    cgi versie: cgi response routines

    edit.py
        document aanpassen en doorlinken naar show.py
        gebruikt cgi
        importeert globals
            edit_main uit edit_main
    globals.py
        o.a. pad naar programmatuur
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

cgi\dml
-------
    cgi versie: data manipulatie routines, aangeroepen door verwerkingsroutines

    docitems.py
        definieert class DataError, LaatsteWijz, ItemList, DocItem
            DocItem is de base class voor de diverse entiteiten
        gebruikt xml.etree
        importeert datapad uit doctool_data_globals
    doctool_data_globals.py
        o.a. pad naar data
    funcdata.py
        definieert class Entiteit voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems
    funcdocs.py
        definieert class FuncDoc voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems
    funcproc.py
        definieert class Functask voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems
    functask.py
        definieert class FuncDoc voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems
    procproc.py
        definieert class Procproc voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems
    project.py
        definieert class ProjectList, Project voor data manipulatie
        gebruikt xml.sax
        importeert datapad uit doctool_data_globals
    relaties.py
        definieert class Relaties tbv leggen relaties tussen entiteiten
        gebruik xml.sax
        importeert uit doctool_data_globals
    techdata.py
        vooralsnog alleen kopie van dtd
        definieert class FuncDoc voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems
    techproc.py
        definieert class Techproc voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems
    techtask.py
        definieert class Techtask voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems
    to_django.py
        conversieprogramma tbv overzetten naar django sqlite db
    userdocs.py
        definieert class UserDoc voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems
    userspec.py
        definieert class Userspec voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems
    userwijz.py
        definieert class Userwijz voor data manipulatie
        importeert datapad uit doctool_data_globals; DocItem uit docitems

cgi\dml\dtd
-----------
    cgi versie: beschrijvingen hoe de data eruit moet zien

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

cgi\html
--------
    cgi versie: html sources e.d.

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
    nieuw.html
        invulsource voor opvoeren nieuw document
    start.html
        invulsource voor startpagina
    start_proj.html
    start_proj_0.html
        invulsourcedeel algemene startpagina
    start_proj_other.html
        invulsource startpagina project
    template.html
        code voor javascript, header, footer

cgi\html\style
--------------
    cgi versie: css

    doctool.css
        styling info

cgi\main_logic
--------------
    cgi versie: verwerkingsroutines, aangeroepen vanuit cgi responses
                deze vullen de html sources verder in
                aan de hand van de opgehaalde gegevens

    doctool_globals.py
        pad naar data
        standaard instellingen/variabelen
    edit_main.py
        genereren source edit pagina's
        importeert types, doctool_globals,
            Project uit project,
            Userspec uit userspec,
            Userdocs uit userdocs,
            Userwijz uit userwijz,
            Funcdocs uit funcdocs,
            Functask uit functask,
            Funcproc uit funcproc,
            Funcdata uit funcdata (nog nietgeimplementeerd),
            Techtask uit techtask,
            Techproc uit techproc,
            Techdata uit techdata (nog niet geimplementeerd),
            Procproc uit procproc,
            Relaties uit relaties
    nieuw_main.py
        genereren foutmeldingen of opvoeren objecten
        importeert doctool_globals,
            Project uit project,
            Userspec uit userspec,
            Userdocs uit userdocs,
            Userwijz uit userwijz,
            Funcdocs uit funcdocs,
            Functask uit functask,
            Funcproc uit funcproc,
            Funcdata uit funcdata,
            Techtask uit techtask,
            Techproc uit techproc,
            Techdata uit techdata,
            Procproc uit procproc,
            ItemList uit docitems,
            Relaties uit relaties
    printobject.py
        genereren source raadplegen/nieuw item pagina's
        importeert doctool.globals,
            ItemList uit docitems
            Project uit project,
            Userspec uit userspec,
            Userdocs uit userdocs,
            Userwijz uit userwijz,
            Funcdocs uit funcdocs,
            Functask uit functask,
            Funcproc uit funcproc,
            Funcdata uit funcdata,
            Techtask uit techtask,
            Techproc uit techproc,
            Techdata uit techdata,
            Procproc uit procproc,
            ItemList uit docitems,
            Relaties uit relaties
    show_main.py
        bepalen te genereren pagina, genereren source algemeen gedeelte
        gebruikt input_<wat><cat>.html, start_proj_xx.html, nieuw.html,
            err_page.html, template.html, menu.html
        importeert doctool_globals,
            ItemList uit docitems
            printHTMLObject, printXMLObject uit printobject

django
------
    programmatuur django versie

    __init__.py
        (lege) package indicator
    admin.py
        aanmelden models bij admin site
    manage.py
        standaard maintenance programma
    models.py
        data mapping
    settings.py
        site instellingen
    urls.py
        url dispatcher
    views.py
        code voor opbouwen pagina's

django\templates
----------------

    base.html
        basis layout
    base_app.html
        app specifieke aanvullingen op base_site
    base_site.html
        site specifieke aanvullingen op base
    bevinding_edit.html
        invul-layout voor wijzigen testbevinding
    bevinding_view.html
        invul-layout voor weergeven testbevinding
    dataitem_edit.html
        invul-layout voor wijzigen technisch datamodel
    dataitem_view.html
        invul-layout voor weergeven technisch datamodel
    entiteit_edit.html
        invul-layout voor wijzigen logisch datamodel
    entiteit_view.html
        invul-layout voor weergeven logisch datamodel
    favicon.ico
        app icon
    funcdoc_edit.html
        invul-layout voor wijzigen document functioneel
    funcdoc_view.html
        invul-layout voor weergeven document functioneel
    funcproc_edit.html
        invul-layout voor wijzigen functioneel proces
    funcproc_view.html
        invul-layout voor weergeven functioneel proces
    gebrtaak_edit.html
        invul-layout voor wijzigen gebruikerstaak
    gebrtaak_view.html
        invul-layout voor weergeven gebruikerstaak
    layout_edit.html
        invul-layout voor wijzigen scherm/printlayout
    layout_view.html
        invul-layout voor weergeven scherm/printlayout
    lijst.html
        standaard layout voor lijstscherm
    programma_edit.html
        invul-layout voor wijzigen programmabeschrijving
    programma_view.html
        invul-layout voor weergeven programmabeschrijving
    project_edit.html
        invul-layout voor wijzigen projectsamenvatting
    project_view.html
        invul-layout voor weergeven projectsamenvatting
    relateren.html
        standaard layout voor keuzelijst bij aanbrengen relatie
    start.html
        startscherm
    techproc_edit.html
        invul-layout voor wijzigen technisch proces
    techproc_view.html
        invul-layout voor weergeven technisch proces
    techtaak_edit.html
        invul-layout voor wijzigen technische procesgroepering
    techtaak_view.html
        invul-layout voor weergeven technische procesgroepering
    testcase_edit.html
        invul-layout voor wijzigen beschrijving testgeval
    testcase_view.html
        invul-layout voor weergeven beschrijving testgeval
    testplan_edit.html
        invul-layout voor wijzigen testplan
    testplan_view.html
        invul-layout voor weergeven testplan
    userdoc_edit.html
        invul-layout voor wijzigen achtergrond informatie
    userdoc_view.html
        invul-layout voor weergeven achtergrond informatie
    userprob_edit.html
        invul-layout voor wijzigen probleem melding
    userprob_view.html
        invul-layout voor weergeven probleem melding
    userspec_edit.html
        invul-layout voor wijzigen gebruikers specificatie
    userspec_view.html
        invul-layout voor weergeven gebruikers specifikatie
    userwijz_edit.html
        invul-layout voor wijzigen aanvraag wijziging
    userwijz_view.html
        invul-layout voor weergeven aanvraag wijziging
