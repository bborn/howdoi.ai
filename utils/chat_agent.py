"""Chat agent with question answering

"""
import os
from utils.giphy import GiphyAPIWrapper
from dataclasses import dataclass

from langchain.chains import LLMChain
from langchain import Wikipedia, OpenAI
from langchain.agents.react.base import DocstoreExplorer
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor, get_all_tool_names, load_tools, initialize_agent

import langchain
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()


news_api_key = os.environ["NEWS_API_KEY"]
tmdb_bearer_token = os.environ["TMDB_API_KEY"]


@dataclass
class ChatAgent:
    agent_executor: AgentExecutor = None

    def _get_docstore_agent(self):
        docstore = DocstoreExplorer(Wikipedia())
        docstore_tools = [
            Tool(
                name="Search",
                func=docstore.search
            ),
            Tool(
                name="Lookup",
                func=docstore.lookup
            )
        ]
        docstore_llm = OpenAI(temperature=0, model_name="text-davinci-003")
        docstore_agent = initialize_agent(
            docstore_tools, docstore_llm, agent="react-docstore", verbose=True)
        return docstore_agent

    def __init__(self, *, conversation_chain: LLMChain = None):
        # set up a Wikipedia docstore agent
        docstore_agent = self._get_docstore_agent()

        giphy = GiphyAPIWrapper()

        tool_names = get_all_tool_names()

        tool_names.remove("pal-math")

        tools = load_tools(tool_names,
                           llm=OpenAI(temperature=0, model="text-davinci-003"),
                           news_api_key=news_api_key,
                           tmdb_bearer_token=tmdb_bearer_token)

        # Tweak some of the tool descriptions
        for tool in tools:
            if tool.name == "Search":
                tool.description = "Use this tool exclusively for questions relating to current events, or when you can't find an answer using any of the other tools."
            if tool.name == "Calculator":
                tool.description = "Use this to solve numeric math questions and do arithmetic. Don't use it for general or abstract math questions."

        # wrapper for when the conversation chain is used within an agent
        def conversation_chain_wrapper(input):
            out = conversation_chain.run(input)
            return "\nFinal Answer: " + out.strip()

        tools = tools + [
            Tool(
                name="WikipediaSearch",
                description="Useful for answering a wide range of factual, scientific, academic, political and historical questions.",
                func=docstore_agent.run
            ),
            Tool(
                name="Conversation",
                func=conversation_chain_wrapper,
                description="Useful for answering a wide range of questions, conversing with a human, writing text and code. Don't use it for questions relating to events after April 1, 2021. Input should be a complete sentence."
            ),
            Tool(
                name="GiphySearch",
                func=giphy.run,
                description="useful for when you need to find a gif or picture, and for randomly replying to a human"
            )
        ]

        prefix = """
The current date is {date}. Questions that refer to a specific date or time period will be interpreted relative to this date.
Answer the following questions as best you can. You have access to the following tools (N=3): """
        suffix = """
Conversation History:
{history}

Begin!

Question: {input}
{agent_scratchpad}"""

        prompt = ZeroShotAgent.create_prompt(
            tools,
            prefix=prefix,
            suffix=suffix,
            input_variables=["input", "agent_scratchpad", "date", "history"]
        )

        llm_chain = LLMChain(llm=OpenAI(temperature=.5, model="text-davinci-003"),
                             prompt=prompt, verbose=True)

        agent = ZeroShotAgent(llm_chain=llm_chain, tools=tools,
                              verbose=True)

        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True)
