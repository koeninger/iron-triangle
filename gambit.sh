#!/bin/bash

python3 ./iron_triangle.py | /Applications/Gambit.app/Contents/MacOS/gambit-lcp -d3 | tr , '\n'
