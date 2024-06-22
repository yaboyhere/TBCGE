# importing required libraries
from tkinter import *
import pygame
import time
from pathlib import Path
root = Tk()
root.title('GeeksforGeeks sound player')

root.geometry("500x400")

pygame.mixer.init()# initialise the pygame

def play():
    pygame.mixer.music.load(str(Path(__file__).parent.resolve()) + r"\Down_by_the_River.mp3")
    pygame.mixer.music.play(loops=0)
    time.sleep(10)
    pygame.mixer.music.stop()

 

title=Label(root,text="GeeksforGeeks",bd=9,relief=GROOVE,
			font=("times new roman",50,"bold"),bg="white",fg="green") 
title.pack(side=TOP,fill=X) 

play_button = Button(root, text="Play Song", font=("Helvetica", 32), command=play)
play_button.pack(pady=20)
root.mainloop()
