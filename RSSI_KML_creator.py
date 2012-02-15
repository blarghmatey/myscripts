from pykml.factory import KML_ElementMaker as KML
import csv
import argparse
from lxml import etree
from pykml.parser import Schema

parser = argparse.ArgumentParser(description='Create KML point data for RSSI values')
parser.add_argument('-f', '--infile', nargs=1, required=True, dest='infile')
parser.add_argument('-o', '--outfile', nargs=1, required=True, dest='outfile')
parser.add_argument('-t', '--type', nargs=1, default='avg', choices=['avg', 'min', 'max'], dest='valuearg')

args = parser.parse_args()
valuetype = ""
if(args.valuearg == 'avg'):
	valuetype = "AvgRSSI"
if(args.valuearg == 'min'):
	valuetype = "MinRSSI"
if(args.valuearg == 'max'):
	valuetype = "MaxRSSI"

data = csv.reader(open(str(args.infile).strip('[]\'')))
fields = data.next()
item = []
print "Parsing CSV"
for row in data:
	item.append(dict(zip(fields, row)))

points = []
for x in range(len(item)):
        points.append((float(item[x]['LATITUDE'].strip('"')), float(item[x]['LONGITUDE'].strip('"')), float(item[x][valuetype].strip('"'))))
#        points.append((item[x]['LATITUDE'], item[x]['LONGITUDE'], float(item[x][valuetype].strip('"'))))

doc = KML.Document()
style1 = KML.Style(
		KML.IconStyle(
			KML.scale(0.5),
			KML.color("BF0000FF"),
			KML.Icon(
				KML.href("http://www.earthpoint.us/Dots/GoogleEarth/WhitePaddle/blu-blank.png")
			)
		),
                KML.LabelStyle(
                        KML.color("BF0000FF"),
                        KML.colorMode("normal"),
                        KML.scale(0.65)
                ),
		id="red"
	)
doc.append(style1)

style2 = KML.Style(
                KML.IconStyle(
                        KML.scale(0.5),
                        KML.color("BF00FFFF"),
                        KML.Icon(
                                KML.href("http://www.earthpoint.us/Dots/GoogleEarth/WhitePaddle/blu-blank.png")
                        )
                ),
                KML.LabelStyle(
                        KML.color("BF00FFFF"),
                        KML.colorMode("normal"),
                        KML.scale(0.65)
                ),
                id="yellow"
        )
doc.append(style2)

style3 = KML.Style(
                KML.IconStyle(
                        KML.scale(0.5),
                        KML.color("BFFFFFFF"),
                        KML.Icon(
                                KML.href("http://www.earthpoint.us/Dots/GoogleEarth/WhitePaddle/blu-blank.png")
                        )
                ),
		KML.LabelStyle(
			KML.color("BFFFFFFF"),
			KML.colorMode("normal"),
			KML.scale(0.65)
		),
                id="white"
        )
doc.append(style3)

pointFolder = KML.Folder()
pointList = []
print "Creating KML"
for y in range(len(points)):
	if(points[y][2] <=10):
		colorvalue = "red"
	elif(points[y][2] >10 and points[y][2] <=14):
		colorvalue = "yellow"
	else:
		 colorvalue = "white"
	coord = points[y][1],points[y][0]
	pm = KML.Placemark(
			KML.name(points[y][2]),
			KML.styleUrl(colorvalue),
			KML.Point(
				KML.coordinates(str(coord).strip('() '))
				)
			)
	pointFolder.append(pm)

doc.append(pointFolder)

schema_ogc = Schema("ogckml22.xsd")
schema_ogc.assertValid(pointFolder)
fout = open(str(args.outfile).strip('[]\''),'w')
fout.write(etree.tostring(doc, pretty_print=True))
fout.close()
