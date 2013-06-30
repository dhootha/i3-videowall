i3-videowall
============

This is a very simple script to play multiple videos at a time in a video wall. I mainly wrote it as an excuse to play with i3-py which presents an interface to the i3 window manager.

Usage:
======

find . -iname "*.avi" -or -iname "*.mp4" -print0 | xargs -0 i3-videowall.py -n 6 -s random

Play videos, 6 at a time selecting a random window to split.

find . -iname "*.avi" -or -iname "*.mp4" -or -iname "*.vob" -print0 | sort -R | xargs -0 i3-videowall.py -n 12

Play videos, 12 at a time in random order selecting the biggest window to split
