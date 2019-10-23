import random
from collections import defaultdict


def spit_weighted_number(length):
    random_array = []
    for i in range(1, length + 1):
        random_array.append([i] * (length + 1 - i))
    flattened = [item for sublist in random_array for item in sublist]
    return random.choice(flattened)
    # return flattened


score_dict = defaultdict(int)
for i in range(10000):
    val = spit_weighted_number(5)
    score_dict[val] += 1
    # score_dict[val].update()

# array = spit_weighted_number(5)
for i in sorted(score_dict.keys()):
    print(i, score_dict[i])
