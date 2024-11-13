import requests
import json
from keys import *
import ollama
from openai import OpenAI


def makeCompute(messages: list, model: str = "llama3.2", local: bool =True):

  if not local:
    return openRouterCall(messages=messages, model=model)
  else:
    result = ollamaMakeComute(messages=messages, model=model)
    return result['message']['content']
def ollamaMakeComute(messages: list, model: str = "llama3.2"):
  return  ollama.chat(model=model, messages=messages)

def openRouterCall(messages: list, model: str = "llama3.2",):
  # gets API Key from environment variable OPENAI_API_KEY
  client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
  )
  completion = client.chat.completions.create(
    model=model,
    messages=messages
  )
  return completion.choices[0].message.content