# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 20:50:04 2022

@author: dawid bucki
"""
import os
import ELOMlibs.ELOMtbi

filesPath='ELOMfiles'
rankingsFilePath = "rankings.txt"
gamesFilePath = "games.txt"

#check if the directory with ELOM files exists
#if not, create one
#change directory to the one with ELOM files
dirs = os.listdir()
if filesPath not in dirs:
    os.mkdir(filesPath)
    os.chdir(filesPath)
    listOfRankingsFile = open(rankingsFilePath,'w')
    listOfRankingsFile.close()
    os.chdir('..')
    
os.chdir(filesPath)
ELOMlibs.ELOMtbi.main(rankingsFilePath,gamesFilePath)
os.chdir('..')