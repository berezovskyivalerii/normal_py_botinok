from calculator import calculate_expression

def test_calculate_addition():
    assert calculate_expression('1+1+1') == '3'

def test_calculate_subtraction():
    assert calculate_expression('2-3') == '-1'

def test_calculate_division():
    assert calculate_expression('10/2') == '5.0'

def test_calculate_multiply():
    assert calculate_expression('2*3') == '6'

def test_calculate_multiply_with_spaces():
    assert calculate_expression('2   * 3') == '6'

def test_calculate_order_of_operations():
    assert calculate_expression('2+3*4') == '14'

def test_calculate_parentheses():
    assert calculate_expression('(2+3)*4') == '20'

def test_calculate_floats():
    assert calculate_expression('1.5 + 2.5') == '4.0'

def test_calculate_invalid_chars():
    assert calculate_expression('5a + 10') == None

def test_calculate_division_by_zero():
    assert calculate_expression('10 / 0') == None

def test_calculate_complex_expression():
    assert calculate_expression('10 * (2.5 + 1.5) / 4') == '10.0'

def test_calculate_leading_negative():
    assert calculate_expression('-5 + 20') == '15'
