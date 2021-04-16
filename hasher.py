#!/usr/bin/env python3
###
### MD5 HASHER
###
### Takes in a text file and writes the MD5 hash of each line
### to another text file.
###
### Comp 27: How Systems Fail
### C.R. Calabrese, February 2021
###
### Usage: hasher.py input.txt output.txt
###
### Note: Output will be overwritten

import sys, hashlib

infile  = open(sys.argv[1], "r")
outfile = open(sys.argv[2], "w")

for line in infile:
    ## Blank lines won't be hashed.
    ## if the first character is #, the line won't be hashed. This allows
    ## us to comment on our password files.
    if line != '\n' and line[0] != '#':
        outfile.write(hashlib.md5(line.strip('\n').encode('ascii')).hexdigest())
        outfile.write('\n')
