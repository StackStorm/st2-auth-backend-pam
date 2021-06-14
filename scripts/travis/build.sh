#!/usr/bin/env bash
set -e

if [ -z ${TASK} ]; then
  echo "No task provided"
  exit 2
fi

if [ ${TASK} == 'checks' ]; then
  tox -e lint
elif [ ${TASK} == 'integration' ]; then
  set -x
  # If we need more python versions, add them here.
  if [ -d /home/travis/virtualenv/python3.8/bin ]; then
    sudo bash -c "source /home/travis/virtualenv/python3.8/bin/activate && tox -e py38" || exit $?
  else
    sudo bash -c "source /home/travis/virtualenv/python3.6/bin/activate && tox -e py27,py36" || exit $?
  fi
else
  echo "Invalid task: ${TASK}"
  exit 2
fi
