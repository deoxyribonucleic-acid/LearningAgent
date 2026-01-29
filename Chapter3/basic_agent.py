from backend import OpenAILLM
from dotenv import load_dotenv
import os
if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4")
    api_key = os.getenv("OPENAI_API_KEY", "your_api_key_here")

    llm = OpenAILLM(model_name=model_name, api_key=api_key)
    
    message = llm.construct_prompt(
        sys_prompt="You are a helpful assistant.",
        usr_prompt="Tell me about fast sorting algorithms.",
        image_input=None
    )

    try:
        response = llm.inference(messages=message, temperature=0.5)
        if response:
            print("Final Response:", response)

    except Exception as e:
        print(f"Error during inference: {e}")
