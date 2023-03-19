import os
from dotenv import load_dotenv
import openai  
from base64 import b64decode 

# PROMPT = "Corgi with hat"

# openai.api_key = secret_key

class imageGeneratorOpenAI: 
    def __init__(self): 
        self.response = None
        load_dotenv() 
        secret_key = os.getenv('OPENAI_API_KEY')
        openai.api_key = secret_key

    def generate_image(self, prompt, num_image=1, size='512x512', output_format='b64_json'): 
        self.response = openai.Image.create(
            prompt=prompt,
            n=1,
            size=size,
            response_format='b64_json'
        )

    def write_image(self, prefix='result_images/original_image'): 
        # prefix = 'result_images/original_image'
        with open(f'{prefix}.jpg', 'wb') as f: 
            f.write(b64decode(self.response['data'][0]['b64_json']))