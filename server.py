import logging
import os
from flask import Flask, request, render_template, flash
import openai
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load API keys from file
def load_api_keys(file_path):
    keys = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=')
            keys[key] = value
    print("Loaded API keys:", keys)  # Add this line for debugging
    return keys

api_keys = load_api_keys('api_key.txt')
print("API keys dictionary:", api_keys)  # Add this line for debugging
openai.api_key = api_keys.get('sk-proj-JpTDWmGTmWAd9uHcftceT3BlbkFJGDBDxlIP6T1wrk7Sxzqr', '')  # Modify this line
serpapi_key = api_keys.get('52c0d7c358e91bfe67ddda32575b06889327245b7a4db8eecbfe3fb1c36b750a', '')  # Modify this line


@app.route('/')  
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    try:
        search_results = fetch_search_results(query)
        summary = summarize_results(search_results)
    except requests.exceptions.RequestException as e:
        logger.error(f"HTTP error occurred: {e}")
        flash("An error occurred while fetching search results. Please check your internet connection and try again.")
        return render_template('index.html')
    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI error occurred: {e}")
        flash("An error occurred while processing the search results. Please try again later.")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        flash("An unexpected error occurred. Please try again.")
        return render_template('index.html')
    return render_template('results.html', query=query, summary=summary, results=search_results)


def fetch_search_results(query):
    url = f"https://serpapi.com/search.json?q={query}&api_key={serpapi_key}"
    response = requests.get(url)
    response.raise_for_status()  # Raise an HTTPError for bad responses
    data = response.json()
    search_results = [result['title'] for result in data.get('organic_results', [])]
    return search_results

def summarize_results(results):
    prompt = "Summarize the following search results:\n" + "\n".join(results)
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )
    summary = response.choices[0].text.strip()
    return summary

if __name__ == '__main__':
    app.run(debug=True)
