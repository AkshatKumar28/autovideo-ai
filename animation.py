import numpy as np
import cv2

def pendulum_effect(clip, amplitude_x=30, frequency_x=0.2, amplitude_y=20, frequency_y=0.25):

    def oscillate(get_frame, t):
        frame = get_frame(t)
        x_movement = int(amplitude_x * np.sin(2 * np.pi * frequency_x * t))
        y_movement = int(amplitude_y * np.sin(2 * np.pi * frequency_y * t))
        frame = np.roll(frame, x_movement, axis=1)  # Horizontal roll
        frame = np.roll(frame, y_movement, axis=0)  # Vertical roll
        return frame

    return clip.fl(oscillate)

def zoom_effect(clip, zoom_range=(1.0, 1.5), duration=10, start_with_zoom_in=True):
    half_cycle = duration / 2

    def zoom(get_frame, t):
        cycle_time = t % duration
        if start_with_zoom_in:
            if cycle_time < half_cycle:
                progress = cycle_time / half_cycle
            else:
                progress = 2 - cycle_time / half_cycle
        else:
            if cycle_time < half_cycle:
                progress = 2 - (cycle_time / half_cycle)
            else:
                progress = cycle_time / half_cycle

        current_zoom = zoom_range[0] + (zoom_range[1] - zoom_range[0]) * progress
        new_frame = get_frame(t)
        return cv2.resize(new_frame, None, fx=current_zoom, fy=current_zoom, interpolation=cv2.INTER_LINEAR)

    return clip.fl(zoom)