from io import BytesIO
from PIL import Image, ImageFont
import requests

from .ai_utils import generate_image, generate_json_object
from .image_utils import paste_image, write_text, write_text_centered_within_box, write_text_centered


def get_card_illustration(card_name):

    img_metadata = generate_image(card_name, "dall-e-3")

    img_url = img_metadata.data[0].url
    
    card_image = Image.open(BytesIO(requests.get(img_url).content))

    return card_image

def get_card_parameters(card_name: str):

    card_parameters = generate_json_object(f"""
        For the given card name "{card_name}", generate the following Magic the Gathering card parameters in json format:

        {{
            "name": string,
            "color": lower case string,
            "cost": a list of letters or numbers,
            "power": integer,
            "toughness": integer,
            "type": string,
            "text" string,
            "flavor_text": string,
            "non_creature": boolean
        }}

        """, system_message="You are Magic the Gathering Card generator.", temperature=0)
    
    return card_parameters

def load_blank_card(color, non_creature):
    if color not in ["white", "blue", "black", "red", "green"]:
        color = "white"

    if non_creature:
        filename = f"assets/images/cards/{color}_card.jpg"
    else:
        filename = f"assets/images/cards/{color}_card_creature.jpg"
    
    blank_card = Image.open(filename).convert("RGB")

    return blank_card

def draw_manas(card, manas):

    for i, mana in enumerate(reversed(manas)):
        mana_filename = f"assets/images/manas/{mana}.png"

        try:
            mana_image = Image.open(mana_filename).resize((17,17))
            card = paste_image(source_image=mana_image, target_image=card, x=345-i*19, y=38, mask=mana_image)

        except FileNotFoundError:
            pass

    return card

def place_illustration(card, illustration):
    illustration = illustration.convert("RGB").resize((329,242))
    card = paste_image(source_image=illustration, target_image=card, x=35, y=68, mask=None)
    return card

def write_card_name(card, name):
    card = write_text(image=card, text=name, font=ImageFont.truetype("assets/fonts/title_type.ttf", 20), x=40, y=40)
    return card

def write_card_type(card, type):
    card = write_text(image=card, text=type, font=ImageFont.truetype("assets/fonts/title_type.ttf", 18), x=40, y=322)
    return card

def write_card_text_and_flavor(card, ability_text, flavor_text):
    
    total_text_area_width = 321
    total_text_area_height = 136
    
    total_text_area_x = 38
    total_text_area_y = 355

    if ability_text:        
        if flavor_text:
            ability_proportion = 0.7
        else:
            ability_proportion = 1.0
    else:
        ability_proportion = 0.0

    ability_text_y = total_text_area_y
    ability_text_height = total_text_area_height * ability_proportion

    flavor_text_y = ability_text_y + ability_text_height
    flavor_text_height = total_text_area_height - ability_text_height

    if ability_text:
        card = write_text_centered_within_box(
            card, 
            ability_text, 
            total_text_area_x, ability_text_y, 
            total_text_area_width, ability_text_height, 
            "assets/fonts/text.ttf", 10, 20
        )

    if flavor_text:
        card = write_text_centered_within_box(
            card, 
            flavor_text, 
            total_text_area_x, flavor_text_y, 
            total_text_area_width, flavor_text_height, 
            "assets/fonts/flavor_text.ttf", 8, 14
        )
    
    return card

def write_card_power_and_toughness(card, power, toughness):
    return write_text_centered(
        image=card, 
        text=f"{power}/{toughness}", 
        font=ImageFont.truetype("assets/fonts/power_toughness.ttf", 22), 
        x=307, y=506, width=53
    )

def render_card(color, non_creature, manas, illustration, name, type, ability_text, flavor_text, power, toughness):
    rendered_card = load_blank_card(color, non_creature)
    rendered_card = draw_manas(rendered_card, manas)
    rendered_card = place_illustration(rendered_card , illustration)
    rendered_card = write_card_name(rendered_card, name)
    rendered_card = write_card_type(rendered_card, type)
    rendered_card = write_card_text_and_flavor(rendered_card, ability_text, flavor_text)
    
    if not non_creature:
        rendered_card = write_card_power_and_toughness(rendered_card, power, toughness)
    
    return rendered_card