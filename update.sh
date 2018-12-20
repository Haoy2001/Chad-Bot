#!/bin/sh

#stop bot
pkill -f "python3\ bot.py"

#update from github
git pull origin master

#restart bot
python3 bot.py
