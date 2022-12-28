from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotPromptTemplate
from langchain import OpenAI, PromptTemplate

from utils.chat_agent import ChatAgent
import logging
import json

import sys
from flask import Flask, send_from_directory, request
from datetime import datetime

import langchain
from langchain.cache import InMemoryCache
langchain.llm_cache = InMemoryCache()


logger = logging.getLogger()

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

        chat_agent = ChatAgent(conversation_chain=conversation_chain)

        try:
            reply = chat_agent.agent_executor.run(
                input=input, history=history, date=date)
        except ValueError as inst:
            print('ValueError:\n')
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
        'text': reply.strip()
    }
