import numpy as np

import sys
sys.setrecursionlimit(1000)


############################################################

class TicTacToe():
    def __init__(self):
        #matrix board
        self.auxboard=[ [0.,0.,0.],
                        [0.,0.,0.],
                        [0.,0.,0.]
                      ]
        #define how to prin board
        self.printboard=[["-","-","-"],
                         ["-","-","-"],
                         ["-","-","-"]
                      ]

    def startState(self):
        """
            Start game 
            -create board
            -start with humanpolicy
        """
        self.update_board(self.auxboard)
        return (+1,self.auxboard)
    
    def update_board(self,board):
        """Create and update board"""
        for i in range(3):
            for j in range(3):
                if board[i][j]==1:
                    self.printboard[i][j]="X"
                elif board[i][j]==-1:
                    self.printboard[i][j]="O"
        
        print('{} | {} | {}'.format(self.printboard[0][0],self.printboard[0][1],self.printboard[0][2]))
        print('{} | {} | {}'.format(self.printboard[1][0],self.printboard[1][1],self.printboard[1][2]))
        print('{} | {} | {}'.format(self.printboard[2][0],self.printboard[2][1],self.printboard[2][2]))
        
    def actions(self, state):
        """ 
            actions availables in the board
        """
        player, state_board = state
        auxaction=[]
        #Giving  the actions availble
        for i in range(3):
            for j in range(3):
                if state_board[i][j]==0:
                    auxaction.append([i,j])
        return auxaction

    def succ(self, state, action):
        player,state_board  = state
        #I need to copy a list in order to be recursive
        #but copy DOESNT work for more 1D matrix
        #I had to use MAP instead
        auxlist=auxlist=list(map(list, state_board))
        auxlist[action[0]][action[1]]=player
        return (-player,auxlist)  



    def isEnd(self, state):
        """ check if game has finished when is going deep 
        in every branch of recursivity: 
            win=15 
            tie=-10 penalize 
        """
        player, state_board = state
        #row completed
        for win in np.array(state_board) :
            if abs(sum(win))==3:
                return 15
        #column completed
        for win in np.array(state_board).T :
            if abs(sum(win))==3: 
                return 15
        #diag completed
        if abs(sum(np.diag(state_board)))==3:
            return 15
        elif abs(sum(np.diag(np.rot90(np.array(state_board)))))==3:
            return 15
        #Checking if Tie
        elif np.all(np.array(state_board)):
            return -10
        return False
        
    def utility(self, state):
        player,state_board = state
        return player * 100

    def player(self, state):
        player, state_board = state
        return player



