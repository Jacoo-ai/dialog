from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# 获取当前文件的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
html_path = os.path.join(current_dir, 'rapport.html')

@app.route('/')
def index():
    with open(html_path, 'r') as file:
        html_content = file.read()
    return html_content

@app.route('/start_demo', methods=['GET'])
def start_demo():
    return render_template('rapport_start.html')

@app.route('/send_text', methods=['POST'])
@app.route('/send_text/<string:text_to_send>', methods=['GET'])
def send_text(text_to_send=None):
    print(text_to_send)
    return render_template('rapport_text.html', text_to_say = text_to_send)

if __name__ == '__main__':
    app.run(debug=True)