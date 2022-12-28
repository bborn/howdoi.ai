from langchain.input import print_text
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.prompts import load_prompt, FewShotPromptTemplate
from langchain import LLMMathChain, SerpAPIWrapper, Wikipedia, OpenAI, PromptTemplate
from langchain.agents.react.base import DocstoreExplorer
from langchain.agents import ZeroShotAgent, Tool, AgentExecutor, get_all_tool_names, load_tools, initialize_agent
import logging
import json
from utils.giphy import GiphyAPIWrapper
import os
import sys
from flask import Flask, render_template, jsonify, send_from_directory, request
from datetime import datetime
import langchain
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()


logger = logging.getLogger()

news_api_key = os.environ["NEWS_API_KEY"]
tmdb_bearer_token = os.environ["TMDB_API_KEY"]


app = Flask(__name__)
app.config.from_object(__name__)
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/write')
def root():
    return send_from_directory('./vite/dist', 'write.html')


@app.route('/')
@app.route('/chat')
def howdoi():
    return send_from_directory('./vite/dist', 'howdoi.html')


# Path for the rest of the static files (JS/CSS)
@app.route('/<path:path>')
def assets(path):
    return send_from_directory('./vite/dist', path)


@app.route('/editor', methods=['POST', 'GET'])
def prompt():
    prompt = request.get_json(force=True)

    # print the prompt to the console
    print(prompt)

    input = prompt.get('prompt')
    instruction = prompt.get('instruction')
    operation = prompt.get('operation')

    llm = OpenAI(temperature=.5)

    f = open('experiments/examples-generated.json')
    examples = json.load(f)

    example_prompt = PromptTemplate(
        input_variables=["document", "operation", "instruction",
                         "thought", "action", "edited_document", "output"],
        template="Document: {document}\nOperation: {operation}\nInstruction: {instruction}\nThought: {thought}\nAction: {action}\nEdited Document: {edited_document}\nOutput: {output}",
    )

    example_selector = SemanticSimilarityExampleSelector.from_examples(
        examples,
        OpenAIEmbeddings(),
        FAISS,
        k=1
    )

    prompt_prefix = """
You are an AI writing assistant. You can help make additions and updates to a wide variety of documents. 
Edit the document below to complete the task. If you can't complete the task, say "ERROR: I'm sorry, I can't help with this."

You should follow this format:

Document: this is the original document.
Operation: this is the operation the user wants you to perform.
Instruction: this is the instruction given by the user. Use this to guide the Operation.\
Thought: You should always think about what to do.
Action: this is the action you need to take to complete this task. Should be one of [insert, remove, update, expand, or condense]. 
Edited Document: The document after you have applied the action to the Action Target.
Output: Just the changed/new portion of the document (the difference between the Edited Document and the original Document). This is what you need to return.
"""

    similar_prompt = FewShotPromptTemplate(
        # We provide an ExampleSelector instead of examples.
        example_selector=example_selector,
        example_prompt=example_prompt,
        prefix=prompt_prefix + "\nFor example:\n",
        suffix="###\n\nDocument: {input}\nOperation: {operation}\nInstruction: {instruction}\nThought:",
        input_variables=["input", "instruction", "operation"],
    )

    zero_shot_template = prompt_prefix + """
###
Document: {input}
Operation: {operation}
Instruction: {instruction}
Thought: 
    """

    zero_shot_prompt = PromptTemplate(
        template=zero_shot_template,
        input_variables=["input", "instruction", "operation"],
    )

    chain = LLMChain(llm=llm, prompt=similar_prompt, verbose=True)
    # chain = LLMChain(llm=llm, prompt=zero_shot_prompt, verbose=True)

    # add a try except block to catch errors
    try:
        completion = chain.predict(
            input=input, instruction=instruction, operation=operation)
    except:
        completion = "I'm sorry, I can't help with this."

    # # import betterprompt
    # # perplexity = betterprompt.calculate_perplexity(similar_prompt.format(
    # #     input=input, instruction=instruction, operation=operation))

    # print("\nPerplexity: ", 'blue')
    # print(perplexity, 'blue')
    # print('\n', 'blue')

    print(completion)

    # check if the  last line of completion starts with Output:
    if completion.split('\n')[-1].startswith("Output:"):
        # if so, remove the Output: prefix
        output = completion.split("Output:")[1].strip()
        status = 200
    else:
        # otherwise, return the completion as is
        output = completion
        status = 500

    return {
        'input': input,
        'text': output
    }, status


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    date = datetime.today().strftime('%B %d, %Y')
    json = request.get_json(force=True)
    history_array = json.get('history')
    history = ""
    for p in history_array:
        history += "\nHuman: " + p['prompt'] + "\nAssistant: " + p['response']

    input = json.get('prompt')

    conversation_template = f"""Assistant is a large language model. Assistant is represented by a 🤖.

Assistant uses a light, humorous tone, and Assistant frequently includes emojis its responses. Responses with code examples should be formatted in code blocks using <pre><code></code></pre> tags.

Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.

Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.

If Assistant can't provide a good response, it will truthfully answer that it can't help with the user's request.

Overall, Assistant is a powerful tool that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

The current date is {date}. Questions that refer to a specific date or time period will be interpreted relative to this date.

Conversation History: {history}
Question: {{input}}
Final Answer: """

    conversation_prompt = PromptTemplate(
        input_variables=["input"],
        template=conversation_template
    )

    conversation_chain = LLMChain(
        llm=OpenAI(temperature=0.5, model="text-davinci-003"),
        prompt=conversation_prompt,
        verbose=True,
    )

    # wrapper for when the conversation chain is used within an agent
    def conversation_chain_wrapper(input):
        out = conversation_chain.run(input)
        return "Final Answer: {}".format(out.strip())

    decision_template = """You are an AI. Given an input from a human, it is your job determine whether the input is a question, a request, a greeting, or a statement, or a math problem.
Human: {human_input}
AI: This input is a """

    decision_prompt = PromptTemplate(
        input_variables=["human_input"], template=decision_template)

    print("\n####\n")
    print("\nDecision Prompt:\n")
    print(decision_prompt.format(human_input=json.get('prompt')))

    decision_chain = LLMChain(
        llm=OpenAI(temperature=.5, model="text-davinci-003"),
        prompt=decision_prompt)

    input_type = decision_chain.predict(
        human_input=json.get('prompt')
    )

    print(input_type)
    print("\n####\n")

    reply = ""
    if (input_type == " statement." or input_type == " greeting."):
        print("\nChat GPT Conversation\n")
        print("\n####\n")

        reply = conversation_chain.predict(input=input).strip()
    else:

        # set up a Wikipedia docstore agent
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

        tools = tools + [
            Tool(
                name="WikipediaSearch",
                description="Useful for answering a wide range of factual, scientific, academic, political and historical questions.",
                func=docstore_agent.run
            ),
            Tool(
                name="Conversation",
                func=conversation_chain_wrapper,
                description="Useful for answering a wide range of questions, conversing with a human, responding to a greeting or statement, generating text and code. Don't use it for questions relating to events after April 1, 2021"
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

        agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent, tools=tools, verbose=True)

        try:
            reply = agent_executor.run(input=input, history=history, date=date)
        except ValueError as inst:
            print('ValueError:\n')
            raise Exception(inst)
            print(inst)
            print("\n\Chat GPT Fallback\n")
            print("\n\n####\n")
            reply = conversation_chain.predict(input=input)

    print("\n\n#### REPLY ####\n")
    print(reply)
    print("\n\n#### REPLY ####\n")

    sys.stdout.flush()
    return {
        'input': input,
        'text': reply
    }
