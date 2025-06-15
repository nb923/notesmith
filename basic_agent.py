import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph import MessagesState
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")

class OverallState(MessagesState):
    pass

def node_1(state: MessagesState):
    return {"messages": [llm.invoke(state["messages"])]}

builder = StateGraph(OverallState)

builder.add_node("model", node_1)

builder.add_edge(START, "model")
builder.add_edge("model", END)

graph = builder.compile()