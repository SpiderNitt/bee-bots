import json
from bot_model import bot
import multiprocessing as mp
import sys

bot_config_filename = "bots_config.json"
json_string = open(bot_config_filename).read()
bot_configs = json.loads(json_string)
print(bot_configs)
mp_array = []


def bot_init(config):
    ebot1 = bot(config["port"], config, 0, 0)
    # ebot1.initialise_config(config)
    # ebot1.pick()
    ebot1.Follow_path([0.5, 2, 0.0])
    # ebot1.place()
    ebot1.Follow_path([0.25, 1, 0])
    ebot1.place_from_other_sceme(21, [0.5, 2, 0.0])


for (i, config) in enumerate(bot_configs):
    if i == int(sys.argv[1]) - 1:
        bot_init(config)

# for config in bot_configs:
#     mp_array.append(mp.Process(target=bot_init, args=(config,)))

# for p in mp_array:
#     p.start()
#     # .join()

# for p in mp_array:
#     p.join()

# for config in bot_configs:
#     print(config)
#     print(config["bot"])
#     if config["bot"] == "eBot1":
#         bot_init(config)


print("simulation complete")

