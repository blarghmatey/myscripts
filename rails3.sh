#!/bin/bash

USER=env | grep USERNAME | sed 's/USERNAME=//'
red='\E[31;40m'

sudo apt-get update
echo -e $red "This is going to take a while. You might want to take a nap or something..."
tput sgr0
sleep 5
sudo apt-get -y install curl git-core libruby1.8 zlib1g-dev libssl-dev libreadline5-dev build-essential python-software-properties sysvbanner
wget http://rvm.beginrescueend.com/releases/rvm-1.0.1.tar.gz
tar -xvzf rvm-1.0.1.tar.gz
cd rvm-1.0.1
./install
echo "[[ -s "$HOME/.rvm/scripts/rvm" ]] && source "$HOME/.rvm/scripts/rvm"" >> /home/$USER/.bashrc
. /home/$USER/.bashrc
rvm install ruby-1.8.7
rvm use ruby-1.8.7 --default
sudo add-apt-repository ppa:ubuntu-on-rails
sudo apt-get update
sudo apt-get -y install ruby rubygems irb ri rdoc rake build-essential ruby1.8-dev libopenssl-ruby sqlite3 libsqlite3-dev
export PATH=/var/lib/gems/1.8/bin:$PATH
sudo chmod -R 777 /var/lib/gems/1.8
gem install sqlite3
rvm install ruby-1.9.2
rvm use ruby-1.9.2 --default
gem install rails sqlite3
banner ALL DONE!
