from moviepy.editor import ImageClip, AudioFileClip
from animation import zoom_effect

def create_video_clip(image_path, audio_path, expected_duration, zoom_in):
    delay = 0.5
    audio_clip = AudioFileClip(audio_path)
    image_clip = ImageClip(image_path)

    min_duration = min(audio_clip.duration, expected_duration)
    audio_clip = audio_clip.set_duration(min_duration)
    image_clip = image_clip.set_duration(min_duration + delay)

    video_clip = image_clip.set_audio(audio_clip)
    video_clip = zoom_effect(video_clip, start_with_zoom_in=zoom_in)
    return video_clip
