from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import xml.etree.ElementTree as ET
import re

app = Flask(__name__)
CORS(app)

# XMLをパースして辞書を作成する関数
def parse_xml_to_dict(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    word_dict = {}
    
    def normalize(text):
        return re.sub(r'\s+', '', text).lower()
    
    for pattern in root.find('patterns'):
        name = pattern.find('name').text
        description = pattern.find('description').text
        word_dict[normalize(name)] = description.strip()
    
    for keyword in root.find('keywords'):
        name = keyword.find('name').text
        description = keyword.find('description').text
        word_dict[normalize(name)] = description.strip()
    
    return word_dict

# 辞書データの読み込み
word_dict = parse_xml_to_dict('phits_keywords.xml')

# デバッグ用に辞書の内容を表示
print("辞書の内容:")
for k, v in word_dict.items():
    print(f"{k}: {v}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/search', methods=['GET'])
def search_word():
    word = request.args.get('word')
    normalized_word = re.sub(r'\s+', '', word).lower()
    print(f"検索クエリ: {word} (正規化: {normalized_word})")  # デバッグ用
    if normalized_word in word_dict:
        return jsonify({"found": True, "description": word_dict[normalized_word]})
    else:
        return jsonify({"found": False})

if __name__ == '__main__':
    app.run(debug=True, port=5010)
