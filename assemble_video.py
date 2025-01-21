import numpy as np
from moviepy.editor import TextClip, CompositeVideoClip, concatenate_videoclips

def assemble_final_video(captions_info, video_clips, fps=24):
    final_clips = []

    for caption, clip in zip(captions_info, video_clips):
        sentence = caption['text']
        words = sentence.split()
        total_characters = sum(len(word) for word in words) 
        total_duration = caption['duration']
        word_durations = [(len(word) / total_characters) * total_duration for word in words]

        word_start_times = np.cumsum([0] + word_durations[:-1]) 

        text_clips = []
        for word, start_time, duration in zip(words, word_start_times, word_durations):
            word_clip = TextClip(word, fontsize=50, color='white', font='Arial-Bold', method='caption', size=(clip.size[0]*0.8, None))
            word_clip = word_clip.set_position('center').set_duration(duration).set_start(start_time)
            word_clip = word_clip.fadein(0.1)  
            text_clips.append(word_clip)

        if text_clips: 
            all_clips = [clip] + text_clips 
            composite_clip = CompositeVideoClip(all_clips, size=clip.size) 
            final_clips.append(composite_clip)
        else:
            final_clips.append(clip.set_duration(total_duration))

    final_video = concatenate_videoclips(final_clips, method="compose")
    final_video.fps = fps
    return final_video
