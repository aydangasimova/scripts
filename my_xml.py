import xml.etree.ElementTree as ET
import re

def xml_prep(filename):
    with open(filename, 'a+') as file:
        file.write('\n</root>')

    def line_prepender(line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line.rstrip('\r\n') + '\n' + content)

    return line_prepender('<root>')

if __name__ == "__main__":

    filename = '../doc/telecats/bar.xml'
    file_list = ['../doc/telecats/bar.xml', '../doc/telecats/lubach.xml', '../doc/telecats/lubach2.xml', '../doc/telecats/joardy.xml', '../doc/telecats/joardy2.xml']

    for x in file_list:
        try:
            tree = ET.parse(filename)
        except ET.ParseError:
            print("assumed error in xml file - lacking the <root> element. <root> element being added now.")
            xml_prep(filename)

    tree = ET.parse(filename)
    root = tree.getroot()