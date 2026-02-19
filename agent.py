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
        self.epsilon = 0 # randomness
        self.gamma = 0 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        print(f"Agent initialized with max memory {MAX_MEMORY}\n Batch size {BATCH_SIZE}\n Learning rate {LR}")
        self.model = None #TODO 
        self.trainer = None #TODO
        


    def get_state(self, game): 
        head = game.snake[0]
        # check if boundary/food might get hit
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20,  head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y+20)
        # current direction 
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            # danger straight 
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)), 

            # danger right 
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)), 

            # danger left 
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)), 

            # move direction
            dir_l, 
            dir_r,
            dir_u,
            dir_d,
            
            # food location 
            game.food.x < game.head.x, # food left 
            game.food.x > game.head.x, # right
            game.food.y < game.head.y, # food up
            game.food.y > game.head.y # food down 
        ]
        
        return np.array(state, dtype=int)
    

    def remember(self, state, action, reward, next_state, done) -> None:
        self.memory.append((state, action, reward, next_state, done)) # popleft if max mem 
    
    def _unzip (self, sample): 
        if not sample: 
            return ()
        
        num_fields = len(sample[0])
        result = [[] for _ in range(num_fields)]

        for item in sample: 
            for i in range(num_fields): 
                result[i].append(item[i])
        
        return tuple(tuple(field) for field in result)

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuiples 
        else: 
            mini_sample = self.memory
        
        # extract vars 
        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        

    def train_short_memory(self, state, action, reward, next_state, done) -> None:
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff expoloration and exploitation 
        # TODO play around with this 

        # smaller the epsilon, less frequent of random moves 
        self.epsilon = 80 - self.number_of_games
        final_move = [0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1
        else: 
            state0 = torch.tensor(state, dtype = torch.float)
            predication = self.model.predict(state0)
            move = torch.argmax(predication).item()
            final_move[move] = 1

        return final_move

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
