from src.agent.TIC_TAC_TOE import * 
from src.board.board_v3 import * 
import pandas as pd
import numpy as np
import time 
#def main(): 

    #window = tk.Tk()
    #app = MainGUI(window)
    #window.mainloop()


############################################################
# Policies
# def humanPolicy(game, state):
#     action2=[0,0]
#     while True:
#         print ('humanPolicy: Enter move:')
#         action2[0] = input('y row ').strip()
#         action2[1] = input('x column ').strip()
#         action2=list(map(int,action2))
#         if action2 in game.actions(state):
#             return action2
#         else:
#             print("ERROR, cell is already in use {} {}" .format(action2[1],action2[0]))
def humanPolicy(game, state,row, column):
    action2=[0,0]
    while True:
        print ('humanPolicy: Enter move:')
        action2[0] = row
        action2[1] = column
        action2=list(map(int,action2))
        if action2 in game.actions(state):
            return action2
        else:
            print("ERROR, cell is already in use {} {}" .format(action2[1],action2[0]))

def minimaxPolicy(game, state,row,column):
    """ mini-max algorithm
        working recursively 
    """
    print("Thinking...!! wait")
    def recurse(state):
        # Return (utility of that state, action that achieves that utility)
        TestEndGame=game.isEnd(state) #if 15 the game has been won by CPU
        if TestEndGame==15:
            player=-game.player(state)
            state=player, state[1]
            return (game.utility(state), None)
        elif TestEndGame==-10: #otherwise -10 it was a tie or CPU has lost the game
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
    
    board = TicTacToeBoard()
    #print(board)
    #board.mainloop()
    
    
    while not board.end_game:
        #board = TicTacToeBoard()
        game = TicTacToe()
        policies = {+1: humanPolicy,
                    -1: minimaxPolicy}
        
        #start board and return the first state
        #by definition is policy +1 ==> humand
        state = game.startState()

        #check whether game has finished
        GameEnd=game.isEnd(state)
        
        while (not GameEnd) & (not board.end_game):
            #wait to press button on GUI board
            board.master.update()
            # Select player
            player = game.player(state)
            #--------------------------------
            #If player is not humman can pass, or if humman must press button 
            # this is ineficient.bucle
            if  (board.flag_button_pressed) or (player!=1) :
            #------------------------------
                board.flag_button_pressed=False
                #Select policy depend on player 1 human or -1 CPU
                policy = policies[player]
      
                #print(board.aux_row, board.aux_column)
                #print(board.btn_text)
                # Ask policy to make a move
                action = policy(game, state,board.aux_row,board.aux_column)
                 #------------------------------
                #return row and col to board
                if player==-1:
                    board.cpu(action[0],action[1])
                 #------------------------------
                #print(action)
                # Advance state
                state = game.succ(state, action)
                #get new board state in state[1] due to game.succ
                game.update_board(state[1])
                GameEnd=game.isEnd(state) #consulta si el juego termino
            
       
        if GameEnd>0:  
            if state[0]==-1:
                player="HUMAN"
                board.count_h=board.count_h+1
                board.update_counter()
            elif state[0]==1:
                player="CPU"
                board.count_cpu=board.count_cpu+1
                board.update_counter()
            print("Player {} has won !!!. Congratulation!".format(player))
        else:
            print("TIE !!!!")
        board.disable_buttons()

