from flask import Flask, request, jsonify
import openai
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.
import os
# Retrieve the API key value from the environment variable

app = Flask(__name__)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
# Set the API key
openai.api_key = os.getenv("API_KEY")

@app.route("/generate-content", methods=["POST"])
def generateContent():
    # Get the input string from the request
    processInput = "Act as a copywriter and write a professional youtube video title and description by using this keyword: "
    processInput += request.json["input_string"]
    # Generate a response
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=processInput,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=1,
        presence_penalty=1
    )

    generated_sentences = response["choices"]

    # Get the first generated sentence
    generated_sentence = generated_sentences[0]["text"]

    # Create a JSON object containing the generated sentence
    result = {"generated_sentence": generated_sentence}
    return result

def generate_suggestions(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=10,
        n=10,
        stop=None,
        temperature=0.5,
    )

    # extract generated text from response
    suggestions = [choice.text.strip() for choice in response.choices]

    # return up to 10 suggestions
    return suggestions[:10]

# define Flask endpoint
@app.route("/search-suggestions", methods=["POST"])
def suggestions():
    processInput = "Act as a search engine and give 10 search phrases without numbering based on this input: "
    # get prompt from request body
    processInput+= request.json["prompt"]

    # generate suggestions
    suggestions = generate_suggestions(processInput)

    # return JSON response
    return jsonify({"suggestions": suggestions})


@app.route("/keyword-suggestions", methods=["POST"])
def keywordSuggestions():
    processInput = "Act as a seo specialist and give 20 common keywords and 20 uncommon keywords based on this input: "
    # get prompt from request body
    processInput+= request.json["prompt"]

    # generate suggestions
    suggestions = generate_suggestions(processInput)

    # return JSON response
    return jsonify({"suggestions": suggestions})

if __name__ == '__main__':
    app.run(host='0.0.0.0')

