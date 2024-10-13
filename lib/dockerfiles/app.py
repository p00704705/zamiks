from flask import render_template
from flask import Flask, request
from backend import summarise


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/app')
def blog():
    return "Hello, from Zamikx App!!"

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/summarise')
def summarise():
    user_input = request.form.get('user_input')
    return render_template('summarise.html')

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0',port=8081,debug=True)