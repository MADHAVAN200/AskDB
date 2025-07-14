import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.agents.agent_types import AgentType

# Load environment variables from .env
load_dotenv()

def initialize_llm(api_key=None):
    """Initializes and returns the ChatGroq LLM using .env or provided API key."""
    api_key = api_key or os.getenv("GROQ_API_KEY")

    if not api_key:
        raise ValueError("Groq API key is missing. Please check your .env file.")

    return ChatGroq(
        groq_api_key=api_key,
        model_name="Llama3-8b-8192",
        streaming=True,
        temperature=0.2
    )

def create_sql_query_agent(llm, db):
    """Creates and returns the LangChain SQL agent."""
    toolkit = SQLDatabaseToolkit(db=db, llm=llm)
    agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION
    )
    return agent
