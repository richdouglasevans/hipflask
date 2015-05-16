#!/usr/bin/env bash

<%= import 'ubuntu.sh' %>

apt-mirror-pick 'uk'
apt-packages-update
apt-packages-install vim

if [ ! -f /home/vagrant/hyperion/setup-mongo ];
then
  apt-packages-repository 'deb http://downloads-distro.mongodb.org/repo/ubuntu-upstart dist 10gen' '7F0CEB10'
  apt-packages-update
  apt-packages-install mongodb-10gen
  touch /home/vagrant/hyperion/setup-mongo
fi
