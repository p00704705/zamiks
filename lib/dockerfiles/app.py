from flask import render_template
from flask import Flask, request
from backend.summarize_text import summarize


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test')
def blog():
    return "Hello, from Zamikx App!!"

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/submit', methods=['POST'])
def submit():
    max_words = request.form.get('max_words')
    num_sents = request.form.get('num_sents')
    input_type = request.form.get('input_type')
    url = request.form.get('url') if input_type == 'url' else None
    user_text = request.form.get('user_text') if input_type == 'text' else None

    # Call the summarize function
    result = summarize(max_words, num_sents, url, user_text)

    # Redirect to a result page or render a template with the result
    return render_template('result.html', result=result)


@app.route('/summarize')
def summarise():
    return render_template('summarize.html')

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0',port=8081,debug=True)