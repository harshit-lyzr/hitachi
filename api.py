import os
from lyzr_rag import retrieve_rag_data
from pydantic import BaseModel
from typing import List
import concurrent.futures
from fastapi import FastAPI
import time
from lyzr_agent import chat_with_agent
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific origins for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

AGENT_1 = os.getenv("AGENT_1")
AGENT_2 = os.getenv("AGENT_2")
AGENT_3 = os.getenv("AGENT_3")
SECTION_Q = os.getenv("SECTION_Q")
SECTION_A = os.getenv("SECTION_A")
RAG_ID = os.getenv("RAG_ID")


@app.get("/health")
def health_check():
     """
     Health check endpoint to verify if the service is running.
     """
     return {"status": "healthy"}

@app.post("/generate_outline/")
async def generate_outline(topic: str,pages: int, words: int):
    start = time.time()

    # subtopic = chat_with_agent(AGENT_1, f"Topic: {topic}")
    outline = chat_with_agent(AGENT_2, f"Topic: {topic} No of Pages:{pages} Words per page: {words}")
    refine_outline = chat_with_agent(AGENT_3,
                                     f"Topic: {topic} Draft Outline: {outline} No of Pages:{pages} Words per page: {words}")

    refined_sections = refine_outline.split("\n\n")
    end = time.time()

    return {"outline": refined_sections, "execution_time": end - start}



# Define Pydantic model for input
class OutlineInput(BaseModel):
    outlines: List[str]
    words: int


# Modified to not be async since we're using it with executor.map
def process_outline_sync(outline):
    print("outline entered")
    # Step 1: Get sectional questions
    sectional_question = chat_with_agent(SECTION_Q, f"Topic: {outline}")
    ques = sectional_question.split('\n\n')

    # Step 2: Retrieve RAG data in parallel using executor.map()
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        print("RAG initiated")
        responses = list(executor.map(lambda q: (q, retrieve_rag_data(RAG_ID, q)), ques))
        print("RAG Done")

    combined_responses = {q: [res["text"] for res in resp.get("results", [])] for q, resp in responses}
    print("combined answer done")

    # Step 3: Generate section answer (non-async version)
    section_answer = chat_with_agent(SECTION_A,
                                     f"Context: {combined_responses}\n\nSECTION OUTLINE: {outline}")
    print("section answer generated")
    return section_answer


@app.post("/process_outline/")
async def process_outline_api(input_data: OutlineInput):
    start = time.time()

    # If chat_with_agent is actually asynchronous, you need a different approach
    # Using a regular ThreadPoolExecutor for non-async functions
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(process_outline_sync, input_data.outlines))

    end = time.time()
    return {"processed_outlines": results, "total_time": end - start}
