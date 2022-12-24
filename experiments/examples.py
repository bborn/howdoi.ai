from langchain.prompts import load_prompt, FewShotPromptTemplate, PromptTemplate
from langchain.prompts.example_selector import SemanticSimilarityExampleSelector
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.example_generator import generate_example
import json
import random

import os

# insert - add new text at end or within the document. Can can a user instruction, or not
# expand - expand the user selected text, using the user instruction or not
# update - update the user selected text, following user's instruction
# condense - condense the user selected text, following user's instruction, or just condense it
# compose - invent an entirely new document, following user's instruction

f = open('examples.json')
examples = json.load(f)


template = """ 
  "document": "{document}",
  "operation": "{operation}",
  "instruction": "{instruction}",
  "thought": "{thought}",
  "action": "{action}",
  "edited_document": "{edited_document}",
  "output": "{output}" 
"""

example_template = PromptTemplate(template=template, input_variables=[
                                  "document", "operation", "instruction", "thought", "action", "output", "edited_document"])

# reject examples which have "grade" INAPPROPRIATE
examples = [example for example in examples if example["grade"] == "APPROPRIATE"]

# remove the "grade" key from examples
for example in examples:
    del example["grade"]

generated_examples = []

for _ in range(3):
    random.shuffle(examples)
    example = generate_example(
        examples, OpenAI(temperature=0.5), example_template)

    print(f"""
    {{
      {example}
    }},
    """)

    json_string = f"""{{
      {example}
    }}"""
    example_json = json.loads(json_string)

    generated_examples.append(example_json)

    json_data = json.dumps(generated_examples, indent=2)
    with open('examples-generated.json', 'w') as file:
        file.write(json_data)
