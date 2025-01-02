import json
import re
import torch
import random  # <-- import random
from typing import Optional, Dict, Any, Type, Union
from transformers import AutoModelForCausalLM, AutoTokenizer
from jsonformer.main import Jsonformer

from pydantic import BaseModel, create_model, Field

class EasyLLM:
    """Wrapper for language model interactions with simplified interface."""

    def __init__(self, model_path: str, max_memory: Optional[Dict[Union[int, str], str]] = None) -> None:
        """Initialize language model with specified parameters.

        Args:
            model_path: Path or identifier for the model
            max_memory: Memory allocation settings per device
        """
        self.model_path = model_path
        self._model = None
        self._tokenizer = None
        self.max_memory = max_memory or {0: "12GiB", "cpu": "30GiB"}
        self._device = "cuda" if torch.cuda.is_available() else "cpu"
        self._load_model()

    def _load_model(self):
        print(f"Loading model from '{self.model_path}' ...")
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self._model = AutoModelForCausalLM.from_pretrained(
            self.model_path,
            device_map="auto",
            max_memory=self.max_memory,
            low_cpu_mem_usage=True
        )
        if self._tokenizer.pad_token_id is None:
            self._tokenizer.pad_token_id = self._tokenizer.eos_token_id or 0
        print("Model loaded successfully.")

    def ask_question(self, prompt: str, max_new_tokens: int = 300) -> str:
        temperature = random.uniform(0.1, 2.0)
        
        inputs = self._tokenizer(prompt, return_tensors="pt")
        input_ids = inputs["input_ids"].to(self._device)

        with torch.no_grad():
            outputs = self._model.generate(
                input_ids=input_ids,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                pad_token_id=self._tokenizer.pad_token_id
            )

        generated_ids = outputs[0]
        gen_tokens = generated_ids[input_ids.shape[-1]:]
        raw_text = self._tokenizer.decode(gen_tokens, skip_special_tokens=True)
        return raw_text

    def create_pydantic_model_from_schema(self, schema: Dict[str, Any]) -> Type[BaseModel]:
        model_fields = {}
        for k, v in schema.items():
            if isinstance(v, tuple) and len(v) == 2:
                model_fields[k] = (Optional[v[0]], Field(default=v[1]))
            else:
                model_fields[k] = (v, Field(...))
        DynamicModel = create_model('DynamicModel', **model_fields)
        return DynamicModel

    def ask_question_with_schema(self, prompt: str, json_schema: dict, max_new_tokens: int = 128) -> dict:
        temperature = random.uniform(0.1, 2.0)
        jsonformer = Jsonformer(
            self._model,
            self._tokenizer,
            json_schema,
            prompt,
            max_number_tokens=max_new_tokens,
            max_string_token_length=max_new_tokens,
            temperature=temperature
        )
        generated_json = jsonformer()
        return generated_json

    def unload_model(self):
        print("Unloading model...")
        if self._model:
            del self._model
            self._model = None
        if self._tokenizer:
            del self._tokenizer
            self._tokenizer = None
        torch.cuda.empty_cache()
        print("Model unloaded.")
