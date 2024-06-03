from .card_utils import get_card_illustration, get_card_parameters, render_card

def generate_card(card_name):
    card_illustration = get_card_illustration(card_name)
    card_parameters = get_card_parameters(card_name)

    return render_card(
        card_parameters["color"] or "", 
        card_parameters["non_creature"] or False, 
        card_parameters["cost"] or [], 
        card_illustration, 
        card_parameters["name"] or "", 
        card_parameters["type"] or "", 
        card_parameters["text"] or "", 
        card_parameters["flavor_text"] or "", 
        card_parameters["power"] or 0, 
        card_parameters["toughness"] or 0
    )