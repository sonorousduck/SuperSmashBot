from collections import deque


class Memory:
    def __init__(self, max_memory_len):
        self.states = deque(maxlen=max_memory_len)
        self.actions = deque(maxlen=max_memory_len)
        self.rewards = deque(maxlen=max_memory_len)
        self.next_state = deque(maxlen=max_memory_len)
        self.done = deque(maxlen=max_memory_len)

    def add_experience(self, state, action, reward, next_state, done):
        self.states.append(state)
        self.actions.append(action)
        self.rewards.append(reward)
        self.next_state.append(next_state)
        self.done.append(done)

