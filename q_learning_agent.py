import numpy as np
import random
import json
import os

class QLearningAgent:
    def __init__(self, action_size, learning_rate=0.3, discount_factor=0.95, exploration_rate=1.0):
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.min_exploration_rate = 0.001
        self.max_exploration_rate = 0.3
        self.x_sections = 120
        self.y_sections = 10

        # Initialisieren der Q-table mit Nullen (1200 x action_size)
        self.q_table = np.zeros((self.x_sections * self.y_sections, action_size))
        
        # Performanzdaten
        self.best_reward = float('-inf')
        self.episode_rewards = []
    
    def get_state_index(self, state):
        """Konvertiert Koordinatentupel (x, y) zu Zustands-Index"""
        x, y = state
        # Schätzung der Dimensionen:
        # - Level-Länge: ~3000 Einheiten
        # - Sprunghöhe: ~140 Einheiten
        # Für x: Level wird in 120 Sektoren unterteilt (3000/120 = 25 Einheiten pro Sektor)
        # Für y: Level wird in 10 Sektoren unterteilt (Doppelte Sprunghöhe 140*2 = 280 Einheiten, ~28 Einheiten pro Sektor)
        x_section_size = 25
        y_section_size = 28
        x_idx = min(int(x) // x_section_size, self.x_sections - 1)  # 0-119 für x
        y_idx = min(int(y) // y_section_size, self.y_sections - 1)  # 0-9 für y
        # 2D Index => 1D index
        return int(x_idx * self.y_sections + y_idx)
    
    def choose_action(self, state, x_max):
        """Wählt nächste Aktion aus"""
        state_idx = self.get_state_index(state)
        x = state[0]

        # Positionsabhängige Exploration Rate
        exploration_rate = max(min(0.005 * x - 0.005*(x_max-35), self.max_exploration_rate), self.min_exploration_rate)

        # Exploration
        if random.random() < exploration_rate:
            return random.randrange(self.action_size)
        
        # Exploitation
        return np.argmax(self.q_table[state_idx])
    
    def learn(self, state, action, reward, next_state, done):
        state_idx = self.get_state_index(state)
        next_state_idx = self.get_state_index(next_state)
        
        # Q-learning Formel
        old_value = self.q_table[state_idx, action]
        if done:
            next_max = 0
        else:
            next_max = np.max(self.q_table[next_state_idx])
        
        new_value = (1 - self.learning_rate) * old_value + self.learning_rate * (reward + self.discount_factor * next_max)
        
        self.q_table[state_idx, action] = new_value
        
    def save(self, filename='mario_agent'):
        """Speichert die Trainings- und Performanzdaten"""

        os.makedirs('saved_agents', exist_ok=True)
        np.save(f'saved_agents/{filename}_qtable.npy', self.q_table)
        
        metrics = {
            'best_reward': self.best_reward,
            'episode_rewards': self.episode_rewards
        }
        with open(f'saved_agents/{filename}_metrics.json', 'w') as f:
            json.dump(metrics, f)
    
    def load(self, filename='mario_agent'):
        """Lädt die Trainings- und Performanzdaten"""
        try:
            self.q_table = np.load(f'saved_agents/{filename}_qtable.npy')
            
            with open(f'saved_agents/{filename}_metrics.json', 'r') as f:
                metrics = json.load(f)
                self.best_reward = metrics['best_reward']
                self.episode_rewards = metrics['episode_rewards']
            return True
        except FileNotFoundError:
            print(f"No saved agent found at {filename}")
            return False
    
    def update_metrics(self, episode_reward):
        """Updated die Performanzdaten"""
        self.episode_rewards.append(episode_reward)
        if episode_reward > self.best_reward:
            self.best_reward = episode_reward
            # Speichert den besten Agenten
            self.save('mario_agent_best') 