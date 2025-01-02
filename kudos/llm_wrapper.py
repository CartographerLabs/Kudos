import json
import gc
import torch
from kudos.easy_llm import EasyLLM
import random

models = ["unsloth/mistral-7b-instruct-v0.3-bnb-4bit","unsloth/SmolLM-1.7B-Instruct","unsloth/Llama-3.1-Storm-8B"]

def ask_question(question, schema, max_new_tokens=500, llm_name=None):

    if llm_name == None:
        llm_name = random.choice(models)
        print(f"Choosing model {llm_name}")
    
    llm = EasyLLM(llm_name)
    #schema_model = llm.create_pydantic_model_from_schema(schema)
    response = llm.ask_question_with_schema(prompt=question, json_schema=schema, max_new_tokens=max_new_tokens)
    llm.unload_model()
    gc.collect()
    print("Response:", response)
    return response
