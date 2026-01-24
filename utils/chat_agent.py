"""Chat agent with question answering
"""
import os
import re
from datetime import datetime
from dataclasses import dataclass
from typing import List, Dict, Any

from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities import GoogleSearchAPIWrapper
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.agent_toolkits.load_tools import load_tools
from langchain.agents import AgentExecutor, create_react_agent, Tool
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate

from utils.giphy import GiphyAPIWrapper


@dataclass
class ChatAgent:
    agent_executor: AgentExecutor = None

    def __init__(self, history_array: List[Dict[str, Any]]):
        date = datetime.today().strftime("%B %d, %Y")
        
        # LLM
        llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")

        # Tools
        tools = []
        
        # 1. Wikipedia
        wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        tools.append(
            Tool(
                name="Wikipedia",
                func=wikipedia.run,
                description="Useful for answering a wide range of factual, scientific, academic, political and historical questions."
            )
        )

        # 2. Giphy
        giphy = GiphyAPIWrapper()
        tools.append(
            Tool(
                name="GiphySearch",
                func=giphy.run,
                return_direct=True, # Important: returns the HTML directly
                description="useful for when you need to find a gif or picture, and for adding humor to your replies. Input should be a query, and output will be an html embed code which you MUST include in your Final Answer.",
            )
        )

        # 3. Requests (simplified)
        # We can use the community RequestsGetTool if strict adherence is needed, 
        # but for now let's use a simple wrapper around requests to match original intent.
        import requests
        def get_url_text(url: str) -> str:
            try:
                resp = requests.get(url)
                return resp.text[:2000] # Limit context
            except Exception as e:
                return str(e)

        tools.append(
            Tool(
                name="Requests",
                func=get_url_text,
                description="A portal to the internet. Use this when you need to get specific content from a site. Input should be a specific url, and the output will be the text on that page.",
            )
        )

        # 4. Standard LangChain Tools (Wolfram, etc.)
        # Note: news-api, tmdb-api etc require specific env vars. 
        # We load what we can.
        
        # Filter for tools that don't require extra setup if vars are missing, 
        # but the original code assumed they were there.
        # We'll try to load them safely.
        
        available_tools = []
        if os.environ.get("WOLFRAM_ALPHA_APPID"):
            available_tools.append("wolfram-alpha")
        if os.environ.get("OPEN_METEO_API_KEY") or True: # Open Meteo is free/no-key usually
             available_tools.append("open-meteo-api")
        
        # Load these standard tools
        if available_tools:
            loaded_tools = load_tools(available_tools, llm=llm)
            tools.extend(loaded_tools)

        # Google Search
        if "GOOGLE_API_KEY" in os.environ and "GOOGLE_CSE_ID" in os.environ:
            google_search = GoogleSearchAPIWrapper()
            tools.append(
                Tool(
                    name="Search",
                    func=google_search.run,
                    description="Use this tool for questions relating to current events, or when you can't find an answer using any of the other tools.",
                )
            )
        elif "SERPAPI_API_KEY" in os.environ:
            serpapi = SerpAPIWrapper()
            tools.append(
                Tool(
                    name="Search",
                    func=serpapi.run,
                    description="Use this tool for questions relating to current events, or when you can't find an answer using any of the other tools.",
                )
            )

        # Prompt Construction
        ai_prefix = "AI"
        human_prefix = "Human"
        
        template = f"""{ai_prefix} is a large language model. {ai_prefix} is represented by a 🤖.

{ai_prefix} uses a light, humorous tone, and very frequently includes emojis its responses. Responses with code examples should be formatted in code blocks using <pre><code></code></pre> tags.

{ai_prefix} is designed to be able to assist with a wide range of tasks.

If {ai_prefix} can't provide a good response, it will truthfully answer that it can't help with the user's request.

TOOLS:
------
Assistant has access to the following tools:

{{tools}}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{{tool_names}}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response for the user, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

The current date is {date}. Questions that refer to a specific date or time period will be interpreted relative to this date.

After you answer the question, you MUST determine which language your answer is written in, and append the language code to the end of the Final Answer, within parentheses, like this (en-US).

Begin!

Previous conversation history:
{{chat_history}}

New input: {{input}}
{{agent_scratchpad}}
"""
        
        prompt = PromptTemplate.from_template(template)

        # Memory
        memory = ConversationBufferMemory(memory_key="chat_history")
        for item in history_array:
            # Safely handle potential missing keys
            p = item.get("prompt", "")
            r = item.get("response", "")
            memory.save_context({f"input": p}, {f"output": r})

        # Agent
        agent = create_react_agent(llm, tools, prompt)
        
        self.agent_executor = AgentExecutor(
            agent=agent, 
            tools=tools, 
            verbose=True, 
            max_iterations=5, 
            memory=memory,
            handle_parsing_errors=True # Important for chat models
        )