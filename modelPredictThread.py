import random

import aiohttp
import multiprocessing as mp
import numpy as np
import requests

def predict(agentStates, model, possibleActions, epsilon, queue):
    if np.random.rand() < epsilon:
        # print(self.possible_actions)
        # print(random.sample(self.possible_actions, 1)[0])
        queue.put(random.sample(possibleActions, 1)[0])

        # return random.sample(self.possible_actions, 1)[0]
    else:
        x = model.predict(agentStates)
        queue.put(possibleActions[np.argmax(x, axis=1)[0]])

#
# class PredictThread(Thread):
#     def __init__(self, agentStates, model, possibleActions, epsilon, pos, resultList):
#         Thread.__init__(self)
#         self.agentStates = agentStates
#         self.model = model
#         self.possible_actions = range(possibleActions)
#         self.epsilon = epsilon
#         self.pos = pos
#         self.resultList = resultList
#
#     def run(self):
#         if np.random.rand() < self.epsilon:
#             # print(self.possible_actions)
#             # print(random.sample(self.possible_actions, 1)[0])
#             self.resultList[self.pos] = random.sample(self.possible_actions, 1)[0]
#
#             # return random.sample(self.possible_actions, 1)[0]
#         else:
#             x = self.model.predict(self.agentStates)
#             self.resultList[self.pos] = self.possible_actions[np.argmax(x, axis=1)[0]]


        # url = "http://127.0.0.1:8000/smashBot/postState/"
        # requests.post(url=url, json={'states': self.agentStates, 'actions': self.agentActions, 'rewards': self.agentRewards,
        #                 'nextStates': self.agentNextStates, 'dones': self.gameDones, 'agent': self.agent})


# def postAgent(agentStates, agentNextStates, agentActions, agentRewards, gameDones, agent):
#     with aiohttp.ClientSession() as session:
#         url = "http://127.0.0.1:8000/smashBot/postState/"
#         with session.post(url=url, json={'states': agentStates, 'actions': agentActions, 'rewards': agentRewards,
#                         'nextStates': agentNextStates, 'dones': gameDones, 'agent': agent}) as resp:
#             return resp


