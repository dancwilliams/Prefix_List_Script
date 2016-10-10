#!/bin/bash

echo 'Testing run_pl_update'

if grep -q True "run_pl_update"; then
  echo 'Running Update'
  python pl_yaml_processing.py
fi

echo 'No Update'
