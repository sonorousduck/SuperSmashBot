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
        self.epsilon = 0.19073842073576128
        # self.epsilon = 1.0
        # self.epsilon = 0.05
        self.epsilon_decay = .975
        self.epsilon_min = 0.05
        self.gamma = 0.90
        self.learning_rate = .025
        self.learns = 0
        self.model = self.create_model()
        # self.target_model = clone_model(self.model)
        self.rewards = []
        self.averageRewardList = []
        self.averageRewardList = []
        self.oneReward = 0


    def create_model(self):
        model = Sequential()
        model.add(Input(56, ))
        model.add(Dense(128, activation="tanh"))
        model.add(Dense(256, activation="tanh"))
        model.add(Dense(512, activation="tanh"))
        model.add(Dense(256, activation="tanh"))
        model.add(Dense(30, activation="linear"))
        optimizer = Adam(learning_rate=3e-4, decay=1e-5)
        model.compile(optimizer, loss='mse')
        model.summary()
        return model

        # model = Sequential()
        # model.add(Input(56, ))
        # model.add(Dense(128, activation="tanh"))
        # model.add(Dense(256, activation="tanh"))
        # model.add(Dense(30, activation="linear"))
        # optimizer = Adam(learning_rate=3e-4, decay=1e-5)
        # model.compile(optimizer, loss='mse')
        # model.summary()
        # return model


    def act(self, state):
        if np.random.rand() < self.epsilon:
            return random.sample(self.possible_actions, 1)[0]

        x = self.model.predict(state)
        return self.possible_actions[np.argmax(x, axis=1)[0]]


    def adaptiveEGreedy(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
        self.epsilon = max(self.epsilon, self.epsilon_min)

        print(f"Agent Epsilon now at {self.epsilon}")


    def remember(self, state, next_state, action, reward, done, previousAction):
        self.memory.append((state, action, reward, next_state, done, previousAction))

