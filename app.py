# app.py
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
import pandas as pd

# Import backend modules
from backend.db_manager import configure_database
from backend.llm_agent import initialize_llm, create_sql_query_agent


# Custom avatars
AI_AVATAR_URL = "C:\\Users\\madha\\OneDrive\\Desktop\\AskDB\\Patrick.jpg"
USER_AVATAR_URL = "C:\\Users\\madha\\OneDrive\\Desktop\\AskDB\\image.png"

st.set_page_config(page_title="Chat with our Database",layout="wide")
st.title("Chat with our Database")

MYSQL = "USE_MYSQL"

# --- Sidebar: MySQL Connection ---
st.sidebar.header("Connect with the Database to Chat")

mysql_host = st.sidebar.text_input("Provide MySQL Host")
mysql_user = st.sidebar.text_input("MYSQL User")
mysql_password = st.sidebar.text_input("MYSQL password", type="password")
mysql_db = st.sidebar.text_input("MySQL database")

connect_clicked = st.sidebar.button("Connect")

# --- Session State ---
if "connected" not in st.session_state:
    st.session_state["connected"] = False
    st.session_state["db"] = None
    st.session_state["llm"] = None
    st.session_state["agent"] = None

# --- Handle Connection ---
if connect_clicked:
    if not mysql_host or not mysql_user or not mysql_password or not mysql_db:
        st.sidebar.error("Please fill in all fields.")
    else:
        try:
            llm = initialize_llm()  # API key loaded internally from .env
            db = configure_database(MYSQL, mysql_host, mysql_user, mysql_password, mysql_db)
            agent = create_sql_query_agent(llm, db)

            st.session_state["connected"] = True
            st.session_state["db"] = db
            st.session_state["llm"] = llm
            st.session_state["agent"] = agent
            st.sidebar.success("✅ Connected to the DB")
        except Exception as e:
            st.sidebar.error(f"❌ Connection Failed: {e}")
            st.stop()

if not st.session_state["connected"]:
    st.warning("Please connect to the database to begin.")
    st.stop()

# --- Chat Interface ---
if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you query your database?"}]

for msg in st.session_state.messages:
    avatar = USER_AVATAR_URL if msg["role"] == "user" else AI_AVATAR_URL
    st.chat_message(msg["role"], avatar=avatar).write(msg["content"])

user_query = st.chat_input(placeholder="Ask anything from the database")

if user_query:
    st.session_state["messages"].append({"role": "user", "content": user_query})
    st.chat_message("user", avatar=USER_AVATAR_URL).write(user_query)

    with st.chat_message("assistant", avatar=AI_AVATAR_URL):
        streamlit_callback = StreamlitCallbackHandler(st.container())
        try:
            response = st.session_state["agent"].run(user_query, callbacks=[streamlit_callback])
            st.session_state["messages"].append({"role": "assistant", "content": response})
            
        except Exception as e:
            error_message = f"An error occurred: {e}"
            st.error(error_message)
            st.session_state["messages"].append({"role": "assistant", "content": error_message})
