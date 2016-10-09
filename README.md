[![Build Status](https://travis-ci.org/dancwilliams/Prefix_List_Script.svg?branch=plist_cicd)](https://travis-ci.org/dancwilliams/Prefix_List_Script)

This script has a few hard coded parts and is basically used for updating some very large prefix lists that exist in an environemnt.

I know the hard coded pices make it custom for my environemnt, but I believe the logic may be reusable.  I am still working on
capturing the descriptions form the test loaded PLs and then adding them back at the end.

The script reads an existing prefix list laod from a text file into a list.

Descriptions and any lines that have a 0.0.0.0/0 network in them are then deleted, as well as any "garbage" lines such as ! lines.

Once that is completed the lines are plit into a list of lists to allow the extraction of the PL name and network statement.

Once the PL name and network have been added to the plList that list is used to form a library based on PL names.

Once we have all the networks in a dictionary and associated with their respective PL name, we can perform a CIDR merge and sort.

After these actions are complete we can sort the dictionary and move to creating the output file.
