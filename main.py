from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
import gym
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
import numpy as np
import time
from q_learning_agent import QLearningAgent

# Level 1-1 laden
env = gym.make('SuperMarioBros-1-1-v0')
env = JoypadSpace(env, gym_super_mario_bros.actions.RIGHT_ONLY)

# Q-Learning Agent initialisieren
# Action space: Für RIGHT_ONLY 5 Zustände (['NOOP'], ['right'], ['right', 'A'],['right', 'B'], ['right', 'A', 'B'],)
agent = QLearningAgent(action_size=env.action_space.n)

# Gespeicherte Trainingsdaten laden, falls vorhanden
if agent.load("mario_agent_best"):
    print("Loaded previous training progress")
else:
    print("🚀 Neuer Lernprozess gestartet")

episodes = 1000000
max_steps = 5000
stuck_threshold = 150  # Anzahl an Schritten ohne positive Belohnung, ab der Mario zurückgesetzt wird (weil kein Fortschritt)
no_progress_reward = 0 

# Bei True wird das Spiel gerendert, False für schnelleres Training
render_training = True

# Intervall in dem die Trainingsdaten abgespeichert werden (in Episoden)
save_interval = 10
last_x = []
jump_hold_frames = 7
jump_hold_counter = 0
last_action = 0


for episode in range(episodes):
    state = env.reset()
    total_reward = 0
    done = False
    mario_x = 0
    mario_y = 0
    current_state = (mario_x, mario_y)
    
    steps_without_progress = 0
    
    current_life = 2  # Marios Leben werden gespeichert

    for step in range(max_steps):

        if jump_hold_counter > 0:
            action_to_take = last_action
            jump_hold_counter -= 1
        else:
            # Aktion auswählen mithilfe des Q-Learning Agenten
            action = agent.choose_action(current_state, np.array(last_x[-3:]).mean())
            
            # Wenn Sprung-Aktion gewählt wurde, halte sie für mehrere Frames
            if 'A' in SIMPLE_MOVEMENT[action]:
                jump_hold_counter = jump_hold_frames
                last_action = action
            
            action_to_take = action

        # Aktion wird ausgeführt
        next_state, reward, done, info = env.step(action_to_take)
        
        total_reward += reward
        
        # Zustands Koordinaten werden vom info dict abgerufen
        next_mario_x = info['x_pos']
        next_mario_y = info['y_pos']
        next_state_coords = (next_mario_x, next_mario_y)
        
        # Check ob Mario Fortschritt macht
        if reward <= no_progress_reward:
            steps_without_progress += 1
        else:
            steps_without_progress = 0
        
        # Terminieren wenn Mario keinen Fortschritt macht
        if steps_without_progress >= stuck_threshold:
            print("⚠️ Kein Fortschritt – Episode wird abgebrochen.")
            done = True
            reward = -15 
        
        # Lern-Funktion (Q-Tabelle wird verändert)
        agent.learn(current_state, action, reward, next_state_coords, done)
        
        current_state = next_state_coords
        
        # Rendern der Umgebung
        if render_training:
            env.render(mode='human')
            # time.sleep(0.01) # Echtzeit-Rendering
        if done:
            break

    last_x.append(current_state[0])
    
    # Speichern der Performanzdaten
    agent.update_metrics(total_reward)
    
    # Speichern der Trainingsdaten
    if (episode + 1) % save_interval == 0:
        agent.save()
        print(f"Progress saved at episode {episode + 1}")
    
    print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}, "
          f"Final Position: {next_mario_x}, "f"Best Reward: {agent.best_reward}")

# Speichern des finalen Zustands
agent.save()
env.close()