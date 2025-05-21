import numpy as np
import random
import json
import os

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.1, discount_factor=0.95, exploration_rate=1.0):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.exploration_decay = 0.995
        self.min_exploration_rate = 0.01
        self.max_exploration_rate = 0.8  # Cap on exploration rate
        
        # Initialize Q-table with zeros
        self.q_table = np.zeros((state_size, action_size))
        
        # Training metrics
        self.best_reward = float('-inf')
        self.episode_rewards = []
    
    def get_state_index(self, state):
        # Convert the state (x, y coordinates) to a single index
        x, y = state
        
        # Game dimensions:
        # - Level length: ~2000 units
        # - Jump height: ~140 units
        # Let's create a grid that's more appropriate for these dimensions
        
        # For x: divide level into 80 sections (2000/80 = 25 units per section)
        # For y: divide height into 10 sections (140*2 = 280 units, so ~28 units per section)
        x_section_size = 25
        y_section_size = 28
        
        # Calculate grid indices
        x_idx = min(int(x) // x_section_size, 79)  # 0-79 for x
        y_idx = min(int(y) // y_section_size, 9)   # 0-9 for y
        
        # Convert 2D grid position to 1D index (80x10 grid = 800 states)
        return int(x_idx * 10 + y_idx)
    
    def get_position_based_exploration(self, x_pos):
        """Calculate exploration rate boost based on Mario's x position"""
        # Convert x position to section (0-79)
        x_section = min(int(x_pos) // 25, 79)
        
        # Calculate exploration boost (0 to 0.4)
        # More boost as Mario gets further in the level
        exploration_boost = (x_section / 79) * 0.4
        
        return exploration_boost
    
    def choose_action(self, state):
        state_idx = self.get_state_index(state)
        x,y = state  # Get x position from state
        
        # Calculate position-based exploration boost
        exploration_boost = self.get_position_based_exploration(x)
        
        # Combine base exploration rate with position-based boost
        effective_exploration_rate = min(
            self.exploration_rate + exploration_boost,
            self.max_exploration_rate
        )
        
        # Exploration: choose a random action
        if random.random() < effective_exploration_rate:
            return random.randrange(self.action_size)
        
        # Exploitation: choose the best action from Q-table
        return np.argmax(self.q_table[state_idx])
    
    def learn(self, state, action, reward, next_state, done):
        state_idx = self.get_state_index(state)
        next_state_idx = self.get_state_index(next_state)
        
        # Q-learning update formula
        old_value = self.q_table[state_idx, action]
        if done:
            next_max = 0
        else:
            next_max = np.max(self.q_table[next_state_idx])
        
        new_value = (1 - self.learning_rate) * old_value + \
                    self.learning_rate * (reward + self.discount_factor * next_max)
        
        self.q_table[state_idx, action] = new_value
        
        # Decay exploration rate
        if done:
            self.exploration_rate = max(self.min_exploration_rate, 
                                      self.exploration_rate * self.exploration_decay)
    
    def save(self, filename='mario_agent'):
        """Save the agent's Q-table and training metrics"""
        # Create directory if it doesn't exist
        os.makedirs('saved_agents', exist_ok=True)
        
        # Save Q-table
        np.save(f'saved_agents/{filename}_qtable.npy', self.q_table)
        
        # Save training metrics
        metrics = {
            'exploration_rate': self.exploration_rate,
            'best_reward': self.best_reward,
            'episode_rewards': self.episode_rewards
        }
        with open(f'saved_agents/{filename}_metrics.json', 'w') as f:
            json.dump(metrics, f)
    
    def load(self, filename='mario_agent'):
        """Load the agent's Q-table and training metrics"""
        try:
            # Load Q-table
            self.q_table = np.load(f'saved_agents/{filename}_qtable.npy')
            
            # Load training metrics
            with open(f'saved_agents/{filename}_metrics.json', 'r') as f:
                metrics = json.load(f)
                self.exploration_rate = metrics['exploration_rate']
                self.best_reward = metrics['best_reward']
                self.episode_rewards = metrics['episode_rewards']
            
            return True
        except FileNotFoundError:
            print(f"No saved agent found at {filename}")
            return False
    
    def update_metrics(self, episode_reward):
        """Update training metrics after each episode"""
        self.episode_rewards.append(episode_reward)
        if episode_reward > self.best_reward:
            self.best_reward = episode_reward
            # Save the best agent
            self.save('mario_agent_best') 