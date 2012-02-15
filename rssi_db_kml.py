from pykml.factory import KML_ElementMaker as KML
#import csv
import argparse
from lxml import etree
from pykml.parser import Schema
import pyodbc

parser = argparse.ArgumentParser(description='Create KML point data for RSSI values')
#parser.add_argument('-f', '--infile', nargs=1, dest='infile')
#parser.add_argument('-o', '--outfile', nargs=1, dest='outfile')
#parser.add_argument('-t', '--type', nargs=1, default='avg', choices=['avg', 'min', 'max'], dest='valuearg')
parser.add_argument('-a', '--area', nargs='*')
parser.add_argument('-s', '--startdate', required=True, help='Date in mmddyyyy format')
parser.add_argument('-e', '--enddate', required=True, help='Date in mmddyyyy format')

args = parser.parse_args()

#valuetype = ""
#if(args.valuearg == 'avg'):
#	valuetype = "AvgRSSI"
#if(args.valuearg == 'min'):
#	valuetype = "MinRSSI"
#if(args.valuearg == 'max'):
#	valuetype = "MaxRSSI"

orgName = ""
for i in args.area:
	orgName = orgName + i + ' '
orgName = orgName.rstrip()
startDate = args.startdate[:2] + '/' + args.startdate[2:4] + '/' + args.startdate[4:] + ' 00:00:00'
endDate = args.enddate[:2] + '/' + args.enddate[2:4] + '/' + args.enddate[4:] + ' 23:59:59'

print "Executing query"
conn = pyodbc.connect("DRIVER=TDS;SERVER=<server>;PORT=14330;DATABASE=<DB>;UID=<user>;PWD=<password>;TDS_Version=8.0;Trusted_Connection=False")
cursor = conn.cursor()
cursor.execute("SELECT ORGANIZATIONNAME, SPACENUMBER, SERIALNUMBER, Assets.LATITUDE, Assets.LONGITUDE, MIN(CAST(RSSI AS INT)) MinRSSI, MAX(CAST(RSSI AS INT)) MaxRSSI, AVG(CAST(RSSI AS DECIMAL)) AvgRSSI\
    FROM ORGANIZATIONS, ORGANIZATIONASSETS, PARKINGMETERPOLICY, HISTORICALPUCKSTATUS, ASSETS\
    WHERE ORGANIZATIONS.ORGANIZATIONID = ORGANIZATIONASSETS.ORGANIZATIONID\
    AND ORGANIZATIONASSETS.ASSETID = PARKINGMETERPOLICY.ASSETID\
    AND ORGANIZATIONASSETS.ASSETID = HISTORICALPUCKSTATUS.ASSETID\
    AND ORGANIZATIONASSETS.ASSETID = ASSETS.ASSETID\
    AND ORGANIZATIONS.ORGANIZATIONNAME LIKE ?\
    AND ORGANIZATIONCATEGORYID = 1\
    AND STATUSDATETIME BETWEEN ? AND ?\
    AND BATTERY NOT IN (254,255)\
    AND SPACENUMBER IS NOT NULL\
    GROUP BY ORGANIZATIONNAME, SPACENUMBER, SERIALNUMBER, ASSETS.LATITUDE, ASSETS.LONGITUDE\
    ORDER BY SPACENUMBER", [orgName, startDate, endDate])

rows = cursor.fetchall()
#data = csv.reader(open(str(args.infile).strip('[]\'')))
#fields = data.next()
#item = []
#print "Parsing CSV"
#for row in data:
#	item.append(dict(zip(fields, row)))

#points = []
#for row in rows:
#        points.append((float(rows[x]['LATITUDE'].strip('"')), float(item[x]['LONGITUDE'].strip('"')), float(item[x][valuetype].strip('"'))))
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

SpaceFolder = KML.Folder(
			KML.name("SpaceNumbers"),
			id='SpaceNumbers')
print "Creating Space Number KML"
for row in rows:
	colorvalue = "white"
	pm = KML.Placemark(
			KML.name(row.SPACENUMBER),
			KML.styleUrl(colorvalue),
			KML.Point(
				KML.coordinates(str(row.LONGITUDE) + ',' + str(row.LATITUDE))
				)
			)
	SpaceFolder.append(pm)
doc.append(SpaceFolder)

AvgRSSIFolder = KML.Folder(
			KML.name("AvgRSSI"),
			id='AvgRSSI')
print "Creating Avg RSSI KML"
for row in rows:
	if(row.AvgRSSI <=10):
		colorvalue = "red"
	elif(row.AvgRSSI >10 and row.AvgRSSI <=14):
		colorvalue = "yellow"
	else:
		 colorvalue = "white"
	pm = KML.Placemark(
			KML.name(row.AvgRSSI),
			KML.styleUrl(colorvalue),
			KML.Point(
				KML.coordinates(str(row.LONGITUDE) + ',' + str(row.LATITUDE))
				)
			)
	AvgRSSIFolder.append(pm)

doc.append(AvgRSSIFolder)

MinRSSIFolder = KML.Folder(
			KML.name("MinRSSI"),
			id='MinRSSI')
print "Creating Min RSSI KML"
for row in rows:
        if(row.MinRSSI <=10):
                colorvalue = "red"
        elif(row.MinRSSI >10 and row.MinRSSI <=14):
                colorvalue = "yellow"
        else:
                 colorvalue = "white"
        pm = KML.Placemark(
                        KML.name(row.MinRSSI),
                        KML.styleUrl(colorvalue),
                        KML.Point(
                                KML.coordinates(str(row.LONGITUDE) + ',' + str(row.LATITUDE))
                                )
                        )
        MinRSSIFolder.append(pm)
doc.append(MinRSSIFolder)

MaxRSSIFolder = KML.Folder(
			KML.name("MaxRSSI"),
			id='MaxRSSI')
print "Creating Max RSSI KML"
for row in rows:
        if(row.MaxRSSI <=10):
                colorvalue = "red"
        elif(row.MaxRSSI >10 and row.MaxRSSI <=14):
                colorvalue = "yellow"
        else:
                 colorvalue = "white"
	pm = KML.Placemark(
                        KML.name(row.MaxRSSI),
                        KML.styleUrl(colorvalue),
                        KML.Point(
                                KML.coordinates(str(row.LONGITUDE) + ',' + str(row.LATITUDE))
                                )
                        )
        MaxRSSIFolder.append(pm)
doc.append(MaxRSSIFolder)

fout = open(orgName + 'RSSIOverlay.kml', 'w')
fout.write(etree.tostring(doc, pretty_print=True))
fout.close()
#schema_ogc = Schema("ogckml22.xsd")
#schema_ogc.assertValid(doc)
