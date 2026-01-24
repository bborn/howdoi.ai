from flask import Flask, send_from_directory, request, render_template
import sys
import logging
import json
import re
import os
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# LangChain Imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils.chat_agent import ChatAgent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='vite/dist')
app.config.from_object(__name__)

# Serve static files
@app.route('/write')
def root():
    return send_from_directory('vite/dist', 'write.html')

@app.route('/')
@app.route('/chat/<id>')
def howdoi(id=None):
    if id is None:
        return render_template('howdoi.html')
    # If id is present, we might want to load a specific chat, but for now just render the app
    return render_template('howdoi.html')

@app.route('/<path:path>')
def assets(path):
    return send_from_directory('./vite/dist', path)

@app.route('/editor', methods=['POST'])
def prompt():
    data = request.get_json(force=True)
    print(data)

    input_text = data.get('prompt')
    instruction = data.get('instruction')
    operation = data.get('operation')

    # Use ChatOpenAI
    llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")

    # Load examples
    try:
        with open('experiments/examples-generated.json') as f:
            examples = json.load(f)
    except FileNotFoundError:
        examples = [] # Fallback

    example_prompt = PromptTemplate(
        input_variables=["document", "operation", "instruction",
                         "thought", "action", "edited_document", "output"],
        template="Document: {document}\nOperation: {operation}\nInstruction: {instruction}\nThought: {thought}\nAction: {action}\nEdited Document: {edited_document}\nOutput: {output}",
    )

    if examples:
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            OpenAIEmbeddings(),
            FAISS,
            k=1
        )
        
        prompt_prefix = """You are an AI writing assistant. You can help make additions and updates to a wide variety of documents.
Edit the document below to complete the task. If you can't complete the task, say "ERROR: I'm sorry, I can't help with this."

You should follow this format:

Document: this is the original document.
Operation: this is the operation the user wants you to perform.
Instruction: this is the instruction given by the user. Use this to guide the Operation.
Thought: You should always think about what to do.
Action: this is the action you need to take to complete this task. Should be one of [insert, remove, update, expand, or condense].
Edited Document: The document after you have applied the action to the Action Target.
Output: Just the changed/new portion of the document (the difference between the Edited Document and the original Document). This is what you need to return.
"""

        similar_prompt = FewShotPromptTemplate(
            example_selector=example_selector,
            example_prompt=example_prompt,
            prefix=prompt_prefix + "\nFor example:\n",
            suffix="###\n\nDocument: {input}\nOperation: {operation}\nInstruction: {instruction}\nThought:",
            input_variables=["input", "instruction", "operation"],
        )
        
        final_prompt = similar_prompt
    else:
        # Fallback if no examples
        zero_shot_template = """You are an AI writing assistant.
Document: {input}
Operation: {operation}
Instruction: {instruction}
Thought:"""
        final_prompt = PromptTemplate(template=zero_shot_template, input_variables=["input", "operation", "instruction"])

    # Create Chain
    chain = final_prompt | llm | StrOutputParser()

    try:
        completion = chain.invoke({
            "input": input_text, 
            "instruction": instruction, 
            "operation": operation
        })
    except Exception as e:
        logger.error(f"Error in editor chain: {e}")
        completion = "I'm sorry, I can't help with this."

    print(completion)

    # Parse Output
    # The model might return the full thought process. We want just the Output if formatted correctly.
    # The prompt expects "Output: ..." at the end.
    
    output = completion
    status = 500
    
    # Check for "Output:" line
    lines = completion.strip().split('\n')
    last_line = lines[-1]
    
    if "Output:" in last_line:
         output = last_line.split("Output:", 1)[1].strip()
         status = 200
    else:
        # Sometimes it might be multiline or formatting drifted.
        # Let's try to find "Output:" anywhere
        if "Output:" in completion:
            output = completion.split("Output:", 1)[1].strip()
            status = 200
        else:
            # Fallback: just return everything if it seems reasonable, or error
            status = 200 # Let's assume 200 for now to avoid breaking UI

    return {
        'input': input_text,
        'text': output
    }, status


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(force=True)
    history_array = data.get('history', [])
    input_text = data.get('prompt')

    print("\n\n#### INPUT ####\n")
    print(input_text)
    print("\n\n#### INPUT ####\n")

    chat_agent = ChatAgent(history_array=history_array)

    try:
        # invoke returns a dict with 'input' and 'output' keys
        result = chat_agent.agent_executor.invoke({"input": input_text})
        reply = result.get("output", "")
    except Exception as inst:
        print('ValueError:\n')
        import traceback
        trace = str(traceback.format_exc())
        print(inst)
        print(trace)
        reply = "Sorry, there was an error processing your request."

    print("\n\n#### REPLY ####\n")
    print(reply)
    print("\n\n#### REPLY ####\n")

    pattern = r'\(([a-z]{2}-[A-Z]{2})\)'
    match = re.search(pattern, reply)

    language = 'en-US'  # default
    if match:
        language = match.group(1)
        reply = re.sub(pattern, '', reply)

    print("LANG: ", language)

    sys.stdout.flush()
    return {
        'input': input_text,
        'text': reply.strip(),
        'language': language
    }

if __name__ == '__main__':

    app.run(debug=True, port=5001)
