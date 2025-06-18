import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import cv2
import os
import time

def load_q_table(filename='saved_agents/mario_agent_qtable.npy'):
    """Load the Q-table from file"""
    try:
        return np.load(filename)
    except FileNotFoundError:
        print(f"Q-table file not found at {filename}")
        return None

def load_level_image(filename='SuperMarioBrosMap1-1.png'):
    """Load the level image"""
    try:
        return cv2.imread(filename)
    except Exception as e:
        print(f"Error loading level image: {e}")
        return None

def create_q_value_heatmap(q_table, level_shape, y_offset):
    """Create a heatmap of Q-values for the level"""

    # reshape q value to grid dimensions
    qtable_2d = q_table.reshape(80, 10, -1)

    # Get the maximum Q-value for each state
    max_q_values = np.swapaxes(np.max(qtable_2d, axis=2), 0, 1)

    # Reverse y axis
    max_q_values = max_q_values[::-1]
    
    # move down by y_offset
    final = np.zeros_like(max_q_values)
    if y_offset < max_q_values.shape[0]:
        final[y_offset:] = max_q_values[:max_q_values.shape[0]-y_offset]


    final = np.pad(final, ((0, 0), (0, 55)), mode='constant', constant_values=0)

    # Resize to match the level image dimensions
    q_heatmap = cv2.resize(final, (level_shape[1], level_shape[0]), 
                          interpolation=cv2.INTER_NEAREST)
    
    return q_heatmap

def overlay_q_values(level_img, q_heatmap, alpha=0.4):
    """Overlay Q-values on the level image"""
    # Normalize Q-values to 0-255 range
    q_normalized = cv2.normalize(q_heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)

    # Create a colormap (blue to red)
    colormap = cv2.applyColorMap(q_normalized, cv2.COLORMAP_JET)
    
    # Enhance contrast of the colormap
    colormap = cv2.convertScaleAbs(colormap, alpha=1.5, beta=0)
    
    # Create a mask for high Q-values
    high_q_mask = q_normalized > 50
    high_q_mask = np.stack([high_q_mask] * 3, axis=-1)
    
    # Blend the colormap with the original image
    overlay = cv2.addWeighted(level_img, 1, colormap, alpha, 0)
    
    # Make high Q-values more prominent
    overlay[high_q_mask] = colormap[high_q_mask]
    
    return overlay

def save_visualization(img, filename='map.png'):
    """Save the visualization to a file"""
    # Create directory if it doesn't exist
    os.makedirs('visualizations', exist_ok=True)
    
    # Save image
    save_path = os.path.join('visualizations', filename)
    cv2.imwrite(save_path, img)

def visualize_q_values():
    # Load the Q-table and level image
    q_table = load_q_table()
    level_img = load_level_image()
    
    if q_table is None or level_img is None:
        return
    # Create Q-value heatmap
    q_heatmap = create_q_value_heatmap(q_table, level_img.shape[:2], 1)
    
    # Overlay Q-values on the level image
    overlay = overlay_q_values(level_img, q_heatmap)
    
    # Save the visualization
    save_visualization(overlay)

def main():
    try:
        while True:
            visualize_q_values()
            time.sleep(1)
            print(f"Updated map visualization at {time.strftime('%H:%M:%S')}")
    except KeyboardInterrupt:
        print("\nVisualization stopped by user")

if __name__ == "__main__":
    main()

