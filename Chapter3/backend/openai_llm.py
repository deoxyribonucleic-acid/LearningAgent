from .llm_base import LLMBase
from openai import OpenAI 
from typing import List, Dict
from utils import image2base64
class OpenAILLM(LLMBase):
    def __init__(self, model_name: str, api_key: str):
        super().__init__(model_name)
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key)

    def inference(self, messages: List[Dict[str,str]], **kwargs) -> str:
        print(f"Sending prompt to OpenAI model '{self.model_name}'.")
        
        try:
            response = self.client.chat.completions.create(
                model = self.model_name,
                messages = messages,
                temperature = kwargs.get("temperature", 0.7),
                stream = True
            )

            print("Received response from OpenAI model.")
            collected_chunks = []
            for chunk in response:
                content = chunk.choices[0].delta.content or ""
                print(content, end='', flush=True)
                collected_chunks.append(content)
            print()
            return ''.join(collected_chunks)
        
        except Exception as e:
            print(f"An error occurred during inference: {e}")
            return ""
        
    def construct_prompt(self, sys_prompt, usr_prompt, image_input, **kwargs) -> List[Dict[str, str]]:
        messages = [
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": usr_prompt}
        ]
        
        if image_input:
            image_message = {
                "role": "user",
                "content": f"url:data:image/png;base64,{image2base64(image_input)}"
            }
            messages.insert(1, image_message)
        
        return messages