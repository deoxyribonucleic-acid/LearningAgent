from agents.reflect import ReflectAgent
from backend import OpenAILLM
from dotenv import load_dotenv
import os

if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4")
    api_key = os.getenv("OPENAI_API_KEY", "your_api_key_here")

    llm = OpenAILLM(model_name=model_name, api_key=api_key)
    
    agent = ReflectAgent(llm=llm, max_iterations=3)

    user_query = "任务： 编写一个Python函数，找出1到n之间所有的素数"
    
    try:
        result = agent.run(usr_prompt=user_query, image_input=None)
        if result:
            print("Final Answer:", result)
    except Exception as e:
        print(f"Error during agent execution: {e}")