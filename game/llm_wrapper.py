import json
import gc
import torch
from game.easy_llm import EasyLLM

def ask_question(question, schema, max_new_tokens=500, llm_name="unsloth/mistral-7b-instruct-v0.3-bnb-4bit"):
    llm = EasyLLM(llm_name)
    #schema_model = llm.create_pydantic_model_from_schema(schema)
    response = llm.ask_question_with_schema(prompt=question, json_schema=schema, max_new_tokens=max_new_tokens)
    llm.unload_model()
    gc.collect()
    print("Response:", response)
    return response