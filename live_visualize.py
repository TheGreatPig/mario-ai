import numpy as np
import matplotlib.pyplot as plt
import json
import os
import time

def load_qtable(filename='mario_agent'):
    """Load Q-table and metrics from saved files"""
    try:
        qtable = np.load(f'saved_agents/{filename}_qtable.npy')
        with open(f'saved_agents/{filename}_metrics.json', 'r') as f:
            metrics = json.load(f)
        return qtable, metrics
    except FileNotFoundError:
        return None, None

def create_visualization():
    """Create and save the visualization"""
    # Try to load the best agent first, fall back to regular agent if not found
    qtable, metrics = load_qtable('mario_agent')
    if qtable is None:
        qtable, metrics = load_qtable('mario_agent_best')
    if qtable is None:
        print("No Q-table found")
        return
    
    # Create figure and subplots
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    
    # Reshape Q-table to 2D grid (80x10)
    qtable_2d = qtable.reshape(80, 10, -1)
    
    # Plot 1: Heatmap of best actions
    best_actions = np.argmax(qtable_2d, axis=2)
    im1 = axes[0].imshow(best_actions.T, cmap='viridis', aspect='auto')
    axes[0].set_title('Best Actions for Each State')
    axes[0].set_xlabel('X Position (0-79)')
    axes[0].set_ylabel('Y Position (0-9)')
    plt.colorbar(im1, ax=axes[0], label='Action Index')
    
    # Plot 2: Heatmap of maximum Q-values
    max_q_values = np.max(qtable_2d, axis=2)
    im2 = axes[1].imshow(max_q_values.T, cmap='hot', aspect='auto')
    axes[1].set_title('Maximum Q-Values')
    axes[1].set_xlabel('X Position (0-79)')
    axes[1].set_ylabel('Y Position (0-9)')
    plt.colorbar(im2, ax=axes[1], label='Q-Value')
    
    # Plot 3: Reward history
    if metrics and 'episode_rewards' in metrics:
        rewards = metrics['episode_rewards']
        window = min(100, len(rewards))
        recent_rewards = rewards[-window:]
        episodes = range(len(rewards) - window + 1, len(rewards) + 1)
        
        axes[2].plot(episodes, recent_rewards, 'b-', label='Episode Reward')
        axes[2].set_title('Recent Reward History')
        axes[2].set_xlabel('Episode')
        axes[2].set_ylabel('Reward')
        axes[2].legend()
        axes[2].grid(True)
    
    # Add training metrics
    if metrics:
        metrics_text = f"Best Reward: {metrics['best_reward']:.2f}\n"
        metrics_text += f"Exploration Rate: {metrics['exploration_rate']:.3f}\n"
        metrics_text += f"Episodes: {len(metrics['episode_rewards'])}"
        
        plt.figtext(0.5, 0.01, metrics_text, ha='center', fontsize=10, 
                    bbox=dict(facecolor='white', alpha=0.8))
    
    plt.tight_layout()
    plt.savefig('saved_agents/live_visualization.png')
    plt.close()
    print(f"Updated visualization at {time.strftime('%H:%M:%S')}")

def main():
    # Create saved_agents directory if it doesn't exist
    os.makedirs('saved_agents', exist_ok=True)
    
    try:
        while True:
            create_visualization()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nVisualization stopped by user")

if __name__ == "__main__":
    main() 