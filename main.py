from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import numpy as np
import time
from q_learning_agent import QLearningAgent

# KEIN render_mode angeben, sonst Fehler!
env = gym_super_mario_bros.make('SuperMarioBros-1-1-v0')
env = JoypadSpace(env, SIMPLE_MOVEMENT)

# Agent initialisieren
agent = QLearningAgent(state_size=800, action_size=env.action_space.n)

# Versuche, gespeicherten Fortschritt zu laden
if agent.load("mario_agent_v2"):
    print("✅ Vorheriger Lernfortschritt geladen")
else:
    print("🚀 Neuer Lernprozess gestartet")

episodes = 1000
max_steps = 5000
stuck_threshold = 140
no_progress_reward = 0
render_training = True

save_interval = 1
last_x = []
jump_hold_frames = 7
jump_hold_counter = 0
last_action = 0

for episode in range(episodes):
    state = env.reset()
    total_reward = 0
    done = False
    mario_x = mario_y = 0
    current_state = (mario_x, mario_y)
    steps_without_progress = 0
    current_life = 2

    for step in range(max_steps):
        if jump_hold_counter > 0:
            action_to_take = last_action
            jump_hold_counter -= 1
        else:
            avg_x = np.mean(last_x[-3:]) if len(last_x) >= 3 else 0
            action = agent.choose_action(current_state, avg_x)
            last_action = action
            if 'A' in SIMPLE_MOVEMENT[action]:
                jump_hold_counter = jump_hold_frames
            action_to_take = action

        next_state, reward, done, info = env.step(action_to_take)

        if info['x_pos'] > mario_x:
            reward += 10  # Bonus für Fortschritt

        mario_x, mario_y = info['x_pos'], info['y_pos']

        if info['life'] < current_life:
            print("☠️ Mario gestorben.")
            done = True
            reward = -300
        current_life = info['life']
        total_reward += reward

        next_state_coords = (info['x_pos'], info['y_pos'])

        if reward <= no_progress_reward:
            steps_without_progress += 1
        else:
            steps_without_progress = 0

        if steps_without_progress >= stuck_threshold:
            print("⚠️ Kein Fortschritt – Episode wird abgebrochen.")
            done = True
            reward = -15

        agent.learn(current_state, action_to_take, reward, next_state_coords, done)
        current_state = next_state_coords

        if render_training:
            env.render()

        if done:
            break

    last_x.append(current_state[0])
    agent.update_metrics(total_reward)

    if (episode + 1) % save_interval == 0:
        agent.save("mario_agent_v2")
        print(f"💾 Fortschritt gespeichert bei Episode {episode + 1}")

    print(f"📊 Episode {episode + 1}/{episodes}, Reward: {total_reward:.2f}, "
          f"X: {current_state[0]}, Best: {agent.best_reward:.2f}")

# Am Ende zusätzlich nochmal speichern
agent.save("mario_agent_v2")
env.close()