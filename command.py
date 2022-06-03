import nextcord
import string
from typing import List
import numpy as np
from nextcord import DMChannel, Interaction, SlashOption, ChannelType, Attachment
from nextcord.abc import GuildChannel
from nextcord.ext import tasks, commands
from nextcord.ui import Button, View, Modal, TextInput
from AI.Body import *
from AI.Fung import *


intents = nextcord.Intents.default()
intents.members = True
intents.guilds = True
intents.messages = True

prefix = ""
bot = commands.Bot(command_prefix=prefix, help_command=None,case_insensitive=True, intents=intents)

guild_id = 0


class TicTacToeButton(nextcord.ui.Button["TicTacToe"]):
    def __init__(self, x: int, y: int):
        # A label is required, but we don't need one so a zero-width space is used
        # The row parameter tells the View which row to place the button under.
        # A View can only contain up to 5 rows -- each row can only have 5 buttons.
        # Since a Tic Tac Toe grid is 3x3 that means we have 3 rows and 3 columns.
        super().__init__(style=nextcord.ButtonStyle.secondary, label="\u200b", row=y)
        if y == 0:
            self.p = x
        elif y == 1:
            self.p = x + 3
        elif y == 2:
            self.p = x + 6

    # This function is called whenever this particular button is pressed
    # This is part of the "meat" of the game logic
    async def callback(self, interaction: nextcord.Interaction):
        await interaction.response.defer(ephemeral=True)
        assert self.view is not None
        view: TicTacToe = self.view
        state = np.array(view.board, copy=True)
        content = f"{interaction.user} VS AI LEVEL: 1(Q)"
        time_after = None

        if view.current_player == view.X:
            self.style = nextcord.ButtonStyle.danger
            self.label = "X"
            self.disabled = True
            view.board[self.p] = view.X
            view.current_player = view.O
            await interaction.edit(content=content, view=view, delete_after=time_after)
            if view.board.min() == 0 and view.check_board_winner() is None and view.current_player == view.O:
                view.AI()

        else:
            await interaction.send(f"{interaction.user.mention} ไม่ใชาตาของคุณ", ephemeral=True)

        winner = view.check_board_winner()
        if winner is not None:
            if winner == view.X:
                content = f"{interaction.user.mention} ชนะ!\nยินดีด้วยคุณชนะ AI"
            elif winner == view.O:
                content = "AI ชนะ!\nAI เราเทรนมาดี"
            else:
                content = "เสมอ\nก็ปกติดี"

            for child in view.children:
                child.disabled = True

            view.stop()
            time_after = 15

        await interaction.edit(content=content, view=view, delete_after=time_after)


# This is our actual board View
class TicTacToe(nextcord.ui.View):
    # This tells the IDE or linter that all our children will be TicTacToeButtons
    # This is not required
    children: List[TicTacToeButton]
    X = 1
    O = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = np.zeros((9,))
        self.agent = Agent(isPlay=True)

        # Our board is made up of 3 by 3 TicTacToeButtons
        # The TicTacToeButton maintains the callbacks and helps steer
        # the actual game.
        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def AI(self):
        done = False
        while not done:
            state = np.array(self.board, copy=True)
            action = self.agent.act(swapSide(state))
            if self.board[action] == 0:
                done = True
                self.board[action] = self.O
                self.children[X2Y(action)].label = "O"
                self.children[X2Y(action)].style = nextcord.ButtonStyle.success
                self.children[X2Y(action)].disabled = True
                self.current_player = self.X
        for i, b in enumerate(self.board):
            if b == 1:
                if self.children[X2Y(i)].label != "X":
                    self.children[X2Y(i)].label = "X"
                    self.children[X2Y(i)].style = nextcord.ButtonStyle.danger
                    self.children[X2Y(i)].disabled = True
            elif b == 2:
                if self.children[X2Y(i)].label != "O":
                    self.children[X2Y(i)].label = "0"
                    self.children[X2Y(i)].style = nextcord.ButtonStyle.success
                    self.children[X2Y(i)].disabled = True
            else:
                if self.children[X2Y(i)].label != "\u200b":
                    self.children[X2Y(i)].label = "\u200b"
                    self.children[X2Y(i)].style = nextcord.ButtonStyle.secondary
                    self.children[X2Y(i)].disabled = False
        self.current_player = self.X
    
    # This method checks for the board winner -- it is used by the TicTacToeButton
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

    def check_board_winner(self):
        winner = self.checkWin()
        if winner == 2:
            return self.O
        elif winner == 1:
            return self.X
        elif self.board.min() != 0.:
            return 0
        else:
            return None


@bot.slash_command(name='tictactoe', description="เล่น OX กับ AI", guild_ids=[guild_id])
async def Tic_Tac_Toe(Interaction: Interaction):
    viw = TicTacToe()
    await Interaction.send(f"{Interaction.user} VS AI LEVEL: 1(Q)", view=viw)


bot.run('TOKEN')