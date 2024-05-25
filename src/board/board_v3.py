
import numpy as np
import pandas as pd
from PIL import ImageTk, Image
import os



import tkinter as tk
from tkinter import font
from typing import NamedTuple


class Player(NamedTuple):
    label: str
    color: str

class Move(NamedTuple):
    row: int
    col: int
    label: str = ""



class TicTacToeBoard():
    def __init__(self):
        #-----------create the canvas----------
        self.master = tk.Tk()
        self.master.option_add('*Font', '19')
        self.master.title("Tic-Tac-Toe Game")
        #--------------------------------------
        #--------------- Variables ------------
        BOARD_SIZE = 3
        DEFAULT_PLAYERS = (
            Player(label="X", color="blue"),
            Player(label="O", color="green"),
            )
        self._players = DEFAULT_PLAYERS
        self.index=0
        self._current_player=self._players[self.index]
        self._cells = {}
        #--------------------------------------
        
        #------- variabes wich are working as RX for main_board.py -------
        
        self.flag_button_pressed=False
        self.aux_row=0
        self.aux_column=0
        self.end_game=False
        
        #------- variabes wich are working as TX for main_board.py -------
        self.count_h=0
        self.count_cpu=0
        
        
       #Start menu_bar and display
        self.menu_bar()
        self._create_display()
        
        #intercept Tkinter "X" button control (the button that close the window)
        self.master .protocol('WM_DELETE_WINDOW', self._exti_game)  
    
    #------------------------------------------------
    def _exti_game(self):
        """Exit game using elf.end_game flag"""
        self.end_game=True
        self.master.destroy
        
    #------------------------------------------------
    
        ##------------------ Menu Bar ----------------------------------------------------------- 
    def menu_bar(self):  
        #Menu
        menubar = tk.Menu( self.master, relief=tk.RAISED, bd=2,font=font.Font(size=14, weight="bold"))
        filemenu = tk.Menu(menubar, tearoff = 0)
        filemenu.add_command(label = "New Game", command = self.reset_board)
        # filemenu.add_command(label = "Save", command = self.save_file)
        filemenu.add_separator()
        filemenu.add_command(label = "Exit", command = self._exti_game)
        menubar.add_cascade(label = "Game", menu = filemenu)

        helpmenu =tk.Menu(menubar, tearoff=0)
        #helpmenu.add_command(label = "TIC_TAC_TOE", command = self.donothing)
        menubar.add_cascade(label = "By Marcos Tagliapietra - 2024-05-24", menu = helpmenu)

        self.master.config(menu = menubar)
    ##------------------------------------------------------------------------------- 
    
    #--------------- Board ---------------------------- 

        
    def _create_display(self):
            
            # Adjust size
            self.HEIGHT=520
            self.WIDTH=960
            self.master.geometry(str(self.WIDTH)+"x"+str(self.HEIGHT))
            self.master.rowconfigure(0, minsize=10, weight=1)
            self.master.columnconfigure(0, minsize=10, weight=1)
      
            ##------------------ TOP ----------------------------------------------------------- 
            # #------Human counter---------
            self.human_counter = tk.Frame(self.master,relief=tk.FLAT, bd=2,width=int(self.WIDTH*0.28),height=int(self.HEIGHT*0.18), bg='#001a33')
            self.human_counter.grid(row=0, column=0,sticky="nsew")
            self.human_counter.grid_propagate(0)
    
            # #------msg Frame---------
            self.msg_frame = tk.Frame(self.master,relief=tk.FLAT, bd=2,width=int(self.WIDTH*0.40),height=int(self.HEIGHT*0.18), bg='#ccffd9')
            self.msg_frame.grid(row=0, column=1,sticky="nsew")
            self.msg_frame.grid_propagate(False)

            # #------CPU counter---------
            self.cpu_counter = tk.Frame(self.master,relief=tk.FLAT, bd=2,width=int(self.WIDTH*0.30),height=int(self.HEIGHT*0.18), bg='#001a33')
            self.cpu_counter.grid(row=0, column=2,sticky="nsew")
            self.cpu_counter.grid_propagate(False)
       
            self.update_counter()
            ##------------------------------------------------------------------------------- 
            ##--------------------------------Bottom --------------------------------------------- 
            #------picture Human Frame---------
            #Color #rgb #rrggbb #rrrgggbbb
            self.hm_img = tk.Frame(self.master,relief=tk.FLAT, bd=2,width=int(self.WIDTH*0.28),height=self.HEIGHT*0.82, bg='#336666')
            self.hm_img.grid(row=1, column=0,sticky="nsew")
            self.hm_img.grid_propagate(False)
            img = ImageTk.PhotoImage(Image.open("./pic/human_low.png"))
            image_window = tk.Label(self.hm_img, image = img)
            image_window.image = img# <== this is were we anchor the img object
            image_window.grid(row=0, column=0,  padx=5, pady=5,sticky="nsew")
            #------Board ---------
            self.board_frame = tk.Frame(self.master,relief=tk.RAISED, bd=2,width=int(self.WIDTH*0.40),height=self.HEIGHT*0.82, bg='#343d46')
            self.board_frame.grid(row=1, column=1,sticky="ew")
            self.board_frame.grid_propagate(False)
            self.display = tk.Label(master=self.msg_frame,text="Ready?",font=font.Font(size=28, weight="bold"))
            self.display.grid(row=0, column=0, padx=5, pady=5,sticky="ew")
            self._create_board_grid()

            #------Image Frame---------
            #---Picture CPU
            self.cpu_img = tk.Frame(self.master,relief=tk.FLAT, bd=2,width=int(self.WIDTH*0.30),height=self.HEIGHT*0.82, bg='#336666')
            self.cpu_img.grid(row=1, column=2,sticky="nsew")
            self.cpu_img.grid_propagate(False)
            img = ImageTk.PhotoImage(Image.open("./pic/cpu_low.png"))
            image_window = tk.Label(self.cpu_img, image = img)
            image_window.image = img# <== this is were we anchor the img object
            image_window.grid(row=0, column=0, padx=5, pady=5,sticky="ew")
            
            ##------------------------------------------------------------------------------- 
  
    
    def update_counter(self):
        """
            Show and update counters of games won.
        """
        lb_human=tk.Label(self.human_counter ,anchor="center", text='Human ' + str(self.count_h),font=font.Font(size=28, weight="bold"),relief = tk.RAISED)
        lb_human.grid(row=0, column=0, pady=10, padx=35, sticky="wens")

        lb_cpu=tk.Label(self.cpu_counter , text='CPU ' + str(self.count_cpu),font=font.Font(size=28, weight="bold"),relief = tk.RAISED)
        lb_cpu.grid(row=0, column=0, pady=10, padx=80, sticky="wens")

        
    def _create_board_grid(self):
        """
            create board with buttons and add play function when they are pressed
        """
        for row in range(3):
    
            self.master.rowconfigure(row, weight=1, minsize=50)
            self.master.columnconfigure(row, weight=1, minsize=75)
            for col in range(3):
                button = tk.Button(master=self.board_frame,text="",font=font.Font(size=32, weight="bold"),fg="black",
                    width=3,height=2,highlightbackground="lightblue")
                self._cells[button] = (row, col)
                button.bind("<ButtonPress-1>", self.play)
                button.grid(
                    row=row,
                    column=col,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )
    
    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._current_player)
        self.btn_text= clicked_btn.cget("text")
        # check if botton's text is empty or not.
        #if empty, it can be modified
        if self.btn_text=="":
            self._update_button(clicked_btn)
            #change player
            self.toggle_player()
            msg = f"CPU's turn"
            self._update_display(msg)
            #-----------------
            self.aux_row=row
            self.aux_column=col
            self.flag_button_pressed=True
            #-----------------
            return row, col

    
    def cpu(self, row, col):
        """
            Handle a cpu's move.
            It is called by main_board.py
        """
        #find button using row and col
        #key is the button form
        b = (row, col)
        keys = [key for key, value in self._cells.items() if value == b]
        move = Move(row, col, self._current_player)
        #select button's properties
        self._update_button(keys[0]) #using [0] I am accessing to methods
        #change player
        self.toggle_player()
        msg = f"Human's turn"
        self._update_display(msg)
        #-----------------
        self.aux_row=row
        self.aux_column=col
        #-----------------
        return row, col
    
    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color 
        
    def _update_button(self, clicked_btn):
        clicked_btn.config(text=self._current_player.label)
        clicked_btn.config(fg=self._current_player.color)
  
    def toggle_player(self):
        """Return a toggled player."""
        self.index=~self.index
        self._current_player = self._players[self.index]

    
    def reset_board(self):
        """Reset the game's board to play again."""
        self._update_display(msg="Ready?")
        self.index=0
        self._current_player = self._players[self.index]
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")
            button.config(state= "normal")
    

    def disable_buttons(self):
        """disable buttons when game has finished """
        for button in self._cells.keys():
            button.config(state= "disabled")
            if button.cget("text")=="":
                button.config(text="-")





