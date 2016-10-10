#!/bin/bash

set -x

echo "Cleaning for demo mode"

git rm CHG_SCRIPTS/CHG*

git rm ORIGINAL_BACKUPS/orig*

cp EXTRA_SCRIPTS/INITIAL_YAML/initial_load.yaml ORIGINAL/original.yaml

echo "Please perform commit [ci skip] in comment and push upstream"
