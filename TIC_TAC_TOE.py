import numpy as np

import sys
sys.setrecursionlimit(1000)


############################################################

class TicTacToe():
    def __init__(self):
        
        self.auxboard=[ [0.,0.,0.],
                        [0.,0.,0.],
                        [0.,0.,0.]
                      ]
        self.printboard=[["-","-","-"],
                         ["-","-","-"],
                         ["-","-","-"]
                      ]

    def startState(self):
        self.update_board(self.auxboard)
        return (+1,self.auxboard)
    
    def update_board(self,board):
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

############################################################
# Policies

def humanPolicy(game, state):
    action2=[0,0]
    while True:
        print ('humanPolicy: Enter move:')
        action2[0] = input('y row ').strip()
        action2[1] = input('x column ').strip()
        action2=list(map(int,action2))
        if action2 in game.actions(state):
            return action2
        else:
            print("ERROR, cell is already in use {} {}" .format(action2[1],action2[0]))

def minimaxPolicy(game, state):
    print("Thinking...!! wait")
    def recurse(state):
        # Return (utility of that state, action that achieves that utility)
        TestEndGame=game.isEnd(state)
        if TestEndGame==15:
            player=-game.player(state)
            state=player, state[1]
            return (game.utility(state), None)
        elif TestEndGame==-10:
            player=0
            state=player, state[1]
            return (game.utility(state), None)
                
        # List of (utility of succ, action leading to that succ)
        
        candidates = [
            (recurse(game.succ(state, action))[0], action)
            for action in game.actions(state)]
        #Agent player maximaice
        player = game.player(state)
        if player == +1:
            return max(candidates)
        #opponent player try to min agent's policy
        elif player == -1:
            return min(candidates)
        assert False

    utility, action = recurse(state)
    print("DONE...")
    return action

############################################################

game = TicTacToe()

policies = {
    +1: humanPolicy,
    -1: minimaxPolicy
            }

state = game.startState()

GameEnd=game.isEnd(state)

while not GameEnd:
    # Select player
    player = game.player(state)
    #Select policy depend on player 1 human or -1 CPU
    policy = policies[player]
    # Ask policy to make a move
    action = policy(game, state)
    # Advance state
    state = game.succ(state, action)
    #get new board state in state[1] due to game.succ
    game.update_board(state[1])
    GameEnd=game.isEnd(state)
    
if GameEnd>0:  
    if state[0]==-1:
        player="HUMAN"
    elif state[0]==1:
        player="CPU"
    print("Player {} has won !!!. Congratulation!".format(player))
else:
    print("TIE !!!!")

