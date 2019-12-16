#!/usr/bin/env bash

source "/home/karthik/bee/bin/activate"
cd  "/home/karthik/bee-bots/integration/" 


gnome-terminal -e 'bash -c "python3 Bot.py 1"' &
gnome-terminal -e 'bash -c "python3 Bot.py 2"' &
gnome-terminal -e 'bash -c "python3 Bot.py 3"' &



exec bash


