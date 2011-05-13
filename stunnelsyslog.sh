#!/bin/bash

apt-get install stunnel4 -y
mkdir /var/lib/stunnel4/certs

mv ~/$HOSTNAME.pem /etc/ssl/certs/
mv ~/$HOSTNAME.key /etc/ssl/private/
mv ~/logger.pem /var/lib/stunnel4/certs/`openssl x509 -hash -noout -in ~/logger.pem`.0

sed -i -e 's/;client/client/' -e 's/;CApath\ =/CApath\ =/' -e "s/cert\ =\ \/etc\/ssl\/certs\/stunnel.pem/cert\ =\ \/etc\/ssl\/certs\/$HOSTNAME.pem/" -e "s/;key\ =\ \/etc\/ssl\/certs\/stunnel.pem/key\ =\ \/etc\/ssl\/private\/$HOSTNAME.key/" -e 's/;verify\ =\ 2/verify\ =\ 3/' /etc/stunnel/stunnel.conf

echo "
[relp]
accept = 127.0.0.1:2514
connect = logger:62514" >> /etc/stunnel/stunnel.conf

sed -i 's/:omrelp:10.11.7.30:/:omrelp:127.0.0.1:/' /etc/rsyslog.conf

sed -i 's/ENABLED=0/ENABLED=1/' /etc/default/stunnel4

/etc/init.d/stunnel4 restart
service rsyslog restart

exit
