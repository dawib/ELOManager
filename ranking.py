# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 20:50:04 2022

@author: dawid bucki
"""
import os

def expeceted_score(elo_A, elo_B):
    #calculates the expected score of player A 
    #(probability of A winning with B)
    diff = elo_B-elo_A
    ratio = diff/400
    pw = 10**ratio
    return 1/(1+pw)

#class Game:
#    def __init__(self,name,date,results):
#        self.name = name
#        self.date = date
#        self.results = results

class Ranking:
    def __init__(self,K=20):
        self.elos = {}
        self.players = []
        self.games=[]
        self.K=K
        
    def reset(self):
        #resets the ranking to a blank state
        self.elos = {}
        self.players = []
        self.games=[]
        
        
    def add_player(self,player):
        #adds new player with the name <player> to the ranking with 1000ELO
        if (player in self.players):
            print("Player ", player, " is already included in the ranking")
        else:
            self.players.append(player)
            self.elos[player]=1000
    
    def updated_player_score(self,game,player):
        #calculates player's updated score after a game
        change=0
        score=0
        for i in range(len(game)):
            if game[i]==player:
                score=1
                continue
            else:
                change+=score-expeceted_score(self.elos[player], self.elos[game[i]])
        return self.elos[player]+self.K*change/len(game)
    
    def update_elos(self,game):
        #updates elo ranking after a game
        for player in game:
            self.elos[player]=round(self.updated_player_score(game, player))
    
    def update(self,game):
        #adds new players to the ranking and updates elo points 
        #based on the game
        self.games.append(game)
        for player in game:
            if (player not in self.players):
                self.add_player(player)
        self.update_elos(game)
        
    def recalculate(self):
        GAMES = self.games
        self.reset()
        for game in GAMES:
            self.update(game)
            
    def print_games(self):
        for game in self.games:
            print(game)
            
    def delete_game(self,name,date):
        pass
    
    
####################################################################
    
defaultMenuText = "1. Create new ranking\n2. Load an existing ranking\n3. Delete a ranking\nq. Exit\n>"
rankingMenuText = "1. Add new game\n2. Show the ranking points\nq. Back\n>"

def manageRankingMenu():
    gamesList = open("list.txt", "r")
    gamesString = gamesList.readlines()
    gamesList.close()   
    
    games = []
    for line in gamesString:
        line2 = line[0:-1]
        games.append(line2.split())
    
    ranking=Ranking()
    for game in games:
        ranking.update(game)
        
    choice=0
    while choice!='q':
        choice=input(rankingMenuText)
        if choice=='1':
            gameString = input("Type in the result of a game starting from the winning player\n>")
            game = gameString.split()
            ranking.update(game)
            print("Ranking updated!")
        elif choice=='2':
            for player in ranking.elos:
                print(player,'::',ranking.elos[player])
    
    gamesList=open("list.txt", 'w')
    for game in ranking.games:
        line = ' '.join(game)
        gamesList.write(line)
        gamesList.write("\n")
    gamesList.close()
    

def createRankingMenu():
    name = input("Provide a name for the new ranking: ")
    listOfRankings = open("list.txt", "a")
    listOfRankings.write(name)
    listOfRankings.write("\n")
    listOfRankings.close()
    
    os.mkdir(name)
    os.chdir(name)
    gamesList = open('list.txt','w')
    gamesList.close()
    manageRankingMenu()
    os.chdir('..')

def loadRankingMenu():
    listOfRankings = open("list.txt","r")
    rankingsList = listOfRankings.readlines()
    listOfRankings.close()
    for i in range(len(rankingsList)):
        rankingsList[i]=rankingsList[i][0:-1]
    print("Rankings:")
    for name in rankingsList:
        print(name)
    name = input("Choose a ranking to work with: ")
    if name in rankingsList:
        os.chdir(name)
        manageRankingMenu()
        os.chdir('..')
    else:
        print("No such ranking exists")
        
def deleteRankingMenu():
    pass

def menu():
    choice = 0
    while choice!='q':
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

dirs = os.listdir()
if 'rankings' not in dirs:
    os.mkdir('rankings')
os.chdir('rankings')
menu()
os.chdir('..')