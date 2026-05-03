from flask import Flask, render_template, request, jsonify
import chess
import random

app = Flask(__name__)
game = chess.Board()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/move", methods=["POST"])
def move():
    global game
    data = request.get_json()

    move = chess.Move.from_uci(data["from"] + data["to"])

    if move in game.legal_moves:
        game.push(move)
        return jsonify({"status": "ok", "game_status": get_status()})
    return jsonify({"status": "invalid"})

@app.route("/reset", methods=["POST"])
def reset():
    global game
    game = chess.Board()
    return jsonify({"status": "reset"})

@app.route("/hint")
def hint():
    move = random.choice(list(game.legal_moves))
    return jsonify({"hint": game.san(move)})

@app.route("/status")
def status():
    return jsonify({"game_status": get_status()})

def get_status():
    if game.is_checkmate():
        return f"🏆 {'White' if not game.turn else 'Black'} wins!"
    elif game.is_stalemate():
        return "Draw"
    elif game.is_check():
        return "Check!"
    return "Game in progress"

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
