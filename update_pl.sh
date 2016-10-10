#!/bin/bash

set -e

echo 'Testing run_pl_update'

if grep -q True "run_pl_update"; then
  echo 'Running Update'
  mkdir ORIGINAL_BACKUPS_NEW
  mkdir CHG_SCRIPTS_NEW
  python pl_yaml_processing.py
  ret=$?
  if [ $ret -ne 0 ]; then
     #Handle failure
     exit 1
  fi
else
  echo 'No Update'
fi
