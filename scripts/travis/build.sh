#!/usr/bin/env bash
set -e

if [ -z ${TASK} ]; then
  echo "No task provided"
  exit 2
fi

if [ ${TASK} == 'checks' ]; then
  tox -e lint
elif [ ${TASK} == 'integration' ]; then
  # If we need more python versions, add them here.
  sudo bash -c "source /home/travis/virtualenv/python3.6/bin/activate && tox -e py27,py36"
else
  echo "Invalid task: ${TASK}"
  exit 2
fi
