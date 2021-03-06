#!/bin/bash

set -x

echo 'Checking for updates to push.'
if grep -q True "run_pl_update"; then
    echo -e "Starting to update gh\n"

    #copy data we're interested in to other place
    #cp -R ORIGINAL_BACKUPS $HOME/ORIGINAL_BACKUPS_NEWcp -R ORIGINAL_BACKUPS $HOME/ORIGINAL_BACKUPS_NEW
    cp -R CHG_SCRIPTS $HOME/CHG_SCRIPTS_NEW
    cp -R ORIGINAL_BACKUPS $HOME/ORIGINAL_BACKUPS_NEW
    cp -R ORIGINAL $HOME/ORIGINAL_NEW
    cp -R EXTRA_SCRIPTS/MANUAL_CREATE/SCRIPTS $HOME/MANUAL_CONFIGS

    #go to home and setup git
    cd $HOME
    git config --global user.email "travis@travis-ci.org"
    git config --global user.name "Travis"

    #using token clone gh-pages branch
    git clone --branch=plist_cicd https://${GH_TOKEN}@github.com/dancwilliams/Prefix_List_Script.git > /dev/null

    #go into diractory and copy data we're interested in to that directory
    cd Prefix_List_Script/ORIGINAL_BACKUPS
    cp -Rf $HOME/ORIGINAL_BACKUPS_NEW/* .
    cd ../../
    cd Prefix_List_Script/ORIGINAL
    cp -Rf $HOME/ORIGINAL_NEW/* .
    cd ../../
    cd Prefix_List_Script/EXTRA_SCRIPTS/MANUAL_CREATE/SCRIPTS
    cp -Rf $HOME/MANUAL_CONFIGS/* .
    cd ../../../../
    cd Prefix_List_Script/CHG_SCRIPTS
    cp -Rf $HOME/CHG_SCRIPTS_NEW/* .
    cd ..
    
    pwd

    git status
    #add, commit and push files

    git add -f .
    git commit -am "Travis build $TRAVIS_BUILD_NUMBER pushed to plist-cicd [ci skip]"
    git push -fq origin plist_cicd > /dev/null
    echo -e "Done Upldating Github\n"
else
  echo "Finished with check.  No Update"
fi
