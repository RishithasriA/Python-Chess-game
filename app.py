from flask import Flask, request
import chess
import chess.svg   # ✅ IMPORTANT (fixes your error)

app = Flask(__name__)

# Global game board
game = chess.Board()

@app.route("/", methods=["GET", "POST"])
def index():
    global game

    if request.method == "POST":
        move = request.form.get("move")

        try:
            chess_move = game.parse_san(move)

            if chess_move in game.legal_moves:
                game.push(chess_move)
        except:
            pass

    # Generate board SVG
    board_svg = chess.svg.board(board=game)

    # HTML page
    return f"""
    <html>
    <head>
        <title>Chess Game</title>
    </head>
    <body style="text-align:center; font-family:Arial;">

        <h2>♟️ Online Chess Game</h2>

        {board_svg}

        <br><br>

        <form method="POST">
            <input name="move" placeholder="Enter move (e4, Nf3, Qxd7)" style="padding:10px; width:200px;">
            <button type="submit" style="padding:10px;">Play</button>
        </form>

        <br>

        <form method="POST">
            <input type="hidden" name="reset" value="1">
            <button type="submit" style="padding:10px;">Reset Game</button>
        </form>

    </body>
    </html>
    """

# Reset support
@app.before_request
def reset_game():
    global game
    if request.method == "POST" and request.form.get("reset"):
        game = chess.Board()

if __name__ == "__main__":
    import os
app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
