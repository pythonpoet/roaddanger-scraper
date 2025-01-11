from testcases import improved_prompts
# change this file to the path where you have your keys file
#from keys import *
from llm import makeCompute
import copy
from deep_translator import GoogleTranslator
import re 
import json

def translate_text(text, src_lang='auto', dest_lang='en'):
    translator = GoogleTranslator(source=src_lang, target=dest_lang)

    # Translate the text
    try:
        return translator.translate(text)

    except Exception as e:
        return f"Translation failed: {e}"

def extract_json(response):
    # Regex pattern to match a JSON object
    json_pattern = re.compile(r'\{.*\}', re.DOTALL)
    
    # Search for the JSON pattern in the response
    match = json_pattern.search(response)
    
    if match:
        try:
            # Extract the JSON string and parse it
            json_str = match.group(0)
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Extracted JSON is invalid: {json_str}")
            raise Exception(f"JSONDecodeError: {e}")
    else:
        raise Exception("No JSON found in the response.")

def dehum_single_test(msg, Text, explanation=False, model="deepseek/deepseek-chat", local=False):
    """
    Helper function to test a single prompt template.
    If explanation=True, use the prompt template with explanation suffix.
    Returns a tuple (answer, explanation) if explanation=True, else just the answer.
    """
    if explanation:
        # Use the prompt template with explanation suffix
        prompt = msg["explanation"]
    else:
        # Use the standard prompt template
        prompt = msg["standard"]

    response = makeCompute(
        messages=format_message(prompt, Text), 
        model=model, 
        local=local)
    try:
        if explanation:
        # Parse the JSON response to extract the answer and explanation
            return  json.loads(response)
        else:
            # Return the direct response
            return {"answer":response}
    except json.JSONDecodeError as e:
        # Log the invalid response for debugging
        print(f"Invalid JSON response: {response}")
        
        try:
            # Remove extra data or fix formatting
            return extract_json(response)
        except Exception as e:
            raise Exception(f"Failed to parse JSON: {e}")
        
    except Exception as e:
        # TODO, here the model could be feed its answer to itself to auto correct -> this is know as agentic llm flows could also generally be implemented to boost performance
        raise Exception(f"Value error response: {response}is not what it should be err: {e}")
    

def format_message(prompt_message:list, Text:str):
    msg = copy.deepcopy(prompt_message)
    try:
        # Check if the template contains the required placeholders
        template = msg[2]['content']
        if "{Text}" not in template:
            raise ValueError("The template is missing required placeholders: 'Text'")
        
        # Format the template
        msg[2]['content'] = template.format(Text=Text)
        return msg
    except Exception as e:
        raise Exception(f"Failed to format the message: {e}")
    
def dehumanisation_test(Title, Article, explanation=False, model="deepseek/deepseek-chat", local=False):
    """
    Main function to test for dehumanisation.
    If explanation=True, returns a tuple (failure_code, explanation) if a test fails.
    If explanation=False, returns just the failure_code.
    """
    # Test 1: All parties mentioned
    result = dehum_single_test(improved_prompts["prompt_all_parties"], Text=Title, explanation=explanation, model=model, local=local)
    if result["answer"] == 0:
        return (0, result["explanation"]) if explanation else 0
   
    # Test 2: All parties referred to as humans
    result = dehum_single_test(improved_prompts["prompt_human_reference"], Text=Title,explanation=explanation, model=model, local=local)
    if result["answer"] == 0:
        return (1, result["explanation"]) if explanation else 1

    return (6, "No dehumanisation detected.") if explanation else 6
    # Test 3: Grammatical subject is human
    result = dehum_single_test(prompts["prompt_subject"], Text=Title,explanation=explanation, model=model, local=local)
    if result["answer"] == 0:
        return (2, result["explanation"]) if explanation else 2

    # Test 4: Text is written in active grammar
    result = dehum_single_test(prompts["prompt_active_grammar"], Text=Title, explanation=explanation, model=model, local=local)
    if result["answer"] == 0:
        return (3, result["explanation"]) if explanation else 3

    # Test 5: Physical or psychological consequences mentioned
    result = dehum_single_test(prompts["prompt_consequences_mentioned"], Text=Title + "\n" + Article, explanation=explanation, model=model, local=local)
    if result["answer"] == 0:
        return (4, result["explanation"]) if explanation else 4

    # Test 6: Crash placed in a larger pattern
    result = dehum_single_test(prompts["prompt_larger_pattern"], Text=Title + "\n" + Article, explanation=explanation, model=model, local=local)
    if result["answer"] == 0:
        return (5, result["explanation"]) if explanation else 5

    # If no test fails
    return (6, "No dehumanisation detected.") if explanation else 6

