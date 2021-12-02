import aiohttp
from threading import Thread

import requests


class GetThread(Thread):
    def __init__(self):
        Thread.__init__(self)


    def run(self):
        url = 'http://127.0.0.1:9000/smashBot/getAgent'
        with requests.get(url, stream=True) as r:
            with open("recentweights.hdf5", 'wb') as f:
                for chunk in r.iter_content(chunk_size=16 * 1024):
                    f.write(chunk)

# def postAgent(agentStates, agentNextStates, agentActions, agentRewards, gameDones, agent):
#     with aiohttp.ClientSession() as session:
#         url = "http://127.0.0.1:8000/smashBot/postState/"
#         with session.post(url=url, json={'states': agentStates, 'actions': agentActions, 'rewards': agentRewards,
#                         'nextStates': agentNextStates, 'dones': gameDones, 'agent': agent}) as resp:
#             return resp


