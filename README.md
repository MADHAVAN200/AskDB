# AskDB: AI-Powered Database Querying

##  Project Overview

**AskDB** is a Gen-AI-powered solution that allows business users and decision-makers to query **MySQL databases using natural language**, removing the need for SQL expertise. In many production environments, key decisions rely on outdated reports or manual queries—AskDB eliminates this bottleneck by enabling real-time insights through a conversational interface.

The system converts user questions into SQL, executes them on a live MySQL database, and returns the results in a clear, readable tabular format. It is built using Streamlit and LangChain, and powered by Groq's ultra-fast inference of LLaMA 3.

---

## Features

- **Natural Language to SQL**  
  Converts user-friendly questions into executable SQL statements automatically.

- **Real-Time Data Retrieval**  
  Executes the generated SQL on your connected MySQL database and fetches live results.

- **MySQL-Only Support**  
  Currently supports **only MySQL** connections. (No SQLite or PostgreSQL support in this version.)

- **Interactive Chat Interface**  
  Easy-to-use Streamlit-based chat with AI and user avatars for a conversational experience.

- **No Visualizations**  
  As of now, the app **only supports querying** and displays results in table form. Visualizations like charts and graphs are planned for future versions.

- **Clear Error Feedback**  
  Gracefully handles bad input, connection failures, or malformed queries.

---

## Technologies Used

- **Python 3.x**
- **Streamlit** – Chat-based UI
- **LangChain** – LLM agent and SQL generation framework
- **Groq** – For ultra-fast LLaMA 3 inference
- **SQLAlchemy** – ORM and SQL abstraction
- **mysql-connector-python** – MySQL DB connectivity
- **Pandas** – Tabular output display



---

## Setup Instructions
### 1. Clone the Repository

```bash
git clone https://github.com/MADHAVAN200/AskDB.git
cd AskDB

