#!/bin/bash

FILE=/etc/opennms/poll-outages.xml
DATE1=`date +%d-%b-%Y\ %k:%M:%S`
DATE2=`date --date='+10 minutes' +%d-%b-%Y\ %k:%M:%S`
	sed -i -e "s/begins=\".*\ .*\"\ /begins=\"$DATE1\"\ /g" -e "s/ends=\".*\ .*\"/ends=\"$DATE2\"/g" $FILE

	/usr/share/opennms/bin/send-event.pl uei.opennms.org/internal/schedOutagesChanged

