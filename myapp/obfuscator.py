# obfuscator.py
import string
import random


def obfuscate_code(code):
    # Define a mapping of characters to be replaced
    char_map = {
        "a": "ɑ",
        "b": "ɓ",
        "c": "ɔ",
        "d": "ɗ",
        "e": "ɛ",
        "f": "ʄ",
        "g": "ɠ",
        "h": "ɦ",
        "i": "ɩ",
        "j": "ʆ",
        "k": "ƙ",
        "l": "ɭ",
        "m": "ɱ",
        "n": "ɳ",
        "o": "ɵ",
        "p": "ƥ",
        "q": "ƣ",
        "r": "ɼ",
        "s": "ʂ",
        "t": "ƭ",
        "u": "ʊ",
        "v": "ʋ",
        "w": "ɯ",
        "x": "�χ",
        "y": "ɣ",
        "z": "ȥ",
    }

    # Replace characters in the code with their obfuscated counterparts
    obfuscated_code = "".join(char_map.get(char, char) for char in code)

    # Optionally, you can add more obfuscation techniques here

    return obfuscated_code
