import math
from collections import deque

from keras.layers import Flatten, Reshape
from tensorflow.keras.models import Sequential, clone_model
from tensorflow.keras.layers import Dense, Dropout, Input, LSTM, Embedding, BatchNormalization
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
import numpy as np
import random

from moveset import Moveset
from memory import Memory


class Agent():
    def __init__(self):
        # Moveset.__init__(self, controller)
        # self.memory = deque(maxlen=50000)
        # self.controller = controller
        # self.moveset = Moveset(controller)
        self.possible_actions = [i for i in range(30)]
        # self.epsilon = 0.5397473191725894
        self.epsilon = 0.05
        # self.epsilon = 0.9848718460076812
        self.epsilon_decay = .9995
        self.epsilon_min = 0.05
        self.gamma = 0.90
        # self.learning_rate = 0.0025
        self.learning_rate = .025
        self.batch_size = 256
        self.learns = 0
        self.model = self.create_model()
        self.target_model = clone_model(self.model)
        self.rewards = []
        self.averageRewardList = []
        self.oneReward = 0


    def create_model(self):
        model = Sequential()
        model.add(Input(26,))
        # model.add(Reshape((1, 44)))
        # model.add(Embedding(44, 128))
        # model.add(LSTM(128, return_sequences=True))
        # model.add(LSTM(256))
        # model.add(Flatten())

        model.add(Dense(128, activation="swish"))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        model.add(Dense(512, activation="swish"))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        model.add(Dense(1024, activation="swish"))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        model.add(Dense(512, activation="swish"))
        model.add(BatchNormalization())
        model.add(Dropout(0.4))
        model.add(Dense(30, activation="softmax"))
        optimizer = Adam(self.learning_rate)
        model.compile(optimizer, loss='mse')
        model.summary()
        return model


    def act(self, state):
        if np.random.rand() < self.epsilon:
            return random.sample(self.possible_actions, 1)[0]

        x = self.model.predict(state)
        return self.possible_actions[np.argmax(x, axis=1)[0]]


    def adaptiveEGreedy(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon, self.epsilon_min)

        # if len(self.memory) > self.batch_size:
        #     self.rewards.append(self.oneReward)

        # if len(self.rewards) > 250:
        #     self.averageRewardList.append(np.mean(self.rewards[:-250]))
        # else:
        #     self.averageRewardList.append(np.mean(self.rewards))
        #
        # self.oneReward = 0
        print(f"Agent Epsilon now at {self.epsilon}")


    def remember(self, state, next_state, action, reward, done):
        self.memory.append((state, action, reward, next_state, done))





