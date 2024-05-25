from src.agent.TIC_TAC_TOE import * 
import pandas as pd
import numpy as np
#def main(): 

    #window = tk.Tk()
    #app = MainGUI(window)
    #window.mainloop()


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

if __name__ == '__main__':
    game = TicTacToe()
    
    policies = {+1: humanPolicy,
                -1: minimaxPolicy}
    
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

