#!/usr/bin/env bash
set -e

if [ -z ${TASK} ]; then
  echo "No task provided"
  exit 2
fi

if [ ${TASK} == 'checks' ]; then
  tox -e lint
elif [ ${TASK} == 'integration' ]; then
  sudo tox -e py27  # If we need more python versions, add them here.
else
  echo "Invalid task: ${TASK}"
  exit 2
fi
