# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 18:44:14 2022

@author: bucki
"""

import tkinter as tk

root = tk.Tk()

myLabel1 = tk.Label(root, text="Hello world!")
myLabel2 = tk.Label(root, text="My name is John ELder")

myLabel1.grid(row=0, column=0)
myLabel2.grid(row=1, column=1)



myButton = tk.Button(root, padx=50, pady=50, text="Click me!")

myButton.grid(row=2, column=2)

root.mainloop()