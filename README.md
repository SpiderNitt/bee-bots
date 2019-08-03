# bee-bots 
Swarm and Blockcahin based 2-d Constructive System
# Technicalities :
Swarm systems are systems where independently
simple entities on collabration with the same entities make
intelligent decisions.
 It is proven that swarms require a decentralised system
to make decisions and block-chain is a well established
decentralised system.
#  The Experiment:
![experiment](https://user-images.githubusercontent.com/47322496/62413868-f0232a80-b631-11e9-8e4c-c1ef56ba4f79.PNG)

1. This is the proposed arena . The Task will be done in the
 following way:
 1. There will be a overhead camera which will scan
the block positions and the bots will get the informations about the
blocks from the blockspace to the workspace .
 2. There should be a set of constraints like a red block
should be on the left and green on the right and so on. This
reduces the central dependency of some entity to sort the work for
the bots.
 The actions that a bot should know are:
 Left,Right,Forward,Backward,pick,place,sensing the
obstacles(other bots) and color detection.
 It is done to make the bots dumb so that they dont know the
whole information about whats going on
 This also brings a lot of randomness into the Task as different
results are occured everytime the same configuration is kept . This
is because of the small differences in the arena everytime occurs
like the speed of the bots would be different etc and a lot of other
differences.
 3. So communication plays a important role here. So
every bot has a copy of all the transcations. Transactions here
mean picking and placing of the blocks. So every bot has a copy
of all the transactions done so far. So according to the constraints
every bot gets to know the location of the block to be placed. A
sample example for communicating between the bots would be as
shown(by using blockchain)

![picture 2](https://user-images.githubusercontent.com/47322496/62413880-2b255e00-b632-11e9-8762-5e395a9551d4.PNG)

To make things interesting, we can make collective
decisions and one bot can help the other by having smarts
contracts.
1. Whenever a bot wants to make decision lets say there are 3-4
block red blocks and the bot is confused which one to pick so it
creates a accountno:(similar to a election ballet paper) and the bot
s have to pay some money into it the the accountno with the
highest balace is the block it chooses.
2. If a particular bot needs a help for picking a block or something
it creates a smart contract for picking and placing the the blocks.

# The organisation of tasks:
To actually test the algorithm before optimising on the factors
like battery and power consumption.
 It will be good to have two microcontrollers.
 The embedded one will be controlled by Nano and the higher
level commands using pyhton so Ras-pi.
 Communication will be done using wifi.
 All the bots will be connected by sockets by having p2p
network among themselves and in a bot the connection will be
serially.
So basic flow will be :
 1.A bot goes to the workspace and checks for the block to be
picked(to be decided on the logic)
 2.It picks a block and feeds it into the path planning module,
which gives the coordinates to be traversed(by taking into the
short paths and obstacles etc). This coordinates are converted into
the simple commads of left right etc and fed to the nano
 3.Nano completes the path and acknowledges to the raspi
once after one task is done and waits for the next task . Here by
tasks it could be like picking a block taking a right or even a
complete path of picking and placing a block. 

# Path planning:
The whole
work+blockspace can be
broken into grids

![path](https://user-images.githubusercontent.com/47322496/62413915-92431280-b632-11e9-99a7-d48847cee281.PNG)

The whole space can be broken into grids and every
grid can have 6 degrees of movement and accordingly using
A* algorithm the shortest path could be found out .

# The bot:
![blockchain_swarm_robotics_bot](https://user-images.githubusercontent.com/47322496/62413924-c1f21a80-b632-11e9-8c26-0b3273a2ab02.png)

This is the rough model of the bot
The picking-mech and and the raspi go on the top floor and
the nano and embedded hardware go on the bottom floor
there will be proximity sensors all around the bot.
Preferably 45 degrees to each other 

# Pick place mechanism:
![pick _ place mechanism](https://user-images.githubusercontent.com/47322496/62413940-0a113d00-b633-11e9-9877-88df0f6ef3be.PNG)

# Timelines:
![Untitled Diagram (1)-1](https://user-images.githubusercontent.com/47322496/62414016-2497e600-b634-11e9-9666-7d36d3a648e8.png)
![Untitled Diagram](https://user-images.githubusercontent.com/47322496/62417208-e1f00100-b667-11e9-8989-ebc56053f965.jpg)
