from app.normalizer import extract_glass


def test_extract_glass_pos_case():
    instructions_raw = [
        {
        "@type": "HowToStep",
        "name": "Prepare glass",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-1",
        "text": "Select and pre-chill a PINEAPPLE SHELL (FROZEN) GLASS."
        },
        {
        "@type": "HowToStep",
            "name": "Prepare garnish",
            "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-2",
            "text": "Cut the top off a small pineapple and carefully scoop out the flesh from the base to leave a shell with 12mm (½ inch) thick walls. Place the shell in a freezer to chill."
        },
        {
        "@type": "HowToStep",
        "name": "Prepare garnish",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-3",
        "text": "Cut a straw sized hole in the sliced off top of the pineapple shell for use as a lid."
        },
        {
        "@type": "HowToStep",
        "name": "BLEND",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-4",
        "text": "Remove the hard core from the pineapple flesh and discard; roughly chop the remaining flesh, add other ingredients and BLEND with one 12oz scoop of crushed ice."
        },
        {
        "@type": "HowToStep",
        "name": "POUR",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-5",
        "text": "POUR into the pineapple shell. (The flesh of one pineapple blended with other ingredients will fill two shells.)"
        },
        {
        "@type": "HowToStep",
        "name": "Garnish",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-6",
        "text": "Serve with a straw."
        }
    ]
    result = extract_glass(instructions_raw)
    assert result == "PINEAPPLE SHELL (FROZEN) GLASS"

def test_extract_glass_no_Prepare_glass_step():
    instructions_raw = [
        {
        "@type": "HowToStep",
        "name": "Prepare grass",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-1",
        "text": "Select and pre-chill a PINEAPPLE SHELL (FROZEN) GLASS."
        },
        {
        "@type": "HowToStep",
            "name": "Prepare garnish",
            "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-2",
            "text": "Cut the top off a small pineapple and carefully scoop out the flesh from the base to leave a shell with 12mm (½ inch) thick walls. Place the shell in a freezer to chill."
        },
        {
        "@type": "HowToStep",
        "name": "Prepare garnish",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-3",
        "text": "Cut a straw sized hole in the sliced off top of the pineapple shell for use as a lid."
        },
        {
        "@type": "HowToStep",
        "name": "BLEND",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-4",
        "text": "Remove the hard core from the pineapple flesh and discard; roughly chop the remaining flesh, add other ingredients and BLEND with one 12oz scoop of crushed ice."
        },
        {
        "@type": "HowToStep",
        "name": "POUR",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-5",
        "text": "POUR into the pineapple shell. (The flesh of one pineapple blended with other ingredients will fill two shells.)"
        },
        {
        "@type": "HowToStep",
        "name": "Garnish",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-6",
        "text": "Serve with a straw."
        }
    ]
    result = extract_glass(instructions_raw)
    assert result is None

def test_extract_glass_empty_instructions():
    instructions_raw = []
    result = extract_glass(instructions_raw)
    assert result is None

def test_extract_glass_name_with_dots():
    instructions_raw = [
        {
        "@type": "HowToStep",
        "name": "Prepare glass",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-1",
        "text": "Select and pre-chill a PINEAPPLE. SHELL. (FROZEN) GLASS."
        },
        {
        "@type": "HowToStep",
            "name": "Prepare garnish",
            "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-2",
            "text": "Cut the top off a small pineapple and carefully scoop out the flesh from the base to leave a shell with 12mm (½ inch) thick walls. Place the shell in a freezer to chill."
        },
        {
        "@type": "HowToStep",
        "name": "Prepare garnish",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-3",
        "text": "Cut a straw sized hole in the sliced off top of the pineapple shell for use as a lid."
        },
        {
        "@type": "HowToStep",
        "name": "BLEND",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-4",
        "text": "Remove the hard core from the pineapple flesh and discard; roughly chop the remaining flesh, add other ingredients and BLEND with one 12oz scoop of crushed ice."
        },
        {
        "@type": "HowToStep",
        "name": "POUR",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-5",
        "text": "POUR into the pineapple shell. (The flesh of one pineapple blended with other ingredients will fill two shells.)"
        },
        {
        "@type": "HowToStep",
        "name": "Garnish",
        "url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco#method-step-6",
        "text": "Serve with a straw."
        }
    ]
    result = extract_glass(instructions_raw)
    assert result == "PINEAPPLE SHELL (FROZEN) GLASS"