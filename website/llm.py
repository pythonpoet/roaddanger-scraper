import importlib.util
import sys
from pathlib import Path

compiled_file = str(Path(__file__).parent / "__pycache__" / "keys.cpython-311.pyc")

spec = importlib.util.spec_from_file_location("keys", compiled_file)
keys = importlib.util.module_from_spec(spec)
sys.modules["keys"] = keys
spec.loader.exec_module(keys)

OPENROUTER_API_KEY = keys.OPENROUTER_API_KEY

import requests
import json
#from keys import *
#import ollama
from openai import OpenAI

def makeCompute(messages: list, model: str = "llama3.2", local: bool =True):

  if not local:
    return openRouterCall(messages=messages, model=model)
  else:
    raise Exception("Temporarily deactivated ollama")
    result = ollamaMakeComute(messages=messages, model=model)
    return result['message']['content']
def ollamaMakeComute(messages: list, model: str = "llama3.2"):
  pass
  #return  ollama.chat(model=model, messages=messages)

def openRouterCall(messages: list, model: str = "llama3.2",):
  # gets API Key from environment variable OPENAI_API_KEY
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key= OPENROUTER_API_KEY,
  )
  completion = client.chat.completions.create(
    model=model,
    messages=messages
  )
  return completion.choices[0].message.content