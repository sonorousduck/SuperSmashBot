import matplotlib.pyplot as plt
import numpy as np

y1 = []
averages = []

with open('rewards2.txt') as f:
    while True:
        next_line = f.readline()
        if not next_line:
            break
        y1.append(float(next_line.strip()))


for i in range(len(y1) - 10):
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
plt.xlabel("Epochs")
# plt.ylabel("Reward")
plt.ylabel("Avg Reward")
# plt.title("Rewards over Epochs")
plt.title("Average reward over Epochs")
plt.legend()
plt.show()