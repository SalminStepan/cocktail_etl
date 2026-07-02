from app.normalizer import parse_ingredient

def test_parse_ingredient_with_ml_unit():
    ingredient = "45 ml Gin"

    result = parse_ingredient(ingredient)
    
    assert result["raw"] == ingredient
    assert result["amount"] == 45
    assert result["unit"] =="ml"
    assert result["name"] == "Gin"
    assert result["comment"] is None
    assert result["unresolved"] is False

def test_parse_ingredient_returns_unresolved_for_unknown_format():
    ingredient = "Top with soda"

    result = parse_ingredient(ingredient)

    assert result["raw"] == ingredient
    assert result["amount"] is None
    assert result["unit"] is None
    assert result["name"] is None
    assert result["comment"] is None
    assert result["unresolved"] is True

def test_parse_ingredient_with_multi_word_name():
    result = parse_ingredient("1 dash Orange bitters")
    assert result["raw"] == "1 dash Orange bitters"
    assert result["amount"] == 1
    assert result["unit"] == "dash"
    assert result["name"] == "Orange bitters"
    assert result["comment"] is None
    assert result["unresolved"] is False

def test_parse_ingredient_returns_unresolved_for_unknown_unit():
    result = parse_ingredient("3 flop Saline solution")
    assert result["raw"] == "3 flop Saline solution"
    assert result["amount"] is None
    assert result["unit"] is None
    assert result["name"] is None
    assert result["comment"] is None
    assert result["unresolved"] is True

def test_parse_ingredient_returns_unresolved_for_invalid_amount():
    result = parse_ingredient("1&frasl;4 barspoon Xanthan gum")
    assert result["raw"] == "1&frasl;4 barspoon Xanthan gum"
    assert result["amount"] == 0.25
    assert result["unit"] == "barspoon"
    assert result["name"] == "Xanthan gum"
    assert result["comment"] is None
    assert result["unresolved"] is False

def test_parse_ingredient_sprig_unit():
    ingredient = parse_ingredient("1 sprig Rosemary sprig")

    assert ingredient["amount"] == 1.0
    assert ingredient["unit"] == "sprig"
    assert ingredient["name"] == "Rosemary sprig"
    assert ingredient["unresolved"] is False


def test_parse_ingredient_knob_unit():
    ingredient = parse_ingredient("1 knob Unsalted butter")

    assert ingredient["amount"] == 1.0
    assert ingredient["unit"] == "knob"
    assert ingredient["name"] == "Unsalted butter"
    assert ingredient["unresolved"] is False