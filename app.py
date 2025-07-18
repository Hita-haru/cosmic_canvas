from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import json
import os
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'cosmic_secret_v3!'
socketio = SocketIO(app)

GAME_STATE_FILE = 'gamestate.json'

# --- Game State ---
discovered_elements = set()
celestials_on_canvas = []
# --- End Game State ---

# Vastly expanded combinations
combinations = {
    # Tier 1: Basic Building Blocks
    ("ガス", "重力"): ["原始星", "#FFDAB9", 10],
    ("光", "星屑"): ["輝く塵", "#F5F5DC", 2],
    ("水", "重力"): ["氷塊", "#B0E0E6", 4],
    ("鉄", "重力"): ["金属質の小惑星", "#C0C0C0", 5],
    ("時間", "空間"): ["時空", "#483D8B", 0],
    ("暗黒物質", "重力"): ["重力レンズ効果", "#2F4F4F", 0],

    # Tier 2: First Stars and Structures
    ("光", "原始星"): ["恒星", "#FFD700", 15],
    ("氷塊", "重力"): ["小惑星", "#A9A9A9", 3],
    ("ガス", "恒星"): ["星雲", "#4B0082", 30],
    ("原始星", "原始星"): ["褐色矮星", "#A52A2A", 12],

    # Tier 3: Formation of Systems
    ("小惑星", "水"): ["彗星", "#ADD8E6", 5],
    ("恒星", "重力"): ["惑星", "#4682B4", 8],
    ("恒星", "恒星"): ["連星", "#FFFF00", 20],
    ("分子雲", "重力"): ["星団", "#FFFAF0", 60],

    # Tier 4: Diverse Planets and Phenomena
    ("惑星", "ガス"): ["木星型惑星", "#D2B48C", 12],
    ("惑星", "水"): ["地球型惑星", "#32CD32", 9],
    ("連星", "重力"): ["ブラックホール", "#000000", 25],
    ("恒星", "輝く塵"): ["太陽風", "#FFFACD", 1],
    ("地球型惑星", "鉄"): ["磁場", "#00BFFF", 0],

    # Tier 5: Life's Beginnings and Stellar Events
    ("地球型惑星", "太陽風"): ["オーロラ", "#7FFF00", 0],
    ("地球型惑星", "有機物"): ["原始生命", "#98FB98", 1],
    ("ブラックホール", "恒星"): ["超新星爆発", "#FF4500", 50],
    ("磁場", "太陽風"): ["ヴァン・アレン帯", "#FF69B4", 0],

    # Tier 6: Evolution and Galactic Formation
    ("超新星爆発", "重力"): ["中性子星", "#FFFFFF", 5],
    ("星雲", "連星"): ["銀河", "#DA70D6", 100],
    ("原始生命", "時間"): ["進化", "#BA55D3", 0],
    ("超新星爆発", "ガス"): ["分子雲", "#8B4513", 40],

    # Tier 7: Complex Life and Cosmic Signals
    ("進化", "地球型惑星"): ["生命の惑星", "#00FF7F", 10],
    ("中性子星", "中性子星"): ["重力波", "#E6E6FA", 0],
    ("中性子星", "磁場"): ["パルサー", "#E0FFFF", 6],

    # Tier 8: Intelligence and Early Technology
    ("生命の惑星", "進化"): ["知的生命体", "#F0FFFF", 0],
    ("知的生命体", "鉄"): ["道具", "#D2691E", 0],
    ("知的生命体", "輝く塵"): ["芸術", "#FFC0CB", 0],

    # Tier 9: Advanced Civilization
    ("知的生命体", "道具"): ["テクノロジー", "#8A2BE2", 0],
    ("銀河", "ブラックホール"): ["クエーサー", "#F0E68C", 120],
    ("テクノロジー", "恒星"): ["ダイソン球", "#BDB76B", 18],
    ("芸術", "時間"): ["文化", "#FFE4B5", 0],

    # Tier 10: Transcendent Concepts
    ("テクノロジー", "時間"): ["情報", "#ADD8E6", 0],
    ("文化", "情報"): ["集合意識", "#E6E6FA", 0],
    ("テクノロジー", "空間"): ["ワープ航法", "#9370DB", 0],

    # --- Legendary Path ---
    ("集合意識", "クエーサー"): ["宇宙の意識", "#FFD700", 200] # The End
}

LEGENDARY_CELESTIAL = "宇宙の意識"

def load_game_state():
    global discovered_elements, celestials_on_canvas
    if os.path.exists(GAME_STATE_FILE):
        try:
            with open(GAME_STATE_FILE, 'r', encoding='utf-8') as f:
                state = json.load(f)
                discovered_elements = set(state.get('elements', []))
                celestials_on_canvas = state.get('celestials', [])
        except (json.JSONDecodeError, IOError):
            # If file is corrupted or unreadable, start fresh
            discovered_elements = set()
            celestials_on_canvas = []

    if not discovered_elements:
        discovered_elements = {"星屑", "重力", "ガス", "光", "水", "鉄", "有機物", "時間", "空間", "暗黒物質"}
        
    if not celestials_on_canvas:
         celestials_on_canvas = []

def save_game_state():
    state = {
        'elements': sorted(list(discovered_elements)),
        'celestials': celestials_on_canvas
    }
    with open(GAME_STATE_FILE, 'w', encoding='utf-8') as f:
        json.dump(state, f, indent=4, ensure_ascii=False)

@app.route('/')
def index():
    # The template is now simpler, it just needs to exist
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    # On connection, send the whole current state to the client
    load_game_state() # Ensure we have the latest state
    state = {
        'elements': sorted(list(discovered_elements)),
        'celestials': celestials_on_canvas
    }
    emit('current_state', state)

@socketio.on('combine')
def handle_combine(json_data):
    element1 = json_data['element1']
    element2 = json_data['element2']
    
    key = tuple(sorted((element1, element2)))
    result = combinations.get(key)
    
    if result:
        new_name, color, size = result
        
        is_new_discovery = new_name not in discovered_elements
        
        # Add the new element to the discovered list
        if is_new_discovery:
            discovered_elements.add(new_name)

        # Create the object to be drawn or announced
        celestial_data = {
            "name": new_name,
            "color": color,
            "size": size,
            "x": random.randint(50, 1200), # Expanded canvas in mind
            "y": random.randint(50, 800)
        }
        
        # Only add to canvas if it has a visual size
        if size > 0:
            celestials_on_canvas.append(celestial_data)
            emit('new_celestial', celestial_data, broadcast=True)
        else: # It's a concept/event, just announce it
            emit('new_concept', {"name": new_name}, broadcast=True)

        # If it was a brand new discovery for everyone, update element lists
        if is_new_discovery:
            emit('new_element', {'name': new_name}, broadcast=True)

        # Check for the ultimate win condition
        if new_name == LEGENDARY_CELESTIAL:
            emit('game_won', {'winner': request.sid, 'celestial': new_name}, broadcast=True)

        save_game_state()

if __name__ == '__main__':
    load_game_state()
    socketio.run(app, host='0.0.0.0', port=5000, allow_unsafe_werkzeug=True)