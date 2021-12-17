import matplotlib.pyplot as plt
import numpy as np

y1 = []
averages = []

with open('deepLevel3.txt') as f:
    while True:
        next_line = f.readline()
        if not next_line:
            break
        y1.append(float(next_line.strip()))
        # if float(next_line.strip()) > 0:
        #     print(float(next_line.strip()))


for i in range(0, len(y1) - 10, 10):
    averages.append(np.mean(y1[i:i+10]))






# with open('smashBot/rewards2.txt') as f:
#     while True:
#         next_line = f.readline()
#         if not next_line:
#             break
#         y2.append(float(next_line.strip()))

# plt.plot(np.arange(0, len(y1)), y1, label='agent')
plt.plot(np.arange(0, len(averages)), averages, label='agent')

# plt.plot(np.arange(0, len(y2)), y2, label='agent 2')
plt.xlabel("10 Binned Epochs Each")
# plt.ylabel("Reward")
plt.ylabel("Avg Reward")
# plt.title("Rewards over Epochs")
plt.title("Average Reward for Deeper Agent over Epochs on Level Three AI")
plt.legend()
# plt.show()
plt.savefig('binnedAvgRewards.png')