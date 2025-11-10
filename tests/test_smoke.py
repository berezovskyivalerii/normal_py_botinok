from calculator import calculate_expression

def test_smoke():
    assert True

def test_calculate_addition():
    assert calculate_expression('1 + 1 + 1') == '3'

def test_calculate_sunstraction():
    assert calculate_expression('2-3') == '-1'
