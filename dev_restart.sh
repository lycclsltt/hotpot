#!/bin/sh
rm -f ./settings.ini
ln -s ./settings.ini.dev ./settings.ini
find . -name '*.py' | xargs yapf -i
ps -ef | grep hotpot | grep -v grep | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
mkdir -p ./logs
python3 hotpot.py