import openai
import requests
import os
import pathlib

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

non_text_prompts = "Focus on specific, visually representable elements." \
                   "Keep the image simple." \
                   "Do not include any form of text, equations or captions. Focus on what the sentence is trying to convey and generate based on that."

image_gen_style = "3d render. Hyper-realistic 4k."

def generate_image_from_text(description, output_path):
    response = client.images.generate(
        model="dall-e-3",
        prompt=" Generate an image based on the following description: " + description + non_text_prompts + image_gen_style,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    image_url = response.data[0].url
    response = requests.get(image_url)
    with open(output_path, 'wb') as file:
        file.write(response.content)
    return output_path
