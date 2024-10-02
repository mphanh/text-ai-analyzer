from flask import Flask, request, render_template, redirect, url_for
from utils.file_handler import read_docx, read_pdf
from utils.web_scraper import extract_text_from_url
from utils.summarizer import authenticate_client, summarize_text
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Load Azure credentials from environment variables for security
AZURE_KEY = os.getenv('AZURE_OPENAI_API_KEY')
AZURE_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')

client = authenticate_client(AZURE_KEY, AZURE_ENDPOINT)

@app.route('/', methods=['GET', 'POST'])
def index():
    summary = ""
    error = ""
    if request.method == 'POST':
        try:
            text = ""
            if 'file' in request.files and request.files['file'].filename != '':
                file = request.files['file']
                filename = file.filename.lower()
                if filename.endswith('.txt'):
                    text = file.read().decode('utf-8')
                elif filename.endswith('.docx'):
                    text = read_docx(file)
                elif filename.endswith('.pdf'):
                    text = read_pdf(file)
                else:
                    error = "Unsupported file type. Please upload TXT, DOCX, or PDF."
            elif 'url' in request.form and request.form['url'] != '':
                url = request.form['url']
                text = extract_text_from_url(url)
            else:
                error = "No input provided. Please upload a file or enter a URL."

            if text:
                summaries = summarize_text(client, [text])
                summary = summaries[0]
        except Exception as e:
            error = str(e)
    return render_template('index.html', summary=summary, error=error)

if __name__ == '__main__':
    app.run(debug=True)
