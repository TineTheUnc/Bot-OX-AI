import numpy as np
import random
import json
from itertools import islice
import os
from Body import *
from Fung import *

traintotal = {"win":0, "draw":0, "lose":0}

class TigTagToeGame:
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
        board = self.board.reshape((3, 3))
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

    def play(self, action):
        player = 2
        if self.isXTurn:
            player = 1
        self.board[action] = player
        self.isXTurn = not self.isXTurn
        winner = self.checkWin()
        isDone = self.checkDone()
        nextState = np.array(self.board, copy=True)
        return nextState, isDone


game = TigTagToeGame()
agent = Agent(isPlay=True)


def AIVsHuman ():
    isDone = False
    game.reset()
    while not isDone:
        state = game.getState()
        print("--- AI vs Human ---")
        game.showBoard()
        action = 0
        if game.isXTurn:
            isInputValidate = False
            while not isInputValidate:
                action = int(input("player turn (X):"))
                if len(state) > action and state[action] == 0:
                    isInputValidate = True
            print("thinking x", getHashValue(stateToHash(state)))
            if state[4] == 0:
                action = 4
        else:
            sstate = (state)
            print("thinking", getHashValue(stateToHash(sstate)))
            action = agent.act(swapSide(state))
        print(action)
        state, isDone = game.play(action)
    print("game end")
    game.showBoard()
    winner = game.checkWin()
    if winner == 1:
        print("Congratulation the player win.")
    elif winner == 2:
        print("AI is the winner, We'll conquer the world")
    else:
        print("Draw!!")
        
def AIVsAI ():
    while not isDone:
        state = game.getState()
        print("--- AI vs Human ---")
        game.showBoard()
        action = 0
        if game.isXTurn:
            action = agent.act(state)
            print("thinking x", getHashValue(stateToHash(state)))
            if state[4] == 0:
                action = 4
        else:
            sstate = (state)
            print("thinking", getHashValue(stateToHash(sstate)))
            action = agent.act(swapSide(state))
        print(action)
        state, isDone = game.play(action)
    print("game end")
    game.showBoard()
    winner = game.checkWin()
    if winner == 1:
        print("Congratulation the player win.")
    elif winner == 2:
        print("AI is the winner, We'll conquer the world")
    else:
        print("Draw!!")

def AIVsRandom (round:int = 1000):
    for i in range(round):
        isDone = False
        game.reset()
        while not isDone:
            state = game.getState()
            action = 0
            if game.isXTurn:
                hash = stateToHash(state)
                possibleActions = getPossibilityActions(hash)
                idx = [i for i in range(len(possibleActions))if possibleActions[i] == 1]
                action = random.choice(idx)
            else:
                action = agent.act(swapSide(state))
                if state[4] == 0:
                    action = 4 
            state, isDone = game.play(action)
        winner = game.checkWin()
        if winner == 1:
            print("What!! AI Lose a randomness ?")
            game.showBoard()
            traintotal["lose"] += 1
            break
        elif winner == 2:
            # pass
            print("AI is the winner, We'll conquer the world")
            traintotal["win"] += 1
        else:
            print("Draw!!")
            traintotal["draw"] += 1
            
    for t in traintotal.keys():
        print(t, ":", traintotal[t])

