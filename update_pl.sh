#!/bin/bash

set -e

echo 'Testing run_pl_update'

if grep -q True "run_pl_update"; then
  echo 'Running Update'
  mkdir ORIGINAL_BACKUPS
  mkdir CHG_SCRIPTS
  mkdir ORIGINAL_BACKUPS_NEW
  mkdir CHG_SCRIPTS_NEW
  echo ls -ltr
  python pl_yaml_processing.py
fi

echo 'No Update'
