from flask import Flask, render_template, request, jsonify
import chess
import random

app = Flask(__name__)
game = chess.Board()

# ---------------- HOME ----------------
@app.route("/")
def index():
    return render_template("index.html")

# ---------------- MOVE ----------------
@app.route("/move", methods=["POST"])
def move():
    global game
    data = request.get_json()

    move = chess.Move.from_uci(data["from"] + data["to"])

    if move in game.legal_moves:
        game.push(move)

        return jsonify({
            "status": "ok",
            "game_status": get_status()
        })
    else:
        return jsonify({"status": "invalid"})

# ---------------- RESET ----------------
@app.route("/reset", methods=["POST"])
def reset():
    global game
    game = chess.Board()
    return jsonify({"status": "reset"})

# ---------------- HINT ----------------
@app.route("/hint")
def hint():
    moves = list(game.legal_moves)
    if not moves:
        return jsonify({"hint": "No moves available"})
    move = random.choice(moves)
    return jsonify({"hint": game.san(move)})

# ---------------- STATUS ----------------
@app.route("/status")
def status():
    return jsonify({"game_status": get_status()})

# ---------------- LOGIC ----------------
def get_status():
    if game.is_checkmate():
        return f"🏆 {'White' if not game.turn else 'Black'} wins by Checkmate!"
    elif game.is_stalemate():
        return "🤝 Draw by stalemate"
    elif game.is_insufficient_material():
        return "🤝 Draw (insufficient material)"
    elif game.is_check():
        return f"⚠️ {'White' if game.turn else 'Black'} is in check"
    else:
        return f"{'White' if game.turn else 'Black'} to move"

# ---------------- RUN ----------------
if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
