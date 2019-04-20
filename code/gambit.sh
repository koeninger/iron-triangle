#!/bin/bash

python ./iron_triangle.py > all.nfg
cat all.nfg | /Applications/Gambit.app/Contents/MacOS/gambit-lcp -d3 | tr , '\n'
