import aiohttp
from threading import Thread
import requests
import numpy as np


class PostThread(Thread):
    def __init__(self, agentStates, agentNextStates, agentActions, agentRewards, gameDones, agent, previousActions):
        Thread.__init__(self)
        self.agentStates = agentStates
        self.agentNextStates = agentNextStates
        self.agentActions = agentActions
        self.agentRewards = agentRewards
        self.gameDones = gameDones
        self.agent = agent
        self.previousActions = previousActions

    def run(self):
        url = "http://127.0.0.1:9000/smashBot/postState/"
        agentStates = np.array(self.agentStates)
        agentStates = agentStates.tolist()
        agentNextStates = np.array(self.agentNextStates)
        agentNextStates = agentNextStates.tolist()

        requests.post(url=url, json={'states': agentStates, 'actions': self.agentActions, 'rewards': self.agentRewards,
                        'nextStates': agentNextStates, 'dones': self.gameDones, 'agent': self.agent, 'previousActions': self.previousActions})


# def postAgent(agentStates, agentNextStates, agentActions, agentRewards, gameDones, agent):
#     with aiohttp.ClientSession() as session:
#         url = "http://127.0.0.1:8000/smashBot/postState/"
#         with session.post(url=url, json={'states': agentStates, 'actions': agentActions, 'rewards': agentRewards,
#                         'nextStates': agentNextStates, 'dones': gameDones, 'agent': agent}) as resp:
#             return resp


