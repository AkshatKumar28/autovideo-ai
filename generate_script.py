import openai
import os

def generate_script(question):
    client = openai.AzureOpenAI(
        azure_endpoint=os.environ.get("AZURE_ENDPOINT"),
        api_key=os.environ.get("AZURE_KEY"),
        api_version=os.environ.get("AZURE_API_VERSION"),
    )

    completion = client.chat.completions.create(
        model=os.environ.get("MODEL_NAME"),
        messages=[
            {"role": "system", "content": f"""Generate a concise 10 sentence script for the following user query. Only give the actual content and nothing else. Dont user words such as Narrator or host. ONLY GIVE THE SCRIPT separated by full stops."""},
            {"role": "user", "content": f"""Here is the query:{question}"""}
        ],
        temperature=0.1,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
    )
    response = completion.choices[0].message.content
    return response
