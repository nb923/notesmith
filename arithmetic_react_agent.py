import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph
from langgraph.graph import MessagesState
from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import tools_condition, ToolNode

load_dotenv()

class OverallState(MessagesState):
    pass

def add(a: int, b: int) -> int:
    """Add a and b

    Args:
        a: first int
        b: second int
    """
    return a + b

def subtract(a: int, b: int) -> int:
    """Subtract b from a, so (a - b)

    Args:
        a: first int
        b: second int
    """
    return a - b

def multiply(a: int, b: int) -> int:
    """Multiply a and b

    Args:
        a: first int
        b: second int
    """
    return a * b

def divide(a: int, b: int) -> int:
    """Divide a by b

    Args:
        a: first int
        b: second int
    """
    return a / b

tools = [add, subtract, multiply, divide]
llm = ChatOpenAI(model="gpt-3.5-turbo")
llm_with_tools = llm.bind_tools(tools)

sys_message = SystemMessage(content="You are an assistant that is tasked with performing basic four function math calculations. Take the expression given to you and find the smallest expression that you can calculate with the given numbers. Calculate that expression ONLY then get the value, then try to find the next smallest expression you can calculate and repeat. Do not perform multiple tool calls before getting responses for preceeding ones, one tool call at a time and get a response from a tool call before issuing another one.")

def model_node(state: MessagesState):
    return {"messages": [llm_with_tools.invoke([sys_message] + state["messages"])]}

builder = StateGraph(OverallState)

builder.add_node("model", model_node)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)

builder.add_edge("tools", "model")

graph = builder.compile()
