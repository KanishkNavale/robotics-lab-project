from rai_gym.env import RAI_Env
from rl_agents.DDPG import Agent
import os
import numpy as np
import copy
import torch as T

if __name__ == '__main__':

    # Init. Environment
    env = RAI_Env(reward_type='dense')
    env.reset()

    # Init. Datapath
    data_path = os.path.dirname(os.path.abspath(__file__)) + '/data/'
    agent_path = os.path.abspath("trained_actors")

    # Init. Training
    score_history = []
    avg_history = []
    n_games = 100

    # Init. Agent
    agent = Agent(env, data_path, n_games)
    agent.actor.load_model(agent_path + '/')

    for i in range(n_games):
        score = 0
        distance = 0
        done = False

        # Initial Reset of Environment
        OBS = env.reset()

        while not done:
            # Unpack the observation
            y, target = OBS.values()
            obs = np.concatenate((y, target))

            # Choose agent based action & make a transition
            action = agent.choose_action(obs)
            next_OBS, reward, done = env.step(action)

            next_y, next_target = next_OBS.values()
            next_obs = np.concatenate((next_y, next_target))

            OBS = copy.deepcopy(next_OBS)
            score += reward
            distance = -reward * 1e3

        score_history.append(score)
        avg_score = np.mean(score_history[-100:])
        avg_history.append(avg_score)

        print(f'Episode:{i}'
              f'\t ACC. Rewards: {score:3.2f}'
              f'\t AVG. Rewards: {avg_score:3.2f}'
              f'\t Final Distance Error: {distance:3.2f}')

        # Save the score log
        np.save(data_path + 'score_history', score_history, allow_pickle=False)
        np.save(data_path + 'avg_history', avg_history, allow_pickle=False)
