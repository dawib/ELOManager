# -*- coding: utf-8 -*-
"""
Created on Fri Mar 25 15:52:16 2022

@author: bucki
"""

def expeceted_score(elo_A, elo_B):
    #calculates the expected score of player A 
    #(probability of A winning with B)
    diff = elo_B-elo_A
    ratio = diff/400
    pw = 10**ratio
    return 1/(1+pw)

class Game:
    def __init__(self,results,comment='()'):
        self.results = results.copy()
        self.comment = comment
        

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
        for player in game.results:
            if (player not in self.players):
                self.add_player(player)
        self.update_elos(game.results)
        
    def recalculate(self):
        GAMES = self.games.copy()
        self.reset()
        for game in GAMES:
            self.update(game)
            
    def print_games(self):
        for game in self.games:
            print(game.results,game.comments)
            
    def delete_game(self,name,date):
        pass