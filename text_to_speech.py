import os
import json
import requests
from moviepy.editor import AudioFileClip
import pathlib

elevenlabs_api_key = os.environ.get("ELEVENLABS_API_KEY")
url = "https://api.elevenlabs.io/v1/text-to-speech/"
voices_list_url = "https://api.elevenlabs.io/v1/voices"

def voices_list(elevenlabs_api_key: str):
    try:
        headers = {"Content-Type": "application/json", "xi-api-key": elevenlabs_api_key}
        response = requests.get(voices_list_url, headers=headers)
        response.raise_for_status()
        return json.loads(response.text)['voices']
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Could not get voices list: {err}")
    except Exception as e:
        raise Exception(f"Error in voices_list: {e}")

def text_to_speech_elevenlabs(text: str, output_dir: str = "Audio", output_file: str = "output.wav"):
    try:
        voices = voices_list(elevenlabs_api_key)
        voice_id = [voice["voice_id"] for voice in voices if voice["name"] == "Rachel"][0]
        print(f"Generating audio for {text}, outputfile: {output_file}")
        payload = {
            "text": text,
            "voice_settings": {
                "similarity_boost": 0.75,
                "stability": 0.3,
                "style": 0,
                "use_speaker_boost": True
            }
        }
        headers = {"Content-Type": "application/json", "xi-api-key": elevenlabs_api_key, "Accept": "audio/mpeg"}
        response = requests.post(url + voice_id, json=payload, headers=headers)
        response.raise_for_status()
        pathlib.Path(output_dir).mkdir(parents=True, exist_ok=True)
        target_file = f'{output_dir}/{output_file}'
        with open(target_file, 'wb') as f:
            f.write(response.content)
        return target_file, AudioFileClip(target_file).duration
    except requests.exceptions.HTTPError as err:
        raise Exception(f"Failed to generate audio: {err}")
    except Exception as e:
        raise Exception(f"Error in text_to_speech_elevenlabs: {e}")
