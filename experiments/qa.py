from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain import OpenAI, VectorDBQA
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores.faiss import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.prompts import FewShotPromptTemplate

import pprint
import json
import os

f = open('examples.json')
examples = json.load(f)

f = open('examples-generated.json')
generated_examples = json.load(f)


prefix = f"""You are an editor checking a student's work. The student has made an edit to a document, and you must decide if their edit is appropriate or not.
You are given a document, the operation, instruction, and student's output and are asked to score the student's output as either APPROPRIATE or INAPPROPRIATE.
If the student's output is reasonable given the document, operation, and instruction, then the output is APPROPRIATE.

Example Format:
Document: this is the original document
Operation: this is the operation to be performed
Instruction: this is the instruction
Thought: this is the thought
Action: this is the action
Edited Document: this is the edited document
Output: student's output here
Grade: APPROPRIATE or INAPPROPRIATE here

Here are some examples of graded edits:"
"""

template = """
Begin!

Document: {document}
Operation: {operation}
Instruction: {instruction}
Thought: {thought}
Action: {action}
Edited Document: {edited_document}
Output: {output}
Grade:"""

example_prompt = PromptTemplate(
    input_variables=["document", "operation", "instruction",
                     "thought", "action", "edited_document", "output", "grade"],
    template="Document: {document}\nOperation: {operation}\nInstruction: {instruction}\nThought: {thought}\nAction: {action}\nEdited Document: {edited_document}\nOutput: {output}\nGrade: {grade}",
)


prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_prompt,
    prefix=prefix,
    suffix=template,
    input_variables=['document', 'operation', 'instruction',
                     'thought', 'action', 'edited_document', 'output']
)
# prompt = PromptTemplate(
#     prefix=prefix,
#     input_variables=['document', 'operation', 'instruction', 'output'], template=template)

llm = OpenAI(temperature=0)
grader = LLMChain(llm=llm, prompt=prompt, verbose=True)

grade_outputs = grader.apply(generated_examples)

pp = pprint.PrettyPrinter(indent=2, sort_dicts=False, width=150)
pp.pprint(grade_outputs)


json_data = json.dumps(grade_outputs, indent=2)
with open('examples-qa.json', 'w') as file:
    file.write(json_data)
