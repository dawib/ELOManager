# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 16:05:59 2022

@author: bucki
"""

import os
from shutil import rmtree
import ELOMlibs.rankingClass
    
defaultMenuText = "1. Create new ranking\n2. Load an existing ranking\n3. Delete a ranking\nq. Exit\n>"
rankingMenuText = "1. Add new game\n2. Show the ranking points\n3. Delete a game\nq. Back\n>"

def main(rankingsFilePath,gamesFilePath):
    #main function
    
    def loadRankingsList():
    #returns a list with names of saved rankings
        listOfRankingsFile = open(rankingsFilePath,"r")
        listOfRankings = listOfRankingsFile.readlines()
        listOfRankingsFile.close()
    
        for i in range(len(listOfRankings)):
            listOfRankings[i]=listOfRankings[i][0:-1]
    
        return listOfRankings

    def saveRankingsList(rankingsList):
    #saves a list with names of rankings to a file
        listOfRankingsFile = open(rankingsFilePath,'w')
        for name in rankingsList:
            listOfRankingsFile.write(name)
            listOfRankingsFile.write("\n")
            
        listOfRankingsFile.close()


    def loadGamesList():
    #returns a list with saved games results
        listOfGamesFile = open(gamesFilePath,'r')
        listOfGames = listOfGamesFile.readlines()
        listOfGamesFile.close()
    
        gamesList = []
        for line in listOfGames:
            results = line.split('/')[:-1]
            comment = line.split('/')[-1]
            game = ELOMlibs.rankingClass.Game(results=results,comment=comment)
            gamesList.append(game)
    
        return gamesList

    def saveGamesList(gamesList):
    #saves a list with games to a file
        listOfGamesFile = open(gamesFilePath,'w')
        for game in gamesList:
            record = '/'.join(game.results)+'/'+game.comment
            listOfGamesFile.write(record)
            listOfGamesFile.write("\n")
            
        listOfGamesFile.close()


    def manageRankingMenu():
    #function for managing existing rankings
        games = loadGamesList()
    
        ranking=ELOMlibs.rankingClass.Ranking()
        for game in games:
            ranking.update(game)
        
        choice=0
        print()
        while choice!='q':
            choice=input(rankingMenuText)
            if choice=='q':
                continue
        
            elif choice=='1':
                gameString = input("Type in the result of a game starting from the winning player. You can add a comment in () at the end.\n>")
                game = gameString.split()
                if game[-1][-1]==')':
                    for j in range(len(game)):
                        if game[j][0]=='(':
                            t=j
                            break
                            
                    results = game[:t]
                    comment = ' '.join(game[t:])
                else:
                    results = game.copy()
                    comment = '()'
                    
                game = ELOMlibs.rankingClass.Game(results=results,comment=comment)                    
                ranking.update(game)
                print("Ranking updated!")
        
            elif choice=='2':
                for player in ranking.elos:
                    print(player,'::',ranking.elos[player])
        
            elif choice=='3':
                print("Choose a game to delete:")
                for i in range(len(ranking.games)):
                    print(i,' : ',ranking.games[i].results,ranking.games[i].comment)
                    
                index = input("Type a number (type q to cancel): ")
                if index=='q':
                    continue
                index = int(index)
                ranking.games.remove(ranking.games[index])
                ranking.recalculate()
        
            else:
                print("Invalid choice! Try again")
    
        saveGamesList(ranking.games)
    

    def createRankingMenu():
    #function for creating new rankings
        name = input("Provide a name for the new ranking: ")
        listOfRankings = loadRankingsList()
        if name in listOfRankings:
            print("A ranking with such name already exists! Load the ranking or choose another name.")
            createRankingMenu(rankingsFilePath,gamesFilePath)
            
        else:
            listOfRankings.append(name)
            os.mkdir(name)
            os.chdir(name)
            gamesList = open(gamesFilePath,'w')
            gamesList.close()
            manageRankingMenu()
            os.chdir('..')
    
        saveRankingsList(listOfRankings)

    
    def loadRankingMenu():
    #function to load an existing ranking
        listOfRankings = loadRankingsList()
        if not listOfRankings:
            print("There are no rankings created yet")
            return
        print("Rankings:")
        for name in listOfRankings:
            print(name)
        
        name = input("Choose a ranking to work with: ")
        if name in listOfRankings:
            os.chdir(name)
            manageRankingMenu()
            os.chdir('..')
            
        else:
            print("No such ranking exists")
        
    def deleteRankingMenu():
    #function to delete an existing ranking
        listOfRankings = loadRankingsList()
        if not listOfRankings:
            print("There are no rankings created yet")
            return
        print("Rankings:")
        for name in listOfRankings:
            print(name)
            
        name = input("Choose a ranking to delete (type q to cancel): ")
        if name=='q':
            return()
        
        if name in listOfRankings:
            listOfRankings.remove(name)
            rmtree(name)
            
        else:
            print("No such ranking exists")
        
        saveRankingsList(listOfRankings)
    
    choice = 0
    while choice!='q':
        print()
        choice = input(defaultMenuText)
        if choice=='1':
            createRankingMenu()
        elif choice=='2':
            loadRankingMenu()
        elif choice=='3':
            deleteRankingMenu()
        elif choice=="q":
            return
        else:
            print(choice," is not a valid option. Try again")