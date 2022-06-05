import numpy as np
import random
import json
from itertools import islice
import os


with open('.\Json\qTable.json', 'r', encoding="utf8") as f:
    qTable = json.load(f)

representStates = [0, 1, 2]


def getHashValue(hash):
    if not hash in qTable:
        qTable[hash] = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    return qTable[hash]


def updateHash(hash, newValue):
    qTable[hash] = newValue
    q = json.dumps(qTable, indent=4, ensure_ascii=False)
    with open('.\Json\qTable.json', 'w', encoding="utf8") as f:
        f.write(q)


def getPossibilityActions(hash):
    possibilityActions = []
    for stringValue in hash:
        value = int(stringValue)
        if value != 0:
            possibilityActions.append(0)
        else:
            possibilityActions.append(1)
    return np.array(possibilityActions)


def stateToHash(state):
    hash = ""
    for s in state:
        hash += str(int(s))
    return hash


def swapSide(state):
    newState = np.array(state, copy=True)

    for i in range(len(newState)):
        if newState[i] == 1:
            newState[i] = 2
        elif newState[i] == 2:
            newState[i] = 1

    return newState


def rotage(state, n=1):
    return np.rot90(state.reshape((3, 3)), n).reshape((9,))


def rotageAction(action, n=1):
    board = np.zeros((9,))
    board[action] = 1
    board = rotage(board, n)
    return np.argmax(board)