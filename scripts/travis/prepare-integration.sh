#!/usr/bin/env bash
set -e

if [ "$(whoami)" != 'root' ]; then
    echo 'Please run with sudo'
    exit 1
fi

TESTUSER='pammer'
TESTPASSWD='spammer'

create_user() {
  if [ $(id -u ${TESTUSER} &> /devnull; echo $?) != 0 ]
  then
    echo "########################################################################################"
    SALT='mkpasswd'
    useradd ${TESTUSER} -p `mkpasswd --method=sha-512 $TESTPASSWD ${SALT}`
  fi
}

# mkpasswd requires whois package
apt-get install -y whois

create_user
