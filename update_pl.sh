#!/bin/bash

set -x

echo 'Testing run_pl_update'

if grep -q True "run_pl_update"; then
  echo 'Running Update'
  mkdir ORIGINAL_BACKUPS_NEW
  mkdir CHG_SCRIPTS_NEW
  mkdir ORIGINAL_NEW
  mkdir MANUAL_CONFIGS
  python pl_yaml_processing.py
  ret=$?
  if [ $ret -ne 0 ]; then
     #Handle failure
     exit 1
  fi
  cd CHG_SCRIPTS
  cp $(ls -1t | head -1) ../EXTRA_SCRIPTS/MANUAL_CREATE/config.yaml
  cd ..
  python EXTRA_SCRIPTS/MANUAL_CREATE/generate_config.py
  ret=$?
  if [ $ret -ne 0 ]; then
     #Handle failure
     exit 1
  fi
else
  echo 'No Update'
fi
