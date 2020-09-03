#!/bin/sh
rm -f ./settings.ini
ln -s ./settings.ini.prod ./settings.ini
ps -ef | grep hotpot | grep -v grep | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
python3 hotpot.py