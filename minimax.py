# 人工智能大作业
# 基于 Minimax 算法的四子棋
#
# minimax实现


import random

class Minimax(object):
    board = None
    colors = ["x", "o"]

    def __init__(self, board):
        self.board = [x[:] for x in board]

    def bestMove(self, depth, state, curr_player):
        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        legal_moves = {}
        for col in range(7):
            if self.isLegalMove(col, state):
                temp = self.makeMove(state, col, curr_player)
                legal_moves[col] = -self.search(depth-1, temp, opp_player)

        best_alpha = -99999999
        best_move = None
        moves = legal_moves.items()
        random.shuffle(list(moves))
        for move, alpha in moves:
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

    def search(self, depth, state, curr_player):
        """ Searches the tree at a given depth
            curr_player: caller of this search

            Returns the alpha value
        """

        legal_moves = []
        for i in range(7):
            if self.isLegalMove(i, state):
                temp = self.makeMove(state, i, curr_player)
                legal_moves.append(temp)

        # terminal node or depth == 0
        if depth == 0 or len(legal_moves) == 0 or self.gameIsOver(state):
            return self.value(state, curr_player)

        if curr_player == self.colors[0]:
            opp_player = self.colors[1]
        else:
            opp_player = self.colors[0]

        alpha = -99999999
        for child in legal_moves:
            if child == None:
                print("child == None (search)")
            alpha = max(alpha, -self.search(depth-1, child, opp_player))
        return alpha

    def isLegalMove(self, column, state):
        for i in range(6):
            if state[i][column] == ' ':
                return True

        # full column
        return False

    def gameIsOver(self, state):
        if self.checkStreaks(state, self.colors[0], 4) >= 1:
            return True
        elif self.checkStreaks(state, self.colors[1], 4) >= 1:
            return True
        else:
            return False


    def makeMove(self, state, column, color):
        temp = [x[:] for x in state]
        for i in range(6):
            if temp[i][column] == ' ':
                temp[i][column] = color
                return temp

    def value(self, state, color):
        return self.winningArray(state, color)

    def winningArray(self, state, color):
        """ Simple heuristic
            my_fours*100000 + my_threes*100 + my_twos
        """
        assert color == 'x' or color == 'o'

        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]

        if(not hasattr(self, "winarray")):
            self.geneWinningArray()

        my_fours  = self.checkStreaks(state, color, 4)
        my_threes = self.checkStreaks(state, color, 3)
        my_twos   = self.checkStreaks(state, color, 2)
        opp_fours = self.checkStreaks(state, o_color, 4)
        #opp_threes = self.checkStreaks(state, o_color, 3)
        #opp_twos   = self.checkStreaks(state, o_color, 2)
        if opp_fours > 0:
            return -100000
        else:
            return my_fours*100000 + my_threes*100 + my_twos


    def checkStreaks(self, state, color, streak):
        if color == self.colors[0]:
            o_color = self.colors[1]
        else:
            o_color = self.colors[0]

        if(not hasattr(self, "winarray")):
            self.geneWinningArray()

        num = 0
        for winlist in self.winarray:
            colorlist = list(state[winlist[i][0]][winlist[i][1]] for i in range(0, 4))
            if(colorlist.count(o_color) == 0 and colorlist.count(color) == streak):\
                num = num + 1

        return num


    def geneWinningArray(self):
        self.winarray = []
        # vertical
        for i in range(0, 3):
            for j in range(0, 7):
                temp = []
                for k in range(0, 4):
                    temp.append((i + k, j))
                self.winarray.append(temp)

        # horizontal
        for i in range(0, 6):
            for j in range(0, 4):
                temp = []
                for k in range(0, 4):
                    temp.append((i, j + k))
                self.winarray.append(temp)

        # positive slope
        for i in range(0, 3):
            for j in range(0, 4):
                temp = []
                for k in range(0, 4):
                    temp.append((i + k, j + k))
                self.winarray.append(temp)

        # negative slope
        for i in range(3, 6):
            for j in range(0, 4):
                temp = []
                for k in range(0, 4):
                    temp.append((i - k, j + k))
                self.winarray.append(temp)

