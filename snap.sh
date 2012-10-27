#!/bin/sh
mkdir -p ~/screenshots
cd ~/screenshots
scrot --select --exec 'climgur.py $f'
