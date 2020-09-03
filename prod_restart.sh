#!/bin/sh
rm -f ./settings.ini
ln -s ./settings.ini.prod ./settings.ini
find . -name '*.pyc' | xargs rm -rf
find . -name '__pycache__' | xargs rm -rf
ps -ef | grep hotpot | grep -v grep | awk '{print $2}' | xargs kill -9 > /dev/null 2>&1
mkdir -p logs
nohup python3 hotpot.py >> ./logs/stdout.log 2>&1 &
sleep 0.5
tail -n 20 ./logs/stdout.log