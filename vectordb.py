import chromadb
import os
import pandas as pd
from uuid import uuid4
from groq import Groq
from dotenv import load_dotenv
from pathlib import Path
load_dotenv()
GROQ_MODEL = os.getenv("GROQ_MODEL")

VECTORDB_PATH=Path.cwd()/'vector store'
FAQ_PATH=Path.cwd()/'resources'/'faq_data.csv'
if not os.path.exists(VECTORDB_PATH):
    os.makedirs(VECTORDB_PATH)
client = chromadb.PersistentClient(path=VECTORDB_PATH)
llm_faq=Groq()

def initiate_vector_db():

    if "faq" in [col.name for col in client.list_collections()]:
        return
    else:

        collection_faq = client.create_collection('faq')
        # data collection
        df = pd.read_csv(FAQ_PATH)
        questions = df['question'].tolist()
        answers = df['answer'].tolist()
        collection_faq.add(
            documents=questions,
            metadatas=[{"answer":a} for a in answers],
            ids=[str(uuid4()) for _ in range(len(questions))]
         )
        print(f"FAQ Data successfully ingested into Chroma collection: faq")

def get_relevant_qa(query):
    collection = client.get_collection("faq")
    result=collection.query(query_texts=query,n_results=2)
    return ''.join([r['answer'] for r in result['metadatas'][0]])


def generate_answer(query, context):
    prompt = f'''
            Given the following context and question, generate answer based on this context only.
            If the answer is not found in the context, kindly state "I don't know". Don't try to make up an answer.

            CONTEXT: {context}

            QUESTION: {query}

            '''
    answer = llm_faq.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model=GROQ_MODEL,
        max_tokens=None)
    return answer.choices[0].message.content

def faq_chain(query):
    initiate_vector_db()
    context=get_relevant_qa(query)
    answer = generate_answer(query, context)
    return answer

if __name__=="__main__":
    initiate_vector_db()
    query = "Do you take cash as a payment option?"
    response=get_relevant_qa(query)
    print(response)
    answer=generate_answer(query, response)
    print(answer)