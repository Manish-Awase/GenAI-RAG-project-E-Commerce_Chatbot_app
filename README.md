# 💬 E-Commerce Chatbot  
### GenAI RAG Project using LLaMA 3.3 + GROQ

This project is a proof of concept (PoC) for an intelligent chatbot designed to enhance user experience on an e-commerce platform. It leverages Retrieval-Augmented Generation (RAG) with real-time database access to deliver accurate, context-aware responses by identifying user intent.

---

## ⚡ Quick Scenario

- User: “Do you offer cash on delivery for electronics?”  
  → Chatbot (faq intent): “Yes, cash on delivery is available for electronics.”

- User: “Show me all Puma sneakers under ₹2500.”  
  → Chatbot (sql intent): Returns a real-time list of matching products from the database.

---

## 📁 Folder Structure

├── app #Core chatbot logic and 
               Streamlit UI

---

## 🧠 Supported Intents

The chatbot currently understands and responds to two primary types of user queries:

- **`faq`**: For general platform-related questions.  
  

- **`sql`**: For product-specific queries that require real-time database access.  
  

---

## 🖼️ Screenshots

**Chatbot Interface**  
![Product Screenshot](resources/product-ss.png)

**System Architecture**  
![Architecture Diagram](resources/architecture-diagram.png)

---

### Set-up & Execution

1. Run the following command to install all dependencies. 

    ```bash
    pip install -r requirements.txt
    ```

1. Inside app folder create a .env file with your GROQ credentials as follows:
    ```text
    GROQ_MODEL=<Add the model name, e.g. llama-3.3-70b-versatile>
    GROQ_API_KEY=<Add your groq api key here>
    ```

1. Run the streamlit app by running the following command.

    ```bash
    streamlit run app.py
    ```
