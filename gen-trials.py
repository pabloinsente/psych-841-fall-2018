# Generate Trials for PLS-FU-2 study
# Author: Pablo Caceres
# Date  : 11/07/18
import random
import numpy as np
"""
Requirements:
    1. Python 3.7
    2. Install X packages
    3. X files

Inputs:
    1. xxx
    2. yyy
    3. ffff

Output:
    1. N x M .cvs file
    2. Variables: x, y, z, t
"""

# parameters

# number of trials
num_trials_t = 220
num_trials_s = 100
num_trials_v = 120
# trial index
trial_index = range(220)

# block
block = ["first", "second"]

# sub-blocks
sub_blocks_first = [""]
sub_blocks_second = [""]

# conditions
conditions = ["vf", "sf"]

# stimuli position
stimuli = [["green","blue"]]*num_trials_t
len(stimuli)
left_pos = []
right_pos = []
for pair in stimuli:
    left, right = random.sample(pair, len(pair))
    left_pos.append(left)
    right_pos.append(right)

# targets
def sub_blocks(green_prob, num_trials):
    """Generate sub_blocks for meta-blocks of the task.

    Keyword arguments:
    green_prob -- probability of green in a given sub-block
                  float between 0.1 and 1.0
    num_trials -- number of trials in a given sub-block
    """
    green_trials = round(num_trials*green_prob)
    blue_trials = round(num_trials*(1-green_prob))
    target = ["green"]*green_trials+["blue"]*blue_trials
    random.seed(100)
    target = random.sample(target, len(target))
    return target

# targets volatile block
sub_vol_1 = sub_blocks(0.7, 20)
sub_vol_2 = sub_blocks(0.3, 30)
sub_vol_3 = sub_blocks(0.9, 20)
sub_vol_4 = sub_blocks(0.1, 30)
sub_vol_5 = sub_blocks(0.7, 20)

# targets stable block
sub_s_1 = sub_blocks(0.2, 120)
sub_s_2 = sub_blocks(0.8, 100)

# target volatile first condition
target_vf = sub_vol_1+sub_vol_2+sub_vol_3+sub_vol_4+sub_vol_5+sub_s_2
target_sf = sub_s_1+sub_s_2

# probability of green
############## TODO = list 220 #############
green_prob = []

# expected key
def expectedKey(target_condition):
    expected_key = []
    for key in zip(left_pos, target_condition):
        if key[0] == "green" and key[1] == "green":
            expected_key.append("left")
        elif key[0] == "green" and key[1] == "blue":
            expected_key.append("right")
        elif key[0] == "blue" and key[1] == "blue":
            expected_key.append("left")
        elif key[0] == "blue" and key[1] == "green":
            expected_key.append("right")
    return expected_key

# expected key for volatile first condition
expected_key_vf = expectedKey(target_vf)
# expected key for stable first condition
expected_key_sf = expectedKey(target_sf)

# reward size
np.random.seed(0)
reward_size_left = np.random.randint(99, size=(1, num_trials_t))
reward_size_left = (reward_size_left.tolist())[0] # to strip extra brackets
np.random.seed(1)
reward_size_right = np.random.randint(99, size=(1, num_trials_t))
reward_size_right = (reward_size_right.tolist())[0] # to strip extra brackets

############### TODO add header ###########################

# write to csv for volatile first condition
with open("vf_trials.csv","w") as fh:
    fh.write('\n'.join('%s, %s, %s, %s, %s, %s, %s,' % x for x in zip(trial_index, \
            left_pos, right_pos, target_vf, expected_key_vf,\
            reward_size_left, reward_size_right)))

# write to csv for volatile first condition
with open("sf_trials.csv","w") as fh:
    fh.write('\n'.join('%s, %s, %s, %s, %s, %s, %s,' % x for x in zip(trial_index, \
            left_pos, right_pos, target_sf, expected_key_sf,\
            reward_size_left, reward_size_right)))
