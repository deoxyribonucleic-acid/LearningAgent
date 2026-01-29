from backend import OpenAILLM
from dotenv import load_dotenv
from agents.react import ReActAgent
import os
if __name__ == "__main__":
    load_dotenv()  # Load environment variables from .env file
    model_name = os.getenv("OPENAI_MODEL_NAME", "gpt-4")
    api_key = os.getenv("OPENAI_API_KEY", "your_api_key_here")

    llm = OpenAILLM(model_name=model_name, api_key=api_key)
    
    agent = ReActAgent(llm=llm, max_steps=10)

    user_query = "请帮我搜索目前购买Apple Watch Series 11 的最佳网站和对应的价格。"
    
    try:
        result = agent.run(usr_prompt=user_query, image_input=None)
        if result:
            print("Final Answer:", result)
    except Exception as e:
        print(f"Error during agent execution: {e}")