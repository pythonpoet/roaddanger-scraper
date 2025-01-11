import subprocess
from flask import Flask, request, jsonify, render_template, redirect, url_for, g
from testcases import improved_prompts
from llm import makeCompute
from dehumanisation_test import dehumanisation_test
import copy
from deep_translator import GoogleTranslator
import re
import json

app = Flask(__name__) 

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/dehumanisation-test', methods=['POST'])
def dehumanisation_test_api():
    try:
        # Get input from the POST request
        data = request.json
        title = data.get("title", "")
        full_text = data.get("full_text", "")
        explanation = data.get("explanation", False)  # Optional parameter
        
        # Ensure required inputs are provided
        if not title or not full_text:
            return jsonify({"error": "Both 'title' and 'full_text' are required."}), 400
        
        # Run the dehumanisation test
        result = dehumanisation_test(Title=title, Article=full_text, explanation=explanation)
        
        # Return the result as JSON
        if explanation:
            return jsonify({
                "failure_code": result[0],
                "explanation": result[1]
            })
        else:
            return jsonify({"failure_code": result})
    
    except Exception as e:
        # Handle any errors
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
