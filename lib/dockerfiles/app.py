from flask import render_template
from flask import Flask, request, jsonify
from backend.summarize_text import summarize_text
from backend.mongdb_connect import store_text
from backend.encypt_decrypt_text import cryptic

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
    summarized_text = summarize_text(max_words, num_sents, url, user_text)

    original_text = """This is an example of a large block of text that represents the original content.
    It can be multiple sentences long and may include various details that are important for summarization."""
   
   
    store_text(user_text, summarized_text)

    # Redirect to a result page or render a template with the result
    return render_template('result.html', result=summarized_text)


@app.route('/summarize')
def summarize():
    return render_template('summarize.html')

@app.route('/encrydecryp')
def crypto():
    return render_template('crypto.html')

@app.route('/encrypt', methods=['POST'])
def encrypt():
    data = request.json
    input_text = data.get('text', '')
    shifter_value = int(data.get('shifter', 1))  # Get the shifter value, default to 1
    # Replace this with your actual encryption logic, possibly using shifter_val

    input_text = data.get('text', '')
    print(input_text)
    print(shifter_value)
    # Replace this with your actual encryption logic
    encrypted_text = cryptic(input_text, 'encrypt', shifter_value)
    return jsonify({'encrypted_text': encrypted_text})

@app.route('/decrypt', methods=['POST'])
def decrypt():
    data = request.json
    input_text = data.get('text', '')
    shifter_value = int(data.get('shifter', 1))  # Get the shifter value, default to 1
    # Replace this with your actual encryption logic, possibly using shifter_val

    input_text = data.get('text', '')
    print(input_text)
    print(shifter_value)
    # Replace this with your actual encryption logic
    decrypted_text = cryptic(input_text, 'decrypt', shifter_value)
    return jsonify({'decrypted_text': decrypted_text})

if __name__ == '__main__':
          
    app.run(threaded=True,host='0.0.0.0',port=8081,debug=True)