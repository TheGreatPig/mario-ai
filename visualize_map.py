import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import cv2
import os
import time

def load_q_table(filename='saved_agents/mario_agent_qtable.npy'):
    try:
        return np.load(filename)
    except FileNotFoundError:
        print(f"Q-table file not found at {filename}")
        return None

def load_level_image(filename='SuperMarioBrosMap1-1.png'):
    try:
        return cv2.imread(filename)
    except Exception as e:
        print(f"Error loading level image: {e}")
        return None

def create_action_heatmap(q_table, level_shape, y_offset):
    # reshape q value to grid dimensions
    qtable_2d = q_table.reshape(120, 10, 5)

    # Get the best action (index of max Q-value) for each state
    best_actions = np.swapaxes(np.argmax(qtable_2d, axis=2), 0, 1)

    # Reverse y axis
    best_actions = best_actions[::-1]
    
    # move down by y_offset
    final = np.zeros_like(best_actions)
    if y_offset < best_actions.shape[0]:
        final[y_offset:] = best_actions[:best_actions.shape[0]-y_offset]

    final = np.pad(final, ((0, 0), (0, 20)), mode='constant', constant_values=0)

    # Resize to match the level image dimensions (use nearest for categorical data)
    action_heatmap = cv2.resize(final, (level_shape[1], level_shape[0]), 
                          interpolation=cv2.INTER_NEAREST)
    
    return action_heatmap

def overlay_actions(level_img, action_heatmap, alpha=0.6):
    # Define a categorical colormap for 5 actions
    action_colors = np.array([
        [255, 0, 0],    # Action 0: Red NOOP
        [0, 255, 0],    # Action 1: Green RIGHT
        [0, 0, 255],    # Action 2: Blue RIGHT A
        [255, 255, 0],  # Action 3: Yellow RIGHT B
        [255, 0, 255],  # Action 4: Magenta RIGHT A B
    ], dtype=np.uint8)

    # Map each action index to its color
    color_map = action_colors[action_heatmap % 5]

    # Blend the color map with the original image
    overlay = cv2.addWeighted(level_img, 1 - alpha, color_map, alpha, 0)
    return overlay

def save_visualization(img, filename='map.png'):
    # Create directory if it doesn't exist
    os.makedirs('visualizations', exist_ok=True)
    
    # Save image
    save_path = os.path.join('visualizations', filename)
    cv2.imwrite(save_path, img)

def visualize_actions():
    # Load the Q-table and level image
    q_table = load_q_table()
    level_img = load_level_image()
    
    if q_table is None or level_img is None:
        return
    # Create action heatmap
    action_heatmap = create_action_heatmap(q_table, level_img.shape[:2], 1)
    
    # Overlay actions on the level image
    overlay = overlay_actions(level_img, action_heatmap)
    
    # Save the visualization
    save_visualization(overlay, filename='map_actions.png')

def main():
    try:
        while True:
            visualize_actions()
            time.sleep(1)
            print(f"Updated map action visualization at {time.strftime('%H:%M:%S')}")
    except KeyboardInterrupt:
        print("\nVisualization stopped by user")

if __name__ == "__main__":
    main()

