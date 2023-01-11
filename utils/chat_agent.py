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
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.agents.conversational.base import ConversationalAgent
from datetime import datetime


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

    def __init__(self, *, conversation_chain: LLMChain = None, history_array):
        date = datetime.today().strftime('%B %d, %Y')

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
                           llm=OpenAI(temperature=0,
                                      model_name="text-davinci-003"),
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
        ai_prefix = "AI"
        human_prefix = "Human"

        prefix = f"""{ai_prefix} is a large language model. {ai_prefix} is represented by a 🤖.

{ai_prefix} uses a light, humorous tone, and {ai_prefix} frequently includes emojis its responses. Responses with code examples should be formatted in code blocks using <pre><code></code></pre> tags.

{ai_prefix} is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, {ai_prefix} is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

If {ai_prefix} can't provide a good response, it will truthfully answer that it can't help with the user's request.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

The current date is {date}. Questions that refer to a specific date or time period will be interpreted relative to this date.

TOOLS:
------

Assistant has access to the following tools:
"""

        suffix = f"""
Questions that refer to a specific date or time period will be interpreted relative to this date.

After you answer the question, you MUST to determine which langauge your answer is written in, and append the language code to the end of the Final Answer, within parentheses, like this (en-US).

Begin!

Previous conversation history:
{{chat_history}}

New input: {{input}}
{{agent_scratchpad}}
"""

        memory = ConversationBufferMemory(memory_key="chat_history")
        for item in history_array:
            memory.save_context(
                {f"{ai_prefix}": item["prompt"]}, {f"{human_prefix}": item["response"]})

        llm = OpenAI(temperature=.5, model="text-davinci-003")
        llm_chain = LLMChain(
            llm=llm,
            prompt=ConversationalAgent.create_prompt(
                tools,
                ai_prefix=ai_prefix,
                human_prefix=human_prefix,
                suffix=suffix
            ),
        )

        agent_obj = ConversationalAgent(
            llm_chain=llm_chain, ai_prefix=ai_prefix)

        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent_obj,
            tools=tools,
            verbose=True,
            max_iterations=5,
            memory=memory)

        # self.agent_executor = AgentExecutor.from_agent_and_tools(
        #     agent=agent,
        #     tools=tools,
        #     max_iterations=5,
        #     verbose=True)
