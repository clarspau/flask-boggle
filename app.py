# Import necessary modules and classes
from boggle import Boggle
from flask import Flask, render_template, request, session, jsonify
import secrets

# Create an instance of the Boggle game
boggle_game = Boggle()

# Generate a random 64-character hexadecimal string for the secret key
SECRET_KEY = secrets.token_hex(32)


app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


@app.route("/")
def home_page():
    """Render the home page."""

    # Generate a new Boggle board and store it in the session
    board = boggle_game.make_board()
    session["board"] = board

    # Retrieve the high score and number of plays from the session, default to 0 if not present
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    return render_template("index.html", board=board, highscore=highscore, numplays=numplays)


@app.route("/word-check")
def word_check():
    """Check if the entered word is a valid word in the dictionary."""

    # Retrieve the current Boggle board from the session & get the word to check from the request arguments
    board = session["board"]
    word = request.args["word"]

    # Check if the word is valid on the current board and in the dictionary
    res = boggle_game.check_valid_word(board, word)
    return jsonify({'result': res})


@app.route("/score", methods=["POST"])
def score():
    """Get current score, update the number of plays (numplays), & update the high score if appropriate."""

    # Get the score from the JSON data in the request
    score = request.json["score"]
    highscore = session.get("highscore", 0)
    numplays = session.get("numplays", 0)

    # Update the session's high score to the maximum of the current score and the existing high score and increment the number of plays by 1
    session["highscore"] = max(score, highscore)
    session["numplays"] = numplays + 1

    # Determine if the current score is a new high score & return the new high score
    newHighscore = score > highscore
    return jsonify(newHighscore=newHighscore)
