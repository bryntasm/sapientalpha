from flask import Flask, request, jsonify, render_template
import json
import re

app = Flask(__name__)

class colors:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def load_data():
    with open('data.json', 'r') as f:
        data = json.load(f)
    return data

data = load_data()

def get_character_info(query, data):
    match = re.match(r"show me the top (\d+) weapons for (.+)", query.lower())
    if match:
        num_weapons = int(match.group(1))
        character_name = match.group(2).strip()
    else:
        character_name = query.lower()

    character = data.get(character_name)
    if character:
        if match:
            weapons = sorted(character['Weapons'])[:num_weapons]
            return {'weapons': weapons}
        else:
            return character
    else:
        return {'error': 'Character not found'}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_build', methods=['POST'])
def get_build():
    character_name = request.form['character_name']
    info = get_character_info(character_name, data)
    return jsonify(info)

if __name__ == '__main__':
    app.run(debug=True)