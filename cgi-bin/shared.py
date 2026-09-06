import cgi
import cgitb
cgitb.enable()
# import sys
# progpad = "../main_logic" # was "/home/albert/pythoneer/doctool"
# sys.path.append(progpad) # waar de eigenlijke programmatuur staat
cgipad = "http://doctool.lemoncurry.nl/cgi-bin/"

def get_input():
    form = cgi.FieldStorage()
    return form

def produce_output(lines):
    print("Content-Type: text/html\n")     # HTML is following
    for x in lines:
        print(x)
    print()

def redirect(loc):
    print("Content-Type: text/html")     # HTML is following
    print(f"Location: cgipad/{loc}\n")
