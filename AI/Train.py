import numpy as np
import random
import json
from itertools import islice
import os
from Body import *
from Fung import *

env = Env()
agent = Agent()

env.getState()

episodes = 1000
winner_history = []


for episode in range(episodes):
    isDone = False
    state = env.reset()
    prevState = state
    prevAction = -1
    isShouldLearn = False

    if episode % 1000 == 0:
        print("Random episode:", episode)

    while not isDone:
        state = env.getState()

        if not env.isXTurn:
            state = swapSide(state)

        hash = stateToHash(state)
        possibleActions = getPossibilityActions(hash)
        idx = [i for i in range(len(possibleActions))if possibleActions[i] == 1]
        action = random.choice(idx)

        nextState, reward, isDone, _ = env.act(action)
        # env.showBoard()

        # if X turn mean before act is not X turn
        if env.isXTurn:
            nextState = swapSide(nextState)

        if isShouldLearn:
            if isDone and not env.checkDraw():
                prevReward = -1
            elif isDone and env.checkDraw():
                prevReward = 0.5
            agent.learn(prevState, swapSide(nextState),
                        prevAction, prevReward, isDone)
            agent.learn(rotage(prevState, 1), rotage(
                swapSide(nextState), 1), rotageAction(prevAction, 1), prevReward, isDone)
            agent.learn(rotage(prevState, 2), rotage(
                swapSide(nextState), 2), rotageAction(prevAction, 2), prevReward, isDone)
            agent.learn(rotage(prevState, 3), rotage(
                swapSide(nextState), 3), rotageAction(prevAction, 3), prevReward, isDone)

        if isDone:
            agent.learn(state, nextState, action, reward, isDone)
            agent.learn(rotage(state, 1), rotage(nextState, 1),
                        rotageAction(action, 1), reward, isDone)
            agent.learn(rotage(state, 2), rotage(nextState, 2),
                        rotageAction(action, 2), reward, isDone)
            agent.learn(rotage(state, 3), rotage(nextState, 3),
                        rotageAction(action, 3), reward, isDone)

        prevState = state
        prevAction = action
        prevReward = reward
        isShouldLearn = True

    winner_history.append(env.checkWin())

for episode in range(episodes):
    isDone = False
    state = env.reset()
    prevState = state
    prevAction = -1
    isShouldLearn = False

    if episode % 1000 == 0:
        print("AI episode:", episode)

    while not isDone:
        state = env.getState()

        if not env.isXTurn:
            state = swapSide(state)

        action = agent.act(state)
        nextState, reward, isDone, _ = env.act(action)
        # env.showBoard()

        # if X turn mean before act is not X turn
        if env.isXTurn:
            nextState = swapSide(nextState)

        if isShouldLearn:
            if isDone and not env.checkDraw():
                prevReward = -1
            elif isDone and env.checkDraw():
                prevReward = 0.5
            agent.learn(prevState, swapSide(nextState),
                        prevAction, prevReward, isDone)
            agent.learn(rotage(prevState, 1), rotage(
                swapSide(nextState), 1), rotageAction(prevAction, 1), prevReward, isDone)
            agent.learn(rotage(prevState, 2), rotage(
                swapSide(nextState), 2), rotageAction(prevAction, 2), prevReward, isDone)
            agent.learn(rotage(prevState, 3), rotage(
                swapSide(nextState), 3), rotageAction(prevAction, 3), prevReward, isDone)

        if isDone:
            agent.learn(state, nextState, action, reward, isDone)
            agent.learn(rotage(state, 1), rotage(nextState, 1),
                        rotageAction(action, 1), reward, isDone)
            agent.learn(rotage(state, 2), rotage(nextState, 2),
                        rotageAction(action, 2), reward, isDone)
            agent.learn(rotage(state, 3), rotage(nextState, 3),
                        rotageAction(action, 3), reward, isDone)

        prevState = state
        prevAction = action
        prevReward = reward
        isShouldLearn = True

    winner_history.append(env.checkWin())
