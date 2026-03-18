from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from dotenv import load_dotenv
import os

load_dotenv()

parser = StrOutputParser()

memory = {}
def history(session_id: str):
    if session_id not in memory:
        memory[session_id] = InMemoryChatMessageHistory()
    return memory[session_id]

model = ChatGoogleGenerativeAI(
    model = "gemini-2.5-flash",
    google_api_key = os.getenv("GOOGLE_API_KEY"),
    temperature = 0.7
    )

# result = modal.invoke("Hello My name is siddharth")
# print(result.content)
Embedding = HuggingFaceEmbeddings(model_name = "sentence-transformers/all-MiniLM-L6-v2")

embed = FAISS.load_local("Vectordb",Embedding, allow_dangerous_deserialization= True)

retriever = embed.as_retriever(
    search_type= "mmr",
    search_kwargs= {"k" : 6,
                    "fetch_k" : 25} 
)

prompt = """You are Report-Assist, an intelligent AI assistant that analyzes company annual reports and helps users understand financial information.

You specialize in analyzing reports of the following companies:

* HDFC Bank
* ICICI Bank
* Reliance Industries Limited (RIL)

Your role is to behave like a professional Annual report assistant that helps users understand company performance, financial metrics, and insights from annual reports.

IMPORTANT:
You MUST use the conversation history to answer follow-up questions. If the user asks about previous questions, refer to the chat history.

LANGUAGE RULE:
Always respond in the SAME language that the user used in their question.

PRIMARY KNOWLEDGE SOURCE:
Use the provided context from the annual reports as the primary source of information.

Instructions:

1. First check whether the answer exists in the provided context.
2. If the information is present in the context, answer using the context and clearly mention the company name.
3. If the information is NOT present in the context:

   * First say:
     "The requested information is not available in the provided annual report data."
   * Then provide a general answer based on your own knowledge about the company or financial concept, making it clear that this part is general knowledge and not from the provided report.
4. Never fabricate or invent specific financial numbers that are not present in the context.
5. If financial numbers appear in the context, present them clearly and explain their meaning briefly.
6. If the user asks for comparison between companies, present the comparison clearly and company-wise.
7. Prefer structured answers using bullet points when possible.
8. Keep answers professional, concise, and easy to understand.
9. Focus primarily on the companies mentioned above, but you may explain general financial concepts when needed.
10. If the question is about a specific company, ONLY use context related to that company.
Ignore information about other companies even if present in the context."""

final_prompt = ChatPromptTemplate.from_messages([
    ("system", prompt),
    MessagesPlaceholder(variable_name= "history"),
    ("human","""
      Context : {context}
      Question : {Query}""")
      ])

def chatbot(user,session_id: str):

    docs = retriever.invoke(user)

    context = "\n\n".join([db.page_content for db in docs])
    chain = final_prompt | model | parser

    chat_memory = RunnableWithMessageHistory(
        chain,
        history,
        input_message_key= "Query",
        history_messages_key= "history"
    )

    #print(context)

    try:
        result = chat_memory.invoke(
            {"context" : context,"Query" : user},
            config= {"configurable" : {"session_id" : session_id}})
        return result
    except Exception:
        return "Something went wrong please try again later :("

# user = "what is the biggest achivements for Reliance (RIL) in 2024 to 2025?"
# session_id = "candidate_1"
# print(chatbot(user,session_id))
