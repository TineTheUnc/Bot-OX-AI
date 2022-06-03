import numpy as np
import random
import json
from itertools import islice
import os
from Fung import *



"""# Create Agent"""

class Agent:
  def __init__(self, epsilon=0.3, lr=0.3, gamma=.99, isPlay=False):
    self.epsilon = epsilon
    self.lr = lr
    self.gamma = gamma
    self.isPlay = isPlay

  def act(self, state):
    rand = random.uniform(0, 1)
    # convert state to hash
    hash = stateToHash(state)

    # get possibility actions
    possibilityActions = getPossibilityActions(hash)

    # get Q value
    qValues = getHashValue(hash)

    # random Q value
    if rand < self.epsilon and not self.isPlay:
      qValues = np.random.rand(9)
    
    # avoid choice same action when qValue is negative
    qValues = np.array(qValues)
    if qValues.min() < 0:
      base = abs(qValues.min())
      qValues += base * 2

    # dot product
    qValues = np.multiply(qValues, possibilityActions)

    # avoid use first action when nothing to choose
    if qValues.sum() == 0:
      qValues = possibilityActions

    # random if have multiple best action
    if np.count_nonzero(qValues == qValues.max()) > 1:
      bestActions = [i for i in range(len(qValues)) if qValues[i] == qValues.max()]
      return random.choice(bestActions)

    # print(qValues)
    # choose best action
    return np.argmax(qValues)

  def learn(self, state, nextState, action, reward, isDone):
    hashState = stateToHash(state)
    hashNextState = stateToHash(nextState)

    qState = getHashValue(hashState)
    qNextState = getHashValue(hashNextState)

    possibilityActions = getPossibilityActions(hashNextState)
    qNextState = np.multiply(qNextState, possibilityActions)

    tmpQNextState = np.array(qNextState, copy=True)
    if qNextState.min() < 0:
      base = abs(qNextState.min())
      tmpQNextState += base * 2

    qState[action] += self.lr * (reward + self.gamma * qNextState[np.argmax(tmpQNextState)] - qState[action])
    if isDone:
      qState[action] = reward

    updateHash(hashState, qState)

"""# Create Env"""

class Env:
  def __init__(self):
    self.reset()

  def reset(self):
    self.board = np.zeros((9,))
    self.isXTurn = True
    return self.getState()

  def checkRows(self, board):
    for row in board:
        if len(set(row)) == 1:
            return row[0]
    return 0

  def checkDiagonals(self, board):
    if len(set([board[i][i] for i in range(len(board))])) == 1:
        return board[0][0]
    if len(set([board[i][len(board)-i-1] for i in range(len(board))])) == 1:
        return board[0][len(board)-1]
    return 0

  def checkWin(self):
    board = self.board.reshape((3,3))
    for newBoard in [board, np.transpose(board)]:
        result = self.checkRows(newBoard)
        if result:
            return result
    return self.checkDiagonals(board)

  def checkDraw(self):
    return self.checkWin() == 0

  def checkDone(self):
    return self.board.min() != 0 or self.checkWin() != 0

  def getState(self):
    return np.array(self.board, copy=True)

  def showBoard(self):
    prettyBoard = self.board.reshape((3, 3))
    for row in prettyBoard:
      print("|", end='')
      for col in row:
        symbol = "*"
        if col == 1:
          symbol = "X"
        elif col == 2:
          symbol = "O"
        print(symbol, end='')
        print("|", end='')
      print("")

  def act(self, action):
    reward = 0
    player = 2
    if self.isXTurn:
      player = 1

    self.board[action] = player
    self.isXTurn = not self.isXTurn

    winner = self.checkWin()
    isDraw = self.checkDraw()
    isDone = self.checkDone()

    if winner:
      reward = 1
    
    if isDraw:
      reward = 0.5

    nextState = np.array(self.board, copy=True)
    return nextState, reward, isDone, {}