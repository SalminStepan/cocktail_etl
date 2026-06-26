from app.normalizer import extract_method


def test_extract_method_pos_case():
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
    result = extract_method(instructions_raw)
    assert result == "BLEND"

def test_extract_method_invalid_names():
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
        "name": "SLEND",
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
    result = extract_method(instructions_raw)
    assert result is None

def test_extract_method_lower_case():
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
        "name": "blend",
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
    result = extract_method(instructions_raw)
    assert result == "BLEND"

