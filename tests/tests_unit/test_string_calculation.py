from string_calculation import str_analisys

def test_only_digits():
    r = str_analisys("12345")
    assert r.digits == 5
    assert r.letters == 0
    assert r.letters_uppercase == 0
    assert r.letters_lowercase == 0
    assert r.chars == 5

def test_only_letters_lowercase():
    r = str_analisys("hello")
    assert r.digits == 0
    assert r.letters == 5
    assert r.letters_uppercase == 0
    assert r.letters_lowercase == 5
    assert r.chars == 5

def test_only_letters_uppercase():
    r = str_analisys("WORLD")
    assert r.digits == 0
    assert r.letters == 5
    assert r.letters_uppercase == 5
    assert r.letters_lowercase == 0
    assert r.chars == 5

def test_letters_mixed():
    r = str_analisys("HeLLo")
    assert r.letters == 5
    assert r.letters_uppercase == 3
    assert r.letters_lowercase == 2

def test_digits_and_letters():
    r = str_analisys("A1b2C3")
    assert r.digits == 3
    assert r.letters == 3
    assert r.letters_uppercase == 2
    assert r.letters_lowercase == 1
    assert r.chars == 6

def test_with_symbols():
    r = str_analisys("Hi!")
    assert r.digits == 0
    assert r.letters == 2
    assert r.chars == 3

def test_empty_string():
    r = str_analisys("")
    assert r.digits == 0
    assert r.letters == 0
    assert r.letters_uppercase == 0
    assert r.letters_lowercase == 0
    assert r.chars == 0

def test_spaces():
    r = str_analisys("   ")
    assert r.digits == 0
    assert r.letters == 0
    assert r.chars == 3

def test_mixed_all():
    r = str_analisys("Aa1!Bb2?")
    assert r.digits == 2
    assert r.letters == 4
    assert r.letters_uppercase == 2
    assert r.letters_lowercase == 2
    assert r.chars == 8

def test_unicode_letters():
    r = str_analisys("Привіт123")
    assert r.digits == 3
    assert r.letters == 6
    assert r.letters_uppercase == 1
    assert r.letters_lowercase == 5
    assert r.chars == 9
