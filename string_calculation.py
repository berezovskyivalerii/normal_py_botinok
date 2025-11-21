class StringData:
    digits: int = 0
    letters: int = 0
    letters_uppercase: int = 0
    letters_lowercase: int = 0
    chars: int = 0

def str_analisys(text: str):
    result = StringData()
    
    result.digits            = len(list(filter(lambda x: x.isdigit(), text)))
    result.letters           = len([char for char in text if char.isalpha()])
    result.letters_uppercase = len([char for char in text if char.isupper()])
    result.letters_lowercase = len([char for char in text if char.islower()])
    result.chars             = len(text)

    return result
