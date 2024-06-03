import json
from openai import OpenAI

def generate_image(prompt, model):
                    
    client = OpenAI()

    response = client.images.generate(
        model=model,
        prompt=prompt,
        n=1,
        size="1024x1024"
    )

    return response

def generate_json_object(message, system_message="", temperature=0):

    client = OpenAI()

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        response_format= { "type": "json_object" },
        temperature=temperature,
        messages=[
            {"role": "system", "content": str(system_message) + " You will generate an answer in json format."},
            {"role": "user", "content": message}
        ]
    )

    return json.loads(response.choices[0].message.content)