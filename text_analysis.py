# validation of method
# try to reproduce roaddangers findings with llm


import os, json
import pandas as pd
from testcases import *
from llm import *
import datetime
import asyncio

models=[
  "openai/o1-mini",
  "llama3.2"
]
model = models[0]
local = False

path_to_json = 'test_data/'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]

llm_eval=[]
 

for index, js in enumerate(json_files):
    with open(os.path.join(path_to_json, js)) as json_file:
        json_text = json.load(json_file)

        print(f'Article: {json_text["id"]} scores {json_text["roaddanger_dehumanisation_score"]} in roaddangers dehumanisation score')
        result=0
        for i in range(0,5):
          def call_func():
            
            prompt_message = [
                {
                'role': 'user',
                'content':  f"""Answer the question with '0' for fals and '1' for truth.
                                Question: Is the city in the same coutry?
                                Amsterdam is in the Netherlands
                              """
                },
                {
                  'role': 'assistant',
                  "content": "1"
                },
                {
                'role': 'user',
                'content':  f"""Answer the question with '0' for fals and '1' for truth.
                                Question: {roaddanger_dehumanisation_question_list[i]}
                                Headline: {json_text['articles'][0]["title"]} 
                                Article: {json_text['articles'][0]["summary"] if not json_text['articles'][0]["alltext"] else json_text['articles'][0]["alltext"]}
                              """
                },
            ]
            return makeCompute(prompt_message, model=model, local=local)

          
          response = None 
          for zx in range(6):
            response = call_func()
            try:
              # test possible value
              if (int(response) == 0) or (int(response) == 1):
                result += int(response)
              else:
                raise Exception("Value error")
              break
            except Exception as e:
              print(f"model halutionated in question {i} attempt {zx}: {response}")

        general_eval = makeCompute(messages=[
          
          {
            'role': 'user',
            'content':  f"""Evaluate dehumanisation in this text in a scale from 0-6
                            Headline: {json_text['articles'][0]["title"]} 
                            Article: {json_text['articles'][0]["summary"] if not json_text['articles'][0]["alltext"] else json_text['articles'][0]["alltext"]}
                          """
          }
        ], model=model, local=local)
          
        print(f"Model {model} eval is { result}")
        llm_eval.append(
          {
            "article_id": json_text['articles'][0]["id"],
            "roaddanger_eval": json_text["roaddanger_dehumanisation_score"],
            "llm_eval": result,
            "llm_eval_general": general_eval,
            "model": model,
            "time-stamp": str(datetime.datetime.now())
          }
        )
print(llm_eval)

