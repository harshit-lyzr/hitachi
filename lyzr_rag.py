import requests
import time

def send_message(message):
    url = "https://agent.api.lyzr.app/v2/chat/"
    headers = {
        "Content-Type": "application/json",
        "x-api-key": "lyzr-V51VDLHozVHdcjJLXAjrzMvP"
    }
    data = {
       "user_id": "harshit@lyzr.ai",
    "agent_id": "6744243e61f92e3cfef02713",
    "session_id": "a462691f-2485-422e-921b-9fc8e4d14a58",
    "message": message
    }

    response = requests.post(url, json=data, headers=headers)

    return response.json()['response']

import concurrent.futures

def chat_with_agent_parallel(questions, max_workers=10):
    answers = []

    def get_answer(q):
        return send_message(q)

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = executor.map(get_answer, questions)

    return "".join(results)


import requests


def retrieve_rag_data(rag_id: str, query: str, retries=3, delay=1):
    url = f"https://rag-prod.studio.lyzr.ai/v3/rag/{rag_id}/retrieve/"
    params = {"query": query}
    headers = {
        "x-api-key": "sk-default-Kp8ZjZ3mlqbSJ6RqommLdD57Sd8CGOaG"
    }

    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)  # Wait before retrying
            else:
                print("Max retries reached. Returning None.")
                return ""


# data = retrieve_rag_data("67e12a665b7f2217c439d297","hello")
