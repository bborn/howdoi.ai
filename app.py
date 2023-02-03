from langchain.cache import InMemoryCache
import langchain
from flask import Flask, send_from_directory, request, render_template
import sys
from langchain.chains import LLMChain
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.prompts import FewShotPromptTemplate
from langchain import OpenAI, PromptTemplate

from utils.chat_agent import ChatAgent
import logging
import json
import re

import os
from supabase import create_client, Client
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


langchain.llm_cache = InMemoryCache()


logger = logging.getLogger()

app = Flask(__name__, template_folder='vite/dist')
app.config.from_object(__name__)
if __name__ == '__main__':
    app.run(debug=True)


@app.route('/write')
def root():
    return send_from_directory('vite/dist', 'write.html')


@app.route('/')
@app.route('/chat/<id>')
def howdoi(id=None):
    # return send_from_directory('./vite/dist', 'howdoi.html')
    if id is None:
        return render_template('howdoi.html')
    else:
        data = supabase.table("chats").select('*').eq('id', id).execute()
        return render_template('howdoi.html', history=data.data[0])


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


@app.route('/save', methods=['POST', 'GET'])
def save():
    json = request.get_json(force=True)
    chat_history = json.get('history')
    data = supabase.table("chats").insert(
        {"chat_history": chat_history}).execute()
    return data.data[0]


@app.route('/chat/<id>.json', methods=['GET'])
def load_chat(id):
    data = supabase.table("chats").select('*').eq('id', id).execute()

    return data.data[0]


@ app.route('/chat', methods=['POST', 'GET'])
def chat():
    json = request.get_json(force=True)
    history_array = json.get('history')

    input = json.get('prompt')
    print("\n\n#### INPUT ####\n")
    print(input)
    print("\n\n#### INPUT ####\n")

    chat_agent = ChatAgent(history_array=history_array)

    try:
        reply = chat_agent.agent_executor.run(input=input)

    except ValueError as inst:
        print('ValueError:\n')
        print(inst)
        reply = "Sorry, there was an error processing your request."

    print("\n\n#### REPLY ####\n")
    print(reply)
    print("\n\n#### REPLY ####\n")

    pattern = r'\(([a-z]{2}-[A-Z]{2})\)'
    # Search for the local pattern in the string
    match = re.search(pattern, reply)

    language = 'en-US'  # defaut
    if match:
        # Get the language code
        language = match.group(1)

        # Remove the language code from the reply
        reply = re.sub(pattern, '', reply)

    print("LANG: ", language)

    sys.stdout.flush()
    return {
        'input': input,
        'text': reply.strip(),
        'language': language
    }
