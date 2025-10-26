from  groq import Groq
from dotenv import load_dotenv
import os
from pathlib import Path
from groq import Groq
import re
import pandas as pd
import sqlite3

load_dotenv()
GROQ_MODEL = os.getenv('GROQ_MODEL')
SQLITE_DB_PATH =  Path.cwd() / "resources/db.sqlite"

llm_groq_sql_client = Groq(max_retries=2)



def get_sql_query(query):
    prompt = """You are an expert in understanding the database schema and generating SQL queries for a natural language question asked
            pertaining to the data you have. The schema is provided in the schema tags. 
            <schema> 
            table: product 

            fields: 
            product_link - string (hyperlink to product)	
            title - string (name of the product)	
            brand - string (brand of the product)	
            price - integer (price of the product in Indian Rupees)	
            discount - float (discount on the product. 10 percent discount is represented as 0.1, 20 percent as 0.2, and such.)	
            avg_rating - float (average rating of the product. Range 0-5, 5 is the highest.)	
            total_ratings - integer (total number of ratings for the product)

            </schema>
            Make sure whenever you try to search for the brand name, the name can be in any case. 
            So, make sure to use %LIKE% to find the brand in condition. Never use "ILIKE". 
            Create a single SQL query for the question provided. 
            The query should have all the fields in SELECT clause (i.e. SELECT *)

            Just the SQL query is needed, nothing more. Always provide the SQL in between the <SQL></SQL> tags.
            """


    response = llm_groq_sql_client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.1,# or another supported model
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content":f" user_input:{query}"}
        ]
    )
    return (response.choices[0].message.content)

def query_to_dic(sql_query):
    pattern = "<SQL>(.*?)</SQL>"
    matches = re.findall(pattern, sql_query, re.DOTALL)

    if len(matches) == 0:
        return "Sorry, ai is not able to generate a query for your question"

    # print(matches[0].strip())
    clean_sql_query = matches[0].strip()
    if clean_sql_query.strip().lower().startswith('select'):
        with sqlite3.connect(SQLITE_DB_PATH) as conn:
            df = pd.read_sql_query(clean_sql_query, conn)

    else:
        return "Sorry, there was a problem executing SQL query"

    context = df.to_dict(orient='records')
    return context

def generate_Human_answer(question,context):
    prompt = '''
    You are a helpful assistant. Use only the provided SQL output (dictionary or dataframe) to answer the question.

    Rules:
    - No external knowledge or assumptions.
    - Respond naturally and clearly.
    - If context includes product data, list each product on a new line in this format:
      <index>. <title>: Rs. <price> (<discount> off), Rating: <rating> <link>
    - If context is invalid,reply:
     ** "No products found matching the given criteria." **
    Context:
    {Context}

    Question:
    {Question}

    Answer:
    '''



    response = llm_groq_sql_client.chat.completions.create(
        model=GROQ_MODEL,
        temperature=0.1,  # or another supported model
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": f" Question:{question},Context:{context}"}
        ]
    )
    return (response.choices[0].message.content)
def sql_chain(user_query):
    sql_query=get_sql_query(user_query)   #user_query-->sql_query
    context=query_to_dic(sql_query)               #sql_query--->data (data from sqlite database in form of dictionary)
    response=generate_Human_answer(sql_query,context)
    return response

if __name__ == '__main__':

    query="show me top shoe brand  that have highest rating"
    query ='show me product name of nike brand with heighest price'
    res=get_sql_query(query)
    print(res)
    print("----------- 1---------")
    context=query_to_dic(res)
    print(pd.DataFrame.from_dict(context))
    print(context)
    print("------------2--------")
    response=generate_Human_answer(query,context)
    print(response)
    print("-------------3-------")
