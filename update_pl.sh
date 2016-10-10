#!/bin/bash

echo 'Testing run_pl_update'

if grep -q True "run_pl_update"; then
  echo 'Running Update'
  mkdir ORIGINAL_BACKUPS
  mkdir CHG_SCRIPTS
  python pl_yaml_processing.py
fi

echo 'No Update'
