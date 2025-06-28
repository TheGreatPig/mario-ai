import numpy as np
import random
import json
import os

class QLearningAgent:
    def __init__(self, state_size, action_size, learning_rate=0.3, discount_factor=0.95):
        self.state_size = state_size
        self.action_size = action_size
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

        self.q_table = np.zeros((state_size, action_size))

        self.best_reward = float('-inf')
        self.episode_rewards = []

    def get_state_index(self, state):
        """Wandelt (x, y)-Koordinaten in diskreten Zustand um"""
        x, y = state
        x_section_size = 15
        y_section_size = 20
        x_idx = min(int(x) // x_section_size, 79)
        y_idx = min(int(y) // y_section_size, 9)
        return int(x_idx * 10 + y_idx)

    def choose_action(self, state, x_max):
        """Wählt Aktion basierend auf Exploration vs. Exploitation"""
        state_idx = self.get_state_index(state)
        x = state[0]

        # Adaptive Exploration Rate basierend auf Fortschritt
        exploration_rate = max(min(0.1 * x - 0.005 * (x_max - 35), 0.5), 0.2)

        if random.random() < exploration_rate:
            return random.randrange(self.action_size)

        return np.argmax(self.q_table[state_idx])

    def learn(self, state, action, reward, next_state, done):
        """Q-Learning-Update-Regel anwenden"""
        state_idx = self.get_state_index(state)
        next_state_idx = self.get_state_index(next_state)

        old_value = self.q_table[state_idx, action]
        next_max = 0 if done else np.max(self.q_table[next_state_idx])

        new_value = (1 - self.learning_rate) * old_value + \
                    self.learning_rate * (reward + self.discount_factor * next_max)

        self.q_table[state_idx, action] = new_value

        # 🧨 Mario gestorben → Q-Werte stark bestrafen
        if done and reward < 0:
            self.q_table[state_idx] *= 0.1

    def save(self, filename='mario_agent_v2'):
        """Q-Tabelle + Metriken speichern"""
        os.makedirs('saved_agents', exist_ok=True)
        np.save(f'saved_agents/{filename}_qtable.npy', self.q_table)
        metrics = {
            'best_reward': self.best_reward,
            'episode_rewards': self.episode_rewards
        }
        with open(f'saved_agents/{filename}_metrics.json', 'w') as f:
            json.dump(metrics, f)

    def load(self, filename='mario_agent_v2'):
        """Agent-Zustand wiederherstellen (falls vorhanden)"""
        try:
            self.q_table = np.load(f'saved_agents/{filename}_qtable.npy')
            with open(f'saved_agents/{filename}_metrics.json', 'r') as f:
                metrics = json.load(f)
                self.best_reward = metrics['best_reward']
                self.episode_rewards = metrics['episode_rewards']
            return True
        except FileNotFoundError:
            print(f"⚠️ Kein gespeicherter Agent gefunden unter: saved_agents/{filename}_qtable.npy")
            return False

    def update_metrics(self, episode_reward):
        """Reward speichern und ggf. besten Agent sichern"""
        self.episode_rewards.append(episode_reward)
        if episode_reward > self.best_reward:
            self.best_reward = episode_reward
            self.save('mario_agent_best')