import os

import time

from flask import Flask, render_template, request

from generator import generate_card

GENERATED_CARDS_DIR = os.path.join("static", "generated_cards")

os.makedirs(GENERATED_CARDS_DIR, exist_ok=True)

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def genmagic():

    search_query = request.args.get("query", "")

    previous_filenames = get_previous_generated_card(20)

    if search_query != "":
        filename = _create_card_and_save(search_query)
    else:
        filename = None

    return render_template("index.html", filename=filename, previous_filenames=previous_filenames)

def get_previous_generated_card(top_k):
    """Get a list of the top k previously generated cards sorted by timestamp."""
    files = os.listdir(GENERATED_CARDS_DIR)
    files = sorted(files, key=lambda x: os.path.getmtime(os.path.join(GENERATED_CARDS_DIR, x)), reverse=True)
    return files[:top_k]

def _create_card_and_save(card_name):

    card = generate_card(card_name)
    
    timestamp = time.time()

    filename = f"{card_name}_{timestamp}.png"
    card.save(os.path.join(GENERATED_CARDS_DIR, filename))

    return filename
    
if __name__ == "__main__":
    app.run(debug=True)