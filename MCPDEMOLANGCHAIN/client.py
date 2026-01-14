# from langchain_mcp_adapters.client import MCPClient
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
# from langchain.prompts import ChatPromptTemplate
# from langchain.schema import HumanMessage
apikey="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"
from langchain_openai import ChatOpenAI
model_name = "nex-agi/deepseek-v3.1-nex-n1:free"
base_url = "https://openrouter.ai/api/v1"
import os
os.environ["OPENAI_API_KEY"] = apikey
llm=ChatOpenAI(model_name=model_name,temperature=0.7,base_url=base_url)

import asyncio

async def main():
    client = MultiServerMCPClient(
        {
            "math":{
                "command":"python",
                "args":["mathservers.py"],
                "transport":"stdio"

            },
            "weather":{
                "url":"http://localhost:8000/mcp",
                "transport":"streamable_http"
            }
        }
    )
    tools = await client.get_tools()
    agent = create_react_agent(llm,tools)

    math_response = await agent.ainvoke(
        {"messages":[{"role":"user","content":"What is (2+2) * 3 ?"}]}
    )
    print("Math response",math_response['messages'][-1].content)
    weather_response = await agent.ainvoke(
        {"messages":[{"role":"user","content":"What is the weather like in New York?"}]}
    )
    print("Weather response",weather_response['messages'][-1].content)
# weather_response = await agent.ai(
#     {"messages":[
#         HumanMessage(content="What is the weather like in New York?")
#     ]}
# )
# print("Weather response",weather_response['messages'][-1].content)\
asyncio.run(main())