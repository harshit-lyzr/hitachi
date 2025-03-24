import requests
from dotenv import load_dotenv
import os

load_dotenv()

def chat_with_agent(agent_id, message):
    url = 'https://agent-prod.studio.lyzr.ai/v3/inference/chat/'
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': os.getenv("API_KEY")
    }
    data = {
        "user_id": "harshit@lyzr.ai",
        "agent_id": agent_id,
        "session_id": "123",
        "message": message
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['response']

# Example usage
# response = chat_with_agent("67dbc903156a494cf6314224", "Hello, Agent!")
# print(response)