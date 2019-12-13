# :rocket: How to set it up:

- Clone the repository and enter into the `integration` folder.
- Open V-REP pro-edu
- Load integration_test.ttt scene that is in this folder
- Create a virtual environment for python3. (`pip3 install virtualenv, virtualenv -p /usr/bin/python3 env`)
- activate the virtual environment. (`source env/bin/activate`)
- Install the requirements. (`pip install -r requirements.txt` ) (It can be pip here instead of pip3)
- Run the simulation in V-REP.
- Run the following command. (`python Bot.py 1`)
- The number after Bot.py is the number of the bot that you are initialising. To run second bot, you have to do `python Bot.py 2` in another terminal.
- The scene supports 3 bots. So create three different terminals, and run `python Bot.py <bot-number>` in each.
- Watch the bees do their job.

(change configration files accordingly if ou want to add more blocks.)

## :honeybee: :honeybee: What it is:

- A blockchain based swarm robotics model build using V-REP (Lua), blockchain and sockets.

## :house: Built using:

- Python 3.6.8
- V-REP
- Lua

Weaved with :spider_web: by Team Bee-Bots of [:spider:](https://spider.nitt.edu)
