from app.normalizer import normalize_recipe

def test_normalize_recipe_pos_case():
    raw_recipe = {
        "source": "diffordsguide",
        "source_url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey",
        "name": "Abbey",
        "description": "Discover how to make an Abbey using Gin, Americano bianco, Orange juice and Aromatic bitters in just 5 easy to follow steps",
        "image_url": "https://cdn.diffordsguide.com/cocktail/NAmyA8/square/0/512x512.webp?v=1737701571",
        "ingredients_raw": [
        "45 ml Gin",
        "22.5 ml Americano bianco",
        "22.5 ml Orange juice",
        "1 dash Aromatic bitters"
        ],
        "instructions_raw": [
        {
            "@type": "HowToStep",
            "name": "Prepare glass",
            "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-1",
            "text": "Select and pre-chill a COUPE GLASS."
        },
        {
            "@type": "HowToStep",
            "name": "Prepare garnish",
            "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-2",
            "text": "Prepare garnish of lemon zest twist."
        },
        {
            "@type": "HowToStep",
            "name": "SHAKE",
            "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-3",
            "text": "SHAKE all ingredients with ice."
        },
        {
            "@type": "HowToStep",
            "name": "FINE STRAIN",
            "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-4",
            "text": "FINE STRAIN into chilled glass."
        },
        {
            "@type": "HowToStep",
            "name": "Express",
            "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-5",
            "text": "EXPRESS lemon zest twist over the cocktail and use as garnish."
        }
        ],
        "keywords": [
        "Aperitivo/aperitif",
        "Classic/vintage"
        ],
        "rating": {
        "@type": "aggregateRating",
        "ratingValue": "4.5",
        "ratingCount": 56,
        "worstRating": "1",
        "bestRating": "5"
        },
        "published_at": "2017-04-07 14:34:38"
    }
    result = normalize_recipe(raw_recipe)
    assert result["parse_status"] == "ok"
    assert result["image_url"] == "https://cdn.diffordsguide.com/cocktail/NAmyA8/square/0/512x512.webp?v=1737701571"
    assert result["description"] == "Discover how to make an Abbey using Gin, Americano bianco, Orange juice and Aromatic bitters in just 5 easy to follow steps"   


def test_normalize_recipe_missing_name():
    raw_recipe = {
        "source": "diffordsguide",
        "source_url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey",
        "name": "",
        "description": "Discover how to make an Abbey using Gin, Americano bianco, Orange juice and Aromatic bitters in just 5 easy to follow steps",
        "image_url": "https://cdn.diffordsguide.com/cocktail/NAmyA8/square/0/512x512.webp?v=1737701571",
        "ingredients_raw": [
        "45 ml Gin",
        "22.5 ml Americano bianco",
        "22.5 ml Orange juice",
        "1 dash Aromatic bitters"
        ],
        "instructions_raw": [
        {
            "@type": "HowToStep",
            "name": "Prepare glass",
            "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-1",
            "text": "Select and pre-chill a COUPE GLASS."
        },
        {
            "@type": "HowToStep",
            "name": "Prepare garnish",
            "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-2",
            "text": "Prepare garnish of lemon zest twist."
        },
        {
            "@type": "HowToStep",
            "name": "SHAKE",
            "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-3",
            "text": "SHAKE all ingredients with ice."
        },
        {
            "@type": "HowToStep",
            "name": "FINE STRAIN",
            "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-4",
            "text": "FINE STRAIN into chilled glass."
        },
        {
            "@type": "HowToStep",
            "name": "Express",
            "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-5",
            "text": "EXPRESS lemon zest twist over the cocktail and use as garnish."
        }
        ],
        "keywords": [
        "Aperitivo/aperitif",
        "Classic/vintage"
        ],
        "rating": {
        "@type": "aggregateRating",
        "ratingValue": "4.5",
        "ratingCount": 56,
        "worstRating": "1",
        "bestRating": "5"
        },
        "published_at": "2017-04-07 14:34:38"
    }
    result = normalize_recipe(raw_recipe)
    assert result["parse_status"] == "failed"

def test_normalize_recipe_unresolved_ingredient():
    raw_recipe = {
        "source": "diffordsguide",
        "source_url": "https://www.diffordsguide.com/cocktails/recipe/1/abacaxi-ricaco",
        "name": "Abacaxi Ricaço",
        "description": "Discover how to make an Abacaxi Ricaço using Pineapple (fresh), Light gold rum 1-3yo, Lime juice and Superfine/caster sugar in 6 easy to follow steps",
        "image_url": "https://cdn.diffordsguide.com/cocktail/KO58rv/square/0/512x512.webp?v=1737701571",
        "ingredients_raw": [
        "1 whole Pineapple (fresh)",
        "90 ml Light gold rum 1-3yo",
        "22.5 ml Lime juice",
        "15 ml Superfine/caster sugar"
        ],
        "instructions_raw": [
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
        ],
        "keywords": [
        "Frozen (blended)",
        "Tiki/tropical"
        ],
        "rating": {
        "@type": "aggregateRating",
        "ratingValue": "4.0",
        "ratingCount": 13,
        "worstRating": "1",
        "bestRating": "5"
        },
        "published_at": "2016-04-10 14:51:44"
    }
    result = normalize_recipe(raw_recipe)
    assert result["parse_status"] == "partial"