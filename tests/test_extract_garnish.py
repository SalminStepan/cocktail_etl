from app.normalizer import extract_garnish

def test_extract_garnish_pos_case():
    instructions_raw = [
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
    ]
    result = extract_garnish(instructions_raw)
    assert result == "lemon zest twist"

def test_extract_garnish_no_Prepare_garnish_step():
    instructions_raw = [
      {
        "@type": "HowToStep",
        "name": "Prepare glass",
        "url": "https://www.diffordsguide.com/cocktails/recipe/3/abbey#method-step-1",
        "text": "Select and pre-chill a COUPE GLASS."
      },
      {
        "@type": "HowToStep",
        "name": "Prepare Barnish",
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
    ]
    result = extract_garnish(instructions_raw)
    assert result is None
        
def test_extract_garnish_pos_case():
    instructions_raw = []
    result = extract_garnish(instructions_raw)
    assert result is None