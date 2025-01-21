import pathlib
import numpy as np
from nltk.tokenize import sent_tokenize
from text_to_speech import text_to_speech_elevenlabs
from generate_script import generate_script
from generate_image import generate_image_from_text
from create_video_clip import create_video_clip
from assemble_video import assemble_final_video
from dotenv import load_dotenv
load_dotenv()
print("All imports successful")

pathlib.Path("Audio").mkdir(parents=True, exist_ok=True)
pathlib.Path("Images").mkdir(parents=True, exist_ok=True)

def create_video_from_question(question: str) -> None:
    try:
        script = generate_script(question)
    except Exception as e:
        print(f"Error generating script: {e}")
        return
    
    print(f"Generated script: {script}")
    captions_info = []
    video_clips = []

    try:
        sentences = sent_tokenize(script)
    except Exception as e:
        print(f"Error tokenizing sentences: {e}")
        return
    
    current_time = 0

    for i, sentence in enumerate(sentences):
        zoom_in = i % 2 == 0 
        try:
            audio_path, audio_duration = text_to_speech_elevenlabs(sentence, output_file=f"{current_time}.mp3")
        except Exception as e:
            print(f"Error generating audio for sentence {i}: {e}")
            return
        
        try:
            image_path = generate_image_from_text(sentence, f"Images/{current_time}.jpg")
        except Exception as e:
            print(f"Error generating image for sentence {i}: {e}")
            return
        
        try:
            video_clip = create_video_clip(image_path, audio_path, audio_duration, zoom_in=zoom_in)
        except Exception as e:
            print(f"Error creating video clip for sentence {i}: {e}")
            return
        
        video_clips.append(video_clip)
        
        captions_info.append({
            "text": sentence,
            "start_time": current_time,
            "duration": audio_duration
        })
        current_time += audio_duration + 0.5

    try:
        final_video = assemble_final_video(captions_info, video_clips)
    except Exception as e:
        print(f"Error assembling final video: {e}")
        return
    
    try:
        final_video.write_videofile("final_output_video_2.mp4", codec="libx264", fps=24)
    except Exception as e:
        print(f"Error writing final video file: {e}")
        return

if __name__ == "__main__":
    question = "Generate a script for the importance of healthy eating."
    create_video_from_question(question)
