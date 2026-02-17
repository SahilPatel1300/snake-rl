import torch 
import random 
import numpy as np 
from game import SnakeGameAI, Direction, Point
from collections import deque

# can store 100k items in memory 
# can play around with these 
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


class Agent:

    def __init__(self):
        self.number_of_games = 0
        self.espilon = 0 # randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        print(f"Agent initialized with max memory {MAX_MEMORY}\n Batch size {BATCH_SIZE}\n Learning rate {LR}")
        #TODO: model and trainer 


    def get_state(self, game): 
        pass

    def remember(self, state, action, reward, next_state, done):
        pass
    
    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass

def train():
    # initialize plot scores and agent
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    # training loop
    while True: 
        # get the old state 
        state_old = agent.get_state(game)
        print(f"State old: {state_old}")

        # get the move based on current state 
        final_move = agent.get_action(state_old)
        print(f"Final move: {final_move}")

        # perform the move and get the new state 
        reward, done, score = game.play_step(final_move)
        print(f"Reward: {reward}, Done: {done}, Score: {score}")
        state_new = agent.get_state(game)
        print(f"State new: {state_new}")

        # train the short memory for 1 step 
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember 
        agent.remember(state_old, final_move, reward, state_new, done)
        if done: 
            # train the long memory, plot the result 
            game.reset()
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                # agent.model.save()
            print('Game', agent.number_of_games, 'Score', score, 'Record:', record)
        
        # TODO: plotting 
        






if __name__ == "__main__":
    train()
