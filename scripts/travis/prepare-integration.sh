#!/usr/bin/env bash
set -e

if [ "$(whoami)" != 'root' ]; then
    echo 'Please run with sudo'
    exit 1
fi

TESTUSER='pammer'
TESTPASSWD='spammer'  # If you are changing this, fix the tests as well.

create_user() {
  if [ $(id -u ${TESTUSER} &> /devnull; echo $?) != 0 ]
  then
    echo "########################################################################################"
    echo "############################# Creating test user #######################################"
    echo "########################################################################################"
    SALT='mkpasswd'
    useradd ${TESTUSER} -p `mkpasswd --method=sha-512 $TESTPASSWD ${SALT}`
  fi
}

# mkpasswd requires whois package
apt-get update
apt-get install -y whois

create_user
