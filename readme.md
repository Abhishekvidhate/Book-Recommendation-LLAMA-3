# Book Recommendation AI Agent (using Langchain ecosystem,streamlit UI)

Building a LLM Chatbot Agent for Book Recommendation based on user query.

### [working link of Book Recommendation Agent Application, deployed on Streamlit cloud]()
### Video Demo 

https://github.com/Abhishekvidhate/Book-Recommendation-LLAMA-3/assets/120262589/2c9d394f-0371-4a47-a615-4800a5098ab2




Agent will prompt user to share their thoughts or ideas on which they want to gain more
knowledge i.e read more on that topic, so Agent will take ***user_query*** then LLM will process query
for later to provide ***web search queries*** based on inital user_query.

Then Agent will use WebSearch tool to search web on the web search queries LLM generated to find latest/best 
books on user query,
then use on ***web searches*** as system prompt for generating list of 10 best books with brief 
description highly
relevant/matching with user query.

***BookRecommendation Agent*** will also be context/history aware so when user will get list of ten books,
LLM will also generate a table( list of books with clickable button to select favorite books)(can be done with streamlit)
after user selected 1 or more , LLM will generate more info on books like where to buy/read online and provide relevant
links , Streamlit will create new UI for this

then LLM will again prompt/start for new chat with user 

### Tools to be used :
* Langchain -
  - langsmith (tracking/monitoring flow of LLM Agent)
  - duckduckgosearch (web search)
  - langchain_groq (LLM - llama3-8b-8192)
  - langchain tools 
  - langchain agents
  - langchain chains
  - langchain's output parsers
  - langchain.prompts (for creation of prompts)

* Streamlit -
  - streamlit libraries
  - also will use streamlit callback ( for displaying agent's actions and thoughts while process)

### References :
* [Langchain](https://github.com/langchain-ai/langchain)
* [Streamlit github](https://github.com/streamlit)
