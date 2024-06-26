import os
import streamlit as st
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_groq import ChatGroq
from langchain_community.tools import DuckDuckGoSearchRun
# Page configuration
st.set_page_config(page_title="Research Assistant", page_icon=":mag:", layout="wide")

# Accessing the environment variables
LANGCHAIN_API_KEY = st.secrets["LANGCHAIN_API_KEY"]
GROQ_API_KEY = st.secrets["GROQ_API_KEY"]

# Define the prompt template
generate_web_search_prompt_template = ChatPromptTemplate.from_messages([
    ("system",
     "You are a web search query generating AI assistant. Read and understand the text in {user_query}, then based on the key words in {user_query} generate one best web search query. The generated query must be in string format and without any quotes or extra characters, just the query itself and no extra messages or text"),
    ("user", "{user_query}")
])

# Initialize the LLM
llm = ChatGroq(model_name="llama3-8b-8192")

# Define the chain with the template, LLM, and output parser
generate_web_search_queries_chain = generate_web_search_prompt_template | llm | StrOutputParser()

# Initialize DuckDuckGo search instance
ddg_search_instance = DuckDuckGoSearchRun()

# Define the book recommendation prompt template
book_recommendation_prompt_template = ChatPromptTemplate.from_messages([
    ("system",
     "You are a Book Recommendation providing AI assistant. Read and understand text in {context},then based on {context} generate list of 10 best books published. This books must be published before 2022,please make sure the books you recommend are books published in real and not made up books name or hallucinated names by you. With this list generated create a table with columns book_title, about; book_title containing name/title of book  and about containing brief description about book along with author name, then after providing/generating the table, also generate a message which book do you like the most, also tell them like from where to read like amazon/kindle/Z-library/etc sites and also provide clickable links amazon/kindle with all ten books name, please make sure links are not made up or hallucinated"),
    ("user", "{context}")
])


# Function to get book recommendations
def get_book_recommendations(user_query):

    # Define context for LLM chain
    context_for_llm_chain = generate_web_search_queries_chain | DuckDuckGoSearchRun() | llm | StrOutputParser()
    context = context_for_llm_chain.invoke({"user_query": user_query})

    # Get book recommendations
    br_chain = book_recommendation_prompt_template | llm | StrOutputParser()
    br_chain_output = br_chain.invoke({"context": context})

    return br_chain_output


st.title("Book Recommendation Agent")

# Initialize chat session
if "chat_session" not in st.session_state:
    st.session_state.chat_session = []

agent_message = "Hello, please share your thoughts or ideas so I can process it and recommend you the best books based on your interest."
if not any(message['role'] == 'agent' for message in st.session_state.chat_session):
    st.session_state.chat_session.append({
        'role': 'agent',
        'text': agent_message
    })

for message in st.session_state.chat_session:
    with st.chat_message(message['role']):
        st.markdown(message['text'], unsafe_allow_html=True)

user_query = st.chat_input("Your idea/thought:")

if user_query:
    st.session_state.chat_session.append({
        'role': 'user',
        'text': user_query
    })

    st.chat_message('user').markdown(user_query)

    with st.spinner('Generating personalized recommendations...'):
        recommendation = get_book_recommendations(user_query)

    st.session_state.chat_session.append({
        'role': 'assistant',
        'text': recommendation
    })
    st.chat_message('assistant').markdown(recommendation)


# Footer in the sidebar
st.sidebar.markdown("---")

# Create an expander for the "Developed by" section in the sidebar
with st.sidebar.expander("Developed by"):
    st.markdown("**Abhishek Vidhate**")
    st.markdown(
        "[LinkedIn](https://www.linkedin.com/in/abhishek-vidhate-21smdb/) | [GitHub](https://github.com/Abhishekvidhate)")

    # Include the atom image inside the expander
    st.markdown('<div class="illustration" style="text-align: center;">'
                '<img src="https://clipground.com/images/atom-clipart-6.jpg" alt="Atom" width="50"></div>',
                unsafe_allow_html=True)
