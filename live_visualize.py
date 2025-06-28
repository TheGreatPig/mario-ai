import numpy as np
import matplotlib.pyplot as plt
import json
import os
import time

def load_qtable(filename='mario_agent'):
    """Lädt Q-Tabelle und Metriken"""
    try:
        qtable = np.load(f'saved_agents/{filename}_qtable.npy')
        with open(f'saved_agents/{filename}_metrics.json', 'r') as f:
            metrics = json.load(f)
        return qtable, metrics
    except FileNotFoundError:
        print("❌ Q-table oder metrics-Datei nicht gefunden.")
        return None, None
    except Exception as e:
        print(f"❌ Fehler beim Laden: {e}")
        return None, None

def create_visualization(fig, axes):
    """Aktualisiert die Visualisierung live"""
    qtable, metrics = load_qtable()
    if qtable is None:
        return

    axes[0].clear()
    axes[1].clear()
    axes[2].clear()

    qtable_2d = qtable.reshape(80, 10, -1)

    # Plot 1: Best Actions
    best_actions = np.argmax(qtable_2d, axis=2)
    im1 = axes[0].imshow(best_actions.T, cmap='viridis', aspect='auto')
    axes[0].set_title('Best Actions for Each State')
    axes[0].set_xlabel('X Position (0–79)')
    axes[0].set_ylabel('Y Position (0–9)')
    fig.colorbar(im1, ax=axes[0], label='Action Index')

    # Plot 2: Max Q-Values
    max_q_values = np.max(qtable_2d, axis=2)
    im2 = axes[1].imshow(max_q_values.T, cmap='hot', aspect='auto')
    axes[1].set_title('Maximum Q-Values')
    axes[1].set_xlabel('X Position (0–79)')
    axes[1].set_ylabel('Y Position (0–9)')
    fig.colorbar(im2, ax=axes[1], label='Q-Value')

    # Plot 3: Reward History
    if metrics and 'episode_rewards' in metrics:
        rewards = metrics['episode_rewards']
        window = min(100, len(rewards))
        recent_rewards = rewards[-window:]
        episodes = range(len(rewards) - window + 1, len(rewards) + 1)
        axes[2].plot(episodes, recent_rewards, 'b-', label='Episode Reward')
        axes[2].set_title('Recent Reward History')
        axes[2].set_xlabel('Episode')
        axes[2].set_ylabel('Reward')
        axes[2].grid(True)
        axes[2].legend()

    # Optionaler Text mit Infos
    if metrics:
        metrics_text = f"Best Reward: {metrics['best_reward']:.2f}\nEpisodes: {len(metrics['episode_rewards'])}"
        fig.text(0.5, 0.01, metrics_text, ha='center', fontsize=10,
                 bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    fig.canvas.draw()

def main():
    os.makedirs('visualizations', exist_ok=True)
    plt.ion()  # Interaktiver Modus für Live-Update
    fig, axes = plt.subplots(1, 3, figsize=(20, 6))

    try:
        while True:
            create_visualization(fig, axes)
            print(f"✅ Updated metric visualization at {time.strftime('%H:%M:%S')}")
            plt.pause(1)  # wartet 1 Sekunde
    except KeyboardInterrupt:
        print("🛑 Live visualization stopped by user.")
        plt.ioff()
        plt.close()

if __name__ == "__main__":
    main()
