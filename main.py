import os
import re
import json
import logging
from typing import List, Optional, Dict, Any
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from dotenv import load_dotenv

# LangChain Imports
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from utils.chat_agent import ChatAgent

# Load env vars
load_dotenv()

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Mount static files
# We serve the 'vite/dist' directory.
# Note: In FastAPI, order matters. We'll handle specific routes first, then static.
app.mount("/assets", StaticFiles(directory="vite/dist/assets"), name="assets")

templates = Jinja2Templates(directory="vite/dist")

# --- Pydantic Models ---

class EditorRequest(BaseModel):
    prompt: str
    instruction: Optional[str] = None
    operation: Optional[str] = None

class ChatRequest(BaseModel):
    prompt: str
    history: List[Dict[str, Any]] = []

# --- Routes ---

@app.get("/write", response_class=HTMLResponse)
async def root_write(request: Request):
    return templates.TemplateResponse("write.html", {"request": request})

@app.get("/", response_class=HTMLResponse)
@app.get("/chat/{id}", response_class=HTMLResponse)
async def root_chat(request: Request, id: Optional[str] = None):
    return templates.TemplateResponse("howdoi.html", {"request": request})

# Fallback for other static files like favicon.ico, images, etc. in root of dist
@app.get("/{file_path:path}")
async def serve_static(file_path: str):
    full_path = os.path.join("vite/dist", file_path)
    if os.path.exists(full_path) and os.path.isfile(full_path):
        return FileResponse(full_path)
    return JSONResponse(status_code=404, content={"message": "Not found"})


@app.post("/editor")
async def editor(request: EditorRequest):
    input_text = request.prompt
    instruction = request.instruction
    operation = request.operation

    print(f"Editor Request: {input_text}")

    # Use ChatOpenAI
    llm = ChatOpenAI(temperature=0.5, model="gpt-3.5-turbo")

    # Load examples
    try:
        with open('experiments/examples-generated.json') as f:
            examples = json.load(f)
    except FileNotFoundError:
        examples = []

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
        zero_shot_template = """You are an AI writing assistant.
Document: {input}
Operation: {operation}
Instruction: {instruction}
Thought:"""
        final_prompt = PromptTemplate(template=zero_shot_template, input_variables=["input", "operation", "instruction"])

    chain = final_prompt | llm | StrOutputParser()

    try:
        # invoke is sync, but we are in async def. 
        # For high load, run_in_threadpool or using async compatible methods is better.
        # But for now, standard invocation is fine for this scale.
        completion = chain.invoke({
            "input": input_text, 
            "instruction": instruction, 
            "operation": operation
        })
    except Exception as e:
        logger.error(f"Error in editor chain: {e}")
        return JSONResponse(status_code=500, content={"input": input_text, "text": "I'm sorry, I can't help with this."})

    print(completion)

    output = completion
    status = 500
    
    if "Output:" in completion:
        # Try to robustly split
        parts = completion.rsplit("Output:", 1)
        if len(parts) > 1:
            output = parts[1].strip()
            status = 200
    else:
        # Fallback
        status = 200

    return JSONResponse(status_code=status, content={
        'input': input_text,
        'text': output
    })


@app.post("/chat")
async def chat(request: ChatRequest):
    input_text = request.prompt
    history_array = request.history

    print("\n\n#### INPUT ####\n")
    print(input_text)
    print("\n\n#### INPUT ####\n")

    try:
        # ChatAgent expects a list of dicts, which matches our Pydantic model's data
        chat_agent = ChatAgent(history_array=history_array)

        # agent_executor.invoke matches the updated chat_agent.py
        result = chat_agent.agent_executor.invoke({"input": input_text})
        reply = result.get("output", "")
    except Exception as inst:
        print('ValueError:\n')
        import traceback
        trace = str(traceback.format_exc())
        print(inst)
        print(trace)
        return JSONResponse(status_code=500, content={"error": str(inst), "trace": trace})

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

    return {
        'input': input_text,
        'text': reply.strip(),
        'language': language
    }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5001)
