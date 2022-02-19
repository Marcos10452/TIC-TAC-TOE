# Project description

TIC-TAC-TOE with minimax algorithm
Using minimax algorithm to play a TIC-TAC-TOE game between human and machine.


##  Requirements

- Hardware: GPU was not needed in this first approch. However if more parameters are added and neurons are incremented  GPU will be needed or training on Colab.
Intel(R) Core(TM) i5-4200M CPU @ 2.50GHz Memory 8GB

- It was developed in Linux Ubuntu 16.04.7 LTS

- Python 3.7


## General Information

The idea was to create a game which can play agains a person.
So, for this project minimax algorithm was selected.

It uses a simple recursive computation of the minimax values of each successor state, directly
implementing the defining equations. The recursion proceeds all the way down to the leaves
of the tree, and then the minimax values are backed up through the tree as the recursion
unwinds. 

minimax algorithm 

![Alt text](/pic/Algo.png?raw=true "minimax algorithm")



1)Define TIC-TAC-TOE class

class TicTacToe():
    
    def __init__(self):
        
        self.auxboard=[ [0.,0.,0.],
                        [0.,0.,0.],
                        [0.,0.,0.]]
        
        self.printboard=[["-","-","-"],
                         ["-","-","-"],
                         ["-","-","-"]]

    # Start
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
        #but copy() DOESNT work for more 1D matrix
        #I had to use MAP instead
        auxlist=list(map(list, state_board))
        auxlist[action[0]][action[1]]=player
        return (-player,auxlist)  
	#Check whether game has finished (Win or tie)
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


1)minimax algorithm


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
		# Candidates return MAX or MIN utility due to accions
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


## Usage
In terminal type:
python TIC_TAC_TOE.py

Room for improvement:
- The problem with minimax search is that the number of game states it has to examine is
  exponential in the depth of the tree. So a solution is to use alpha–beta pruning. 


## Bibliography/Acknowledgements
- Stuart j. Russell (2018) Arificial Intelligence A modern Approach 3rd edition 
- Lecture 9: Game Playing 1 - Minimax, Alpha-beta Pruning | Stanford CS221: AI (Autumn 2019)


## Contact
Created by Marcos Tagliapietra [(https://www.linkedin.com/in/marcos-e-tagliapietra)]
Any question feel free to contact me!


