from doctool_data_globals import datapad
xmlpad = datapad + "tech_data/"
<!ELEMENT gegevens (functie,opbouw,toegang,relatie,levensloop)>
<!ELEMENT functie (#PCDATA)>
<!ELEMENT opbouw  (attribuut+)>
<!ELEMENT attribuut	(omschrijving, soort)>
<!ATTLIST attribuut naam CDATA #REQUIRED soort CDATA #REQUIRED>
<!ELEMENT omschrijving (#PCDATA)>
<!ELEMENT soort (#PCDATA)>
<!ELEMENT toegang (EMPTY)>
<!ATTLIST toegang naam CDATA #REQUIRED>
<!ELEMENT relatie (EMPTY)>
<!ATTLIST relatie naam CDATA #REQUIRED entiteit CDATA #REQUIRED)>
<!ELEMENT levensloop (regel*)>
<!ELEMENT regel (#PCDATA)>

