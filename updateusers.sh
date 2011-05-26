#!/bin/bash

FILE=/etc/postfix/userlist

ldapsearch -x -D "uid=zimbra,cn=admins,cn=zimbra" -H ldap://mailserver.resolution.resodirect.com:389 -w $PASS -b dc=com | grep mail: | sed 's/mail:\ //' | sed 's/$/\ OK/' > $FILE

if [ ! -s $FILE ];
 then exit
 else postmap $FILE && postfix reload
fi
