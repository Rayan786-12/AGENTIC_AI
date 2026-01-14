from typing import Annotated
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langgraph.graph import END,START
from langgraph.graph.state import StateGraph
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
import os
from dotenv import load_dotenv
load_dotenv()
langsmith="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"
os.environ['LANGSMITH_API_KEY']=langsmith
os.environ['LANGSMITH_TRACING']="true"
# os.environ['OPENAI_API_KEY']=os.getenv("API_KEY")
os.environ['LANGSMITH_API_KEY']=os.getenv("langsmith")
os.environ['LANGSMITH_TRACING']="true"
API_KEY = "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"
os.environ["LANGSMITH_PROJECT"]="TestProject"
model_name = "nex-agi/deepseek-v3.1-nex-n1:free"
base_url = "https://openrouter.ai/api/v1"
llm=ChatOpenAI(api_key=API_KEY,model_name=model_name,temperature=0.7,base_url=base_url)

class State(TypedDict):
    messages:Annotated[list[BaseMessage],add_messages]

def make_tool_graph():
    from langchain_core.tools  import tool
    @tool
    def add(a:float,b:float):
        """Add two numbers"""
        return a+b

    tools=[add]

    tool_node=ToolNode([add])
    llm_with_tools = llm.bind_tools([add])


    def tool_calling_llm(state:State):
        return {"messages":[llm_with_tools.invoke(state['messages'])]}
    
    builder  =  StateGraph(State)
    builder.add_node("tool_calling_llm",tool_calling_llm)
    builder.add_node("tools",ToolNode(tools))

    builder.add_edge(START,"tool_calling_llm")
    builder.add_conditional_edges(
        "tool_calling_llm",

        tools_condition


    )
    builder.add_edge("tools","tool_calling_llm")

    graph=builder.compile()
    return graph
    # from IPython.display import Image, display
    # display(Image(graph.get_graph().draw_mermaid_png()))

tool_agent = make_tool_graph()
