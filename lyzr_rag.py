import os
import requests
import time
from dotenv import load_dotenv
load_dotenv()


def retrieve_rag_data(rag_id: str, query: str, retries=3, delay=1):
    url = f"https://rag-prod.studio.lyzr.ai/v3/rag/{rag_id}/retrieve/"
    params = {"query": query}
    headers = {
        "x-api-key": os.getenv("API_KEY")
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


