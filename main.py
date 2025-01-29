
import random

from flask import Flask, jsonify
from datetime import datetime
import pytz
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from models.pokemon import Base

from flask_cors import CORS

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

CORS(app)  # Enable CORS

# python main.py
# /mypokemonapp/ npm start

# Set up the database
DATABASE_URL = "sqlite:///pokemon.db"
engine = create_engine(DATABASE_URL)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

img_url_home = "https://img.pokemondb.net/sprites/home/normal/"


def format_img_url(pokemon_name, shiny=False):
    formatted_name = pokemon_name.replace(" ", "-").replace("'", "").lower()
    img_type = "shiny" if shiny == "True" else "normal"
    return f"https://img.pokemondb.net/sprites/home/{img_type}/{formatted_name}.png"


def get_pokemon_entries(pokemon_id):
    """Fetch all entries with the same pokemon_id from the database."""
    pokemon_entries = session.execute(
        text("SELECT * FROM pokemon WHERE pokemon_id = :id"), {"id": pokemon_id}
    ).fetchall()

    return [
        {
            "pokemon_id": pokemon.pokemon_id,
            "pokemon_name": pokemon.pokemon_name,
            "form_name": pokemon.form_name,
            "shiny": pokemon.shiny,
            "color_1": pokemon.color_1,
            "color_2": pokemon.color_2,
            "color_3": pokemon.color_3,
            "img_url": format_img_url(pokemon.pokemon_name, shiny=pokemon.shiny)
        }
        for pokemon in pokemon_entries
    ]


@app.route("/api/daily_pokemon")
def api_daily_pokemon():
    amsterdam_tz = pytz.timezone("Europe/Amsterdam")
    current_day = datetime.now(amsterdam_tz).timetuple().tm_yday
    pokemon_id = (current_day % 898) + 1  # Pick a Pokémon ID based on day of the year

    pokemon_entries = get_pokemon_entries(pokemon_id)
    pokemon_name = pokemon_entries[0]["pokemon_name"]
    pokemon_main = {
        "id": pokemon_entries[0]["pokemon_id"],
        "name": pokemon_name,
        "colors": [
            pokemon_entries[0]["color_1"],
            pokemon_entries[0]["color_2"],
            pokemon_entries[0]["color_3"]
        ],
        "form_name": pokemon_entries[0]["form_name"] if pokemon_entries[0]["form_name"] else '',
        "img_url": format_img_url(pokemon_name, shiny=pokemon_entries[0]["shiny"]),
        "current_date": datetime.now(amsterdam_tz).strftime("%Y-%m-%d")
    }

    return jsonify({"main": pokemon_main, "forms": pokemon_entries})


@app.route("/api/change_pokemon")
@app.route("/api/change_pokemon/<int:pokemon_id>")
def api_change_pokemon(pokemon_id=None):
    """Fetch a random or specific Pokémon based on optional ID."""
    if pokemon_id is None:
        pokemon_id = random.randint(1, 1025)
    elif not (1 <= pokemon_id <= 1025):
        return jsonify({"error": "Invalid Pokémon ID. Must be between 1 and 1025"}), 400

    pokemon_entries = get_pokemon_entries(pokemon_id)
    amsterdam_tz = pytz.timezone("Europe/Amsterdam")
    pokemon_name = pokemon_entries[0]["pokemon_name"]

    pokemon_main = {
        "id": pokemon_entries[0]["pokemon_id"],
        "name": pokemon_name,
        "colors": [
            pokemon_entries[0]["color_1"],
            pokemon_entries[0]["color_2"],
            pokemon_entries[0]["color_3"]
        ],
        "form_name": pokemon_entries[0]["form_name"] if pokemon_entries[0]["form_name"] else '',
        "img_url": format_img_url(pokemon_name, shiny=pokemon_entries[0]["shiny"]),
        "current_date": datetime.now(amsterdam_tz).strftime("%Y-%m-%d")
    }

    return jsonify({"main": pokemon_main, "forms": pokemon_entries})


if __name__ == "__main__":
    app.run(debug=True)
