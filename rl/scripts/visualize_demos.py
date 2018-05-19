#!/usr/bin/env python3

import argparse
import gym
import levels
import time
import torch

import utils

# Parse arguments

parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True,
                    help="name of the environment to be run (REQUIRED)")
parser.add_argument("--rl-generated", action="store_true", default=False,
                    help="if not specified, the human demos will be loaded")
args = parser.parse_args()

# Load the demos and the corresponding information

demos = utils.load_demos(args.env, human=not args.rl_generated)

# Generate environment

env = gym.make(args.env)
env.seed(1)

# Define the demonstrator

demonstrator = utils.Demonstrator(demos)

# Start running the demonstrator

obs = env.reset()

while True:

    renderer = env.render("human")
    potential_error = "The observations do not match"
    assert utils.check_2_obs_equal(obs, demonstrator.get_observation()), potential_error

    action = demonstrator.get_action()
    obs, reward, done, _ = env.step(action)
    demonstrator.move_to_next_step()

    if done:
        obs = env.reset()
        print("Mission:", obs["mission"])
        next_instance = demonstrator.move_to_next_instance()
        if not next_instance:
            break

    time.sleep(0.1)

    if renderer.window is None:
        break


