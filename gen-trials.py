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
num_trials_t = 220 # total
num_trials_s = 100 # stable - as a second block
num_trials_v = 120 # volatile - volatile first condition
# 1.trial index
trial_index = range(220)

# 2.block
block = ["first"]*num_trials_v+["second"]*num_trials_s

# 3.conditions
condition_vf = ["vf"]*num_trials_t
condition_sf = ["sf"]*num_trials_t

# 3.stimuli position
stimuli = [["green","blue"]]*num_trials_t
left_pos = []
right_pos = []
for pair in stimuli:
    left, right = random.sample(pair, len(pair))
    left_pos.append(left)
    right_pos.append(right)

# 5.targets
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

# targets parameters
gren_probs_v = [0.7, 0.3, 0.9, 0.1, 0.7] # prob of green in volatile block
gren_probs_s = [0.2, 0.8] # prob of green on stable blocks
sub_blocks_vf = [20, 30, 20, 30, 20] # trials by sub-block volatile first
sub_blocks_sf = [120, 100] # trials by sub-block volatile first

# targets sub-blocks volatile block
sub_vol_1 = sub_blocks(gren_probs_v[0], sub_blocks_vf[0])
sub_vol_2 = sub_blocks(gren_probs_v[1], sub_blocks_vf[1])
sub_vol_3 = sub_blocks(gren_probs_v[2], sub_blocks_vf[2])
sub_vol_4 = sub_blocks(gren_probs_v[3], sub_blocks_vf[3])
sub_vol_5 = sub_blocks(gren_probs_v[4], sub_blocks_vf[4])

# targets sub-blocks stable block
sub_s_1 = sub_blocks(gren_probs_s[0], sub_blocks_sf[0]) # first stable block
sub_s_2 = sub_blocks(gren_probs_s[1], sub_blocks_sf[1]) # second stable block

# 5.1 concatenate targets volatile first condition
target_vf = sub_vol_1+sub_vol_2+sub_vol_3+sub_vol_4+sub_vol_5+sub_s_2
# 5.2 concatenate targets stable first condition
target_sf = sub_s_1+sub_s_2

# 6. expected key
def expectedKey(target_condition):
    """Generate expected key (left or right) list

    Keyword arguments:
    target_condition -- target_vf = volatile first; target_sf = stable first
    """
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

# 6.1 expected key for volatile first condition
expected_key_vf = expectedKey(target_vf)
# 6.2 expected key for stable first condition
expected_key_sf = expectedKey(target_sf)

# 7. reward size
np.random.seed(0)
reward_size_left = np.random.randint(99, size=(1, num_trials_t))
reward_size_left = (reward_size_left.tolist())[0] # to strip extra brackets
np.random.seed(1)
reward_size_right = np.random.randint(99, size=(1, num_trials_t))
reward_size_right = (reward_size_right.tolist())[0] # to strip extra brackets

# 8. probability of green
gren_probs_v_list = [[0.7], [0.3], [0.9], [0.1], [0.7]]
sub_blocks_vf = [20, 30, 20, 30, 20] # trials by sub-block volatile first
green_prob_vf = [] # list prob green vf
for pair in zip(gren_probs_v_list, sub_blocks_vf):
    green_prob_vf.extend(pair[0]*pair[1])
green_prob_vf.extend([0.8]*num_trials_s)

green_prob_sf = [0.2]*num_trials_v+[0.8]*num_trials_s # list prob green sf

############### TODO add header ###########################
header = ["trial_index", "block", "condition", "left_stim", "right_stim",\
            "target_position", "expected_key", "reward_left", "reward_right",\
            "green_probability"]

# write to csv for volatile first condition
with open("vf_trials.csv","w") as fh:
    #fh.write(",".join(header))
    fh.write('\n'.join('%s, %s, %s, %s, %s, %s, %s, %s, %s, %s'\
            % x for x in zip(trial_index, block, condition_vf, left_pos,\
            right_pos, target_vf, expected_key_vf,\
            reward_size_left, reward_size_right, green_prob_vf)))

# write to csv for stable first condition
with open("sf_trials.csv","w") as fh:
    fh.write('\n'.join('%s, %s, %s, %s, %s, %s, %s,' % x for x in zip(trial_index, \
            block, condition_sf, left_pos, right_pos, target_sf, expected_key_sf,\
            reward_size_left, reward_size_right, green_prob_sf)))

for x in
