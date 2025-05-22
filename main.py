from nes_py.wrappers import JoypadSpace
import gym
import gym_super_mario_bros
from gym_super_mario_bros.actions import *
import time
import numpy as np
from q_learning_agent import QLearningAgent

# Initialize environment
env = gym.make('SuperMarioBros-1-1-v0')
env = JoypadSpace(env, gym_super_mario_bros.actions.RIGHT_ONLY)

# Initialize Q-Learning agent
# State space: 80x10 grid (800 states)
# Action space: number of possible actions in RIGHT_ONLY
agent = QLearningAgent(state_size=800, action_size=env.action_space.n)

# Try to load previous training progress
if agent.load("mario_agent_best"):
    print("Loaded previous training progress")
else:
    print("Starting new training")

# Training parameters
episodes = 1000
max_steps = 5000
stuck_threshold = 150  # Number of steps without positive reward to consider Mario stuck
no_progress_reward = 0  # Reward threshold to consider as no progress

# Set to True to see the training, False for faster training
render_training = True
# Set to True to use human-readable mode (slower) or False for fast mode
human_mode = True

# Save progress every N episodes
save_interval = 1
last_x = []

for episode in range(episodes):
    state = env.reset()
    total_reward = 0
    done = False
    
    # Get initial state (x, y coordinates from info dict)
    mario_x = 0
    mario_y = 0
    current_state = (mario_x, mario_y)
    
    # Variables to track progress
    steps_without_progress = 0
    
    current_life = 2  # Track Mario's current life count
    for step in range(max_steps):
        # Choose action using Q-Learning agent
        
        action = agent.choose_action(current_state, np.array(last_x[-3:]).mean())
        
        # Take action
        next_state, reward, done, info = env.step(action)
        
        # Check if Mario died (life count decreased)
        if info['life'] < current_life:
            print(f"Mario died! Starting new episode.")
            done = True
            reward = -15  # Penalize death with negative reward
        current_life = info['life']
        
        total_reward += reward
        
        # Get next state coordinates from info dict
        next_mario_x = info['x_pos']
        next_mario_y = info['y_pos']
        next_state_coords = (next_mario_x, next_mario_y)
        
        # Check if Mario is making progress based on reward
        if reward <= no_progress_reward:
            steps_without_progress += 1
        else:
            steps_without_progress = 0
        
        # Terminate if Mario is stuck (no positive rewards for too long)
        if steps_without_progress >= stuck_threshold:
            print(f"Episode terminated: No progress for {stuck_threshold} steps")
            done = True
            reward = -15 
        
        # Learn from this experience
        agent.learn(current_state, action, reward, next_state_coords, done)
        
        # Update current state
        current_state = next_state_coords
        
        # Render the environment if enabled
        if render_training:
            env.render(mode='human' if human_mode else 'rgb_array')
        if done:
            break
    
    last_x.append(current_state[0])
    
    # Update and save metrics
    agent.update_metrics(total_reward)
    
    # Save progress periodically
    if (episode + 1) % save_interval == 0:
        agent.save()
        print(f"Progress saved at episode {episode + 1}")
    
    print(f"Episode {episode + 1}/{episodes}, Total Reward: {total_reward}, "
          f"Final Position: {next_mario_x}, Exploration Rate: {0:.2f}, "
          f"Best Reward: {agent.best_reward}")

# Save final state
agent.save()
env.close()
