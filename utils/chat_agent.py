"""Chat agent with question answering

"""
import os
from utils.giphy import GiphyAPIWrapper
from dataclasses import dataclass

from langchain.chains import LLMChain, LLMRequestsChain
from langchain import Wikipedia, OpenAI
from langchain.agents.react.base import DocstoreExplorer
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor, get_all_tool_names, load_tools, initialize_agent
from langchain.prompts import PromptTemplate


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

    def _get_requests_llm_tool(self):

        template = """
        Extracted: {requests_result}"""

        PROMPT = PromptTemplate(
            input_variables=["requests_result"],
            template=template,
        )

        def lambda_func(input):
            out = chain = LLMRequestsChain(llm_chain=LLMChain(
                llm=OpenAI(temperature=0),
                prompt=PROMPT)).run(input)
            return out.strip()
        return lambda_func

    def __init__(self, *, conversation_chain: LLMChain = None):
        # set up a Wikipedia docstore agent
        docstore_agent = self._get_docstore_agent()

        giphy = GiphyAPIWrapper()

        tool_names = get_all_tool_names()

        tool_names.remove("pal-math")
        tool_names.remove("requests")  # let's use the llm_requests instead
        # let's use the llm_requests instead
        tool_names.remove("google-search")
        tool_names.remove("pal-colored-objects")
        tool_names.remove("python_repl")
        tool_names.remove("terminal")

        requests_tool = self._get_requests_llm_tool()

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

        tools = tools + [
            Tool(
                name="WikipediaSearch",
                description="Useful for answering a wide range of factual, scientific, academic, political and historical questions.",
                func=docstore_agent.run
            ),
            # Tool(
            #     name="Conversation",
            #     func=conversation_chain.run,
            #     description="Useful for answering a wide range of questions, conversing with a human, brainstorming, and writing text and code. Use it to answer most questions relating to events before 2021. Input should be a complete sentence."
            # ),
            Tool(
                name="GiphySearch",
                func=giphy.run,
                description="useful for when you need to find a gif or picture, and for adding humor to your replies. Input should be a query, and output will be an html embed code which you MUST include in your Final Answer."
            ),
            Tool(
                name="Requests",
                func=requests_tool,
                description="A portal to the internet. Use this when you need to get specific content from a site. Input should be a specific url, and the output will be all the text on that page."
            )
        ]

        prefix = """
The current date is {date}. Questions that refer to a specific date or time period will be interpreted relative to this date.
Answer the following questions as best you can. 
After you answer the question, you MUST to determine which langauge your answer is written in, and append the language code to the end of the Final Answer, within parentheses, like this (en-US).
You have access to the following tools (N=3): """
        suffix = """

You do NOT need to use these tools. For most normal conversation, you will not need to, and you can just respond directly to the Human.
If an Observation contains "Final Answer:" you must return that as your response to the Human and skip other steps.

When you have a response to say to the Human, you MUST use the format:

```
Assistant: [your response here]
```

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
            agent=agent,
            tools=tools,
            max_iterations=5,
            verbose=True)
