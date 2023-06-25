import torch
import random
import numpy as np
from collections import deque
from game import SnakeGameAI, Direction, Point

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.number_of_games = 0
        self.epsilon = 0 #randomnes
        self.gamma = 0 #discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        # TODO: model, trainer

    def get_state(self, game):
        head = game.snake[0]
        point_l = Point(head.x - 20, head.y)
        point_r = Point(head.x + 20, head.y)
        point_u = Point(head.x, head.y - 20)
        point_d = Point(head.x, head.y + 20)

        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN

        state = [
            #dange straight
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),

            #dange right
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),

            #dange left
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),

            #move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d

            #food location
            game.food.x < game.head.x,
            game.food.x > game.head.x,
            game.food.y < game.head.y,
            game.food.y > game.head.y
        ]
    
        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        pass

    def train_long_memory(self):
        pass

    def train_short_memory(self, state, action, reward, next_state, done):
        pass

    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = SnakeGameAI()
    while True:
        #get old state
        state_old = agent.get_state()

        #get move
        final_move = agent.get_action(state_old)

        #perform move
        reward, done, score = game.play_step(final_move)

        #get new state
        state_new = agent.get_state()

        #train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        #rememger
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            #train long memory, plot results
            game.reset()
            agent.number_of_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                #TODO: agent.model.save()

            print('Game:', agent.number_of_games, '  Score:', score, '  Record:', record)

            #TODO: plot


if __name__ == '__main__':
    train()